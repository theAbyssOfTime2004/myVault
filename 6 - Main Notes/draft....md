```python
import asyncio

import logging

import re

import os

from collections import deque

from datetime import datetime, timezone

from typing import Any, Dict, List, Optional, Set

from urllib.parse import urljoin, urlparse

from playwright.async_api import async_playwright

import requests

import httpx

import tenacity

from fastapi import APIRouter, BackgroundTasks, HTTPException

from lxml import html

from pydantic import BaseModel

from app.api.data_sources.training_worker import get_datasource_service

from app.api.data_sources.model import RecordWebCrawl

  

router = APIRouter()

logging.basicConfig(level=logging.INFO)

  
  

STOPWORDS = ["#", "/login", "/tai-khoan", "/account", "?trang", "?page", "Warning", "@", "upload"]

STOPWORD_PATTERN = re.compile("|".join(map(re.escape, STOPWORDS)))

EXT_BLACKLIST = {

".jpg", ".jpeg", ".png", ".gif", ".svg", ".ico",

".pdf", ".zip", ".rar", ".tar", ".gz", ".mp4",

".mp3", ".avi", ".wmv", ".doc", ".docx", ".xls", ".xlsx"

}

BAD_SCHEME_IN_PATH = re.compile(r"https?:/[^/]", re.IGNORECASE)

BAD_EMBEDDED = re.compile(r"https?://", re.IGNORECASE)

BACKEND_API_BASE_URL = os.getenv("BACKEND_API_BASE_URL")

CONCURRENCY_DEFAULT = 10

BATCH_SIZE = 15

MainDataSourceService = get_datasource_service()

  

class CrawlDomainRequest(BaseModel):

agent_id: str

url: str

concurrency: Optional[int] = 10

  

class OnboardCrawlDomainRequest(BaseModel):

user_id: Optional[str] = None

agent_id: str

url: str

concurrency: Optional[int] = 10

  

class LinkItem(BaseModel):

link: str

title: Optional[str] = None

  

class CrawlDomainResponse(BaseModel):

status: str

  

class OnboardCrawlDomainResponse(BaseModel):

status: str

  

async def fetch_rendered_hrefs(url: str) -> List[str]:

async with async_playwright() as pw:

browser = await pw.chromium.launch(headless=True)

page = await browser.new_page(

user_agent=(

"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "

"AppleWebKit/537.36 (KHTML, like Gecko) "

"Chrome/114.0.0.0 Safari/537.36"

)

)

timeout = 90_000

await page.goto(url, wait_until="domcontentloaded", timeout=timeout)

await page.wait_for_load_state("domcontentloaded", timeout=timeout)

hrefs = await page.eval_on_selector_all(

"a",

"anchors => anchors.map(a => a.href)"

)

await browser.close()

return hrefs

  

def is_valid_url(u: str) -> bool:

if not (u.startswith("http://") or u.startswith("https://")):

return False

  

parsed = urlparse(u)

  

# 2) No repeated full schemes in path

if "http://" in parsed.path or "https://" in parsed.path:

return False

  

# 3) No malformed single‐slash scheme in path

if BAD_SCHEME_IN_PATH.search(parsed.path):

return False

  

# 4) Stopwords

if STOPWORD_PATTERN.search(u):

return False

  

path_lower = parsed.path.lower()

for ext in EXT_BLACKLIST:

if path_lower.endswith(ext):

return False

  

# 6) No long digit sequences (7 or more) in the path

if re.search(r"\d{7,}", parsed.path):

return False

  

return True

  

def is_clean_url(u: str) -> bool:

if not (u.startswith("http://") or u.startswith("https://")):

return False

if not is_valid_url(u):

return False

return True

  

def normalize_url(base: str, href: str) -> Optional[str]:

href_low = href.lower()

if href_low.count("http://") + href_low.count("https://") > 1:

return None

  

if href.startswith(("http://", "https://")):

parsed = urlparse(href)

if parsed.netloc != urlparse(base).netloc:

return None

if any(parsed.path.lower().endswith(ext) for ext in EXT_BLACKLIST):

return None

return parsed._replace(fragment="").geturl().rstrip("/")

  

if re.match(r"^[a-zA-Z]+:/[^/]", href):

return None

  

parsed = urlparse(href)

if any(parsed.path.lower().endswith(ext) for ext in EXT_BLACKLIST):

return None

full = urljoin(base, parsed.path)

return full.rstrip("/")

  

@tenacity.retry(

wait=tenacity.wait_exponential(multiplier=1, min=1, max=10),

stop=tenacity.stop_after_attempt(3),

reraise=True,

retry=tenacity.retry_if_exception_type((httpx.HTTPStatusError, httpx.RequestError, httpx.TimeoutException))

)

async def fetch_page(url: str, client: httpx.AsyncClient) -> httpx.Response:

resp = await client.get(url, timeout=7.0)

resp.raise_for_status()

return resp

  

async def extract_links(url: str, client: httpx.AsyncClient) -> List[Dict[str, str]]:

resp = await fetch_page(url, client)

base = str(resp.url).rstrip("/")

tree = html.fromstring(resp.text)

  

raw_href_list = tree.xpath("//a/@href")

if not raw_href_list:

rendered_hrefs = await fetch_rendered_hrefs(url)

raw_href_list = rendered_hrefs

  

items: List[Dict[str, str]] = [{"link": base, "title": ""}]

for href in raw_href_list:

norm = normalize_url(base, href)

if norm and is_valid_url(norm):

items.append({"link": norm, "title": None})

return items

  

@router.post(

"/fetch-link",

response_model=CrawlDomainResponse

)

async def fetch_link(

request: CrawlDomainRequest, background_tasks: BackgroundTasks

) -> Any:

"""

‣ Accept the same input as before.

‣ Immediately hand work off to a background task.

‣ Return only status, no crawl payload.

"""

try:

background_tasks.add_task(_run_crawl_job, request)

return CrawlDomainResponse(

status="success"

)

except Exception as e:

logging.error(f"Error in fetch_link: {e}")

raise HTTPException(status_code=500, detail=str(e))

  

async def _run_crawl_job(request: CrawlDomainRequest) -> None:

"""Breadth-first crawl with bounded concurrency and batched persistence."""

start = datetime.now(timezone.utc)

  

seed = request.url.rstrip("/")

concurrency = request.concurrency or CONCURRENCY_DEFAULT

  

visited: set[str] = set() # URLs we have *saved* already

queue: asyncio.Queue[str | None] = asyncio.Queue()

await queue.put(seed)

  

# Shared state

batch: list[RecordWebCrawl] = []

batch_lock = asyncio.Lock() # protect batch across workers

report: list[dict[str, str]] = [] # raw results for final log

  

async def flush_batch(force: bool = False) -> None:

"""Persist current batch if full or forced."""

async with batch_lock:

if batch and (force or len(batch) >= BATCH_SIZE):

await MainDataSourceService.create_url_datasource(

agent_id=request.agent_id,

links=list(batch),

title=None,

)

batch.clear()

  

async with httpx.AsyncClient(

http2=False,

follow_redirects=True,

limits=httpx.Limits(

max_connections=concurrency,

max_keepalive_connections=concurrency,

),

headers={

"User-Agent": (

"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "

"AppleWebKit/537.36 (KHTML, like Gecko) "

"Chrome/114.0.0.0 Safari/537.36"

)

},

) as client:

  

sem = asyncio.Semaphore(concurrency)

  

async def worker() -> None:

while True:

url = await queue.get()

if url is None: # poison pill → shutdown

queue.task_done()

break

  

async with sem:

items = await extract_links(url, client)

  

# process each discovered link

for item in items:

link = item["link"]

if link in visited or not is_valid_url(link):

continue # dedup & coarse filter first

  

visited.add(link) # mark before save / enqueue

  

async with batch_lock:

batch.append(RecordWebCrawl(**item))

await flush_batch()

  

await queue.put(link) # BFS

  

report.extend(items)

queue.task_done()

  

# spin workers

workers = [asyncio.create_task(worker()) for _ in range(concurrency)]

  

await queue.join() # wait until frontier exhausted

  

# stop workers

for _ in range(concurrency):

await queue.put(None)

await asyncio.gather(*workers, return_exceptions=True)

  

# flush remaining records (if any)

await flush_batch(force=True)

  

# prepare final unique count for log

clean_seen: set[str] = {

item["link"] for item in report if is_clean_url(item["link"])

}

  

logging.info(

"Crawl finished: %d links saved in %.1fs",

len(clean_seen),

(datetime.now(timezone.utc) - start).total_seconds(),

extra={"status": "success"},

)

  

def train_url(agent_id: str, url: str) -> bool:

api_url = f"{BACKEND_API_BASE_URL}/api/n/v1/datasources/website/{agent_id}"

headers = {

"accept": "application/json",

"Content-Type": "application/json"

}

payload = {

"links": [

{

"link": url,

"title": ""

}

]

}

try:

response = requests.post(api_url, json=payload, headers=headers)

response.raise_for_status()

return True

except requests.RequestException as e:

logging.error(f"Failed to train URL {url}: {e}")

return False

def save_without_train_url(agent_id: str, url: str) -> bool:

api_url = f"{BACKEND_API_BASE_URL}/api/n/v1/datasources/website/save/{agent_id}"

headers = {

"accept": "application/json",

"Content-Type": "application/json"

}

payload = {

"links": [

{

"link": url,

"title": ""

}

]

}

try:

response = requests.post(api_url, json=payload, headers=headers)

response.raise_for_status()

return True

except requests.RequestException as e:

logging.error(f"Failed to train URL {url}: {e}")

return False

def _get_limit_sync(user_id: str) -> Optional[int]:

"""Blocking HTTP call wrapped by run_in_executor."""

endpoint = f"{BACKEND_API_BASE_URL}/api/n/v1/plans/resource_usage/{user_id}/URL"

try:

resp = requests.get(endpoint, headers={"Accept": "application/json"}, timeout=5)

resp.raise_for_status()

except requests.RequestException as exc:

logging.error("Failed to obtain limit for %s (%s): %s", user_id, endpoint, exc)

return None

  

try:

data = resp.json()

except ValueError as exc:

logging.error("Non-JSON response for %s: %s", user_id, exc)

return None

  

remaining = data.get("remaining")

if isinstance(remaining, int):

logging.info(f"Remaining {remaining} urls!!!")

return remaining

  

logging.warning("Unexpected payload when checking limit for %s: %s", user_id, data)

return None

  

async def get_limit(user_id: str) -> Optional[int]:

loop = asyncio.get_running_loop()

return await loop.run_in_executor(None, _get_limit_sync, user_id)

  
  

async def _run_onboard_crawl_job(request: OnboardCrawlDomainRequest) -> None:

"""

Breadth-first crawl starting from `request.url`.

Saves each clean link via `train_url(...)`.

"""

start = datetime.now(timezone.utc)

  

seed_url = request.url.rstrip("/")

concurrency = request.concurrency or 10

agent_id = request.agent_id

user_id = request.user_id

  

try:

limit_url_number: Optional[int] = await get_limit(user_id)

limit_url_number = int(limit_url_number)

except:

limit_url_number = 20

print("User %s can train %s URLs", user_id, limit_url_number)

visited: set[str] = {seed_url}

crawled: set[str] = set()

trained_urls = 0 # ← will be incremented

queue: asyncio.Queue[str] = asyncio.Queue()

await queue.put(seed_url)

  

async with httpx.AsyncClient(

http2=False,

follow_redirects=True,

limits=httpx.Limits(

max_connections=concurrency,

max_keepalive_connections=concurrency,

),

headers={

"User-Agent": (

"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "

"AppleWebKit/537.36 (KHTML, like Gecko) "

"Chrome/114.0.0.0 Safari/537.36"

)

},

) as client:

  

sem = asyncio.Semaphore(concurrency)

  

async def worker() -> None:

nonlocal trained_urls # we mutate the outer variable

while True:

try:

url = await asyncio.wait_for(queue.get(), timeout=1)

except asyncio.TimeoutError:

break

  

async with sem:

try:

page_items = await extract_links(url, client)

except Exception as exc:

logging.warning("Failed to extract %s: %s", url, exc)

page_items = [{"link": url, "title": None}]

  

for item in page_items:

link = item["link"]

  

if not is_valid_url(link):

continue

  

if link not in visited:

visited.add(link)

await queue.put(link)

  

if link in crawled or not is_clean_url(link):

continue

  

crawled.add(link)

if limit_url_number is None or trained_urls < limit_url_number:

train_url(agent_id, link)

trained_urls += 1

else:

save_without_train_url(agent_id, link)

  

queue.task_done()

  

# Kick off the workers

await asyncio.gather(*(asyncio.create_task(worker()) for _ in range(concurrency)))

  

logging.info(

"Onboard crawl finished: %d links (%d trained) in %.1fs",

len(crawled),

trained_urls,

(datetime.now(timezone.utc) - start).total_seconds(),

)

  

@router.post("/fetch-link-onboard", response_model=OnboardCrawlDomainResponse)

async def fetch_link_onboard(

request: OnboardCrawlDomainRequest,

background_tasks: BackgroundTasks,

) -> OnboardCrawlDomainResponse:

"""

Kick off an onboarding crawl in the background.

"""

try:

background_tasks.add_task(_run_onboard_crawl_job, request)

return OnboardCrawlDomainResponse(status="Success")

except Exception as e:

logging.error(f"Error in fetch_link_onboard: {e}")

raise HTTPException(status_code=500, detail=str(e))
```