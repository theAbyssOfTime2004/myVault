---
title: Tymex Assessment — Code Solutions
date: 2026-05-11
tags: [interview, assessment, tymex, python]
---

# Tymex Assessment — Phần Code (10 câu)

> Mỗi câu: **đề bài tóm tắt → phân tích → solution → giải thích test case mẫu**.
> Tất cả viết bằng Python thuần (chỉ dùng NumPy khi đề cho phép). Không dùng thư viện ML.

## Bảng tổng hợp

| Q | Function | Tóm tắt |
|---|----------|---------|
| 5 | `select_model(models, task)` | Chọn model theo health/version/provider |
| 7 | `clean_predictions(data, valid_labels)` | Lowercase + dedupe theo id, filter labels |
| 8 | `get_stable_models(logs, threshold)` | Models có success rate prod ≥ threshold |
| 11 | `calculate_model_costs(logs)` | Tính cost từ tokens × giá |
| 14 | `evaluate_model(y_true, y_pred)` | accuracy / precision / recall (binary) |
| 15 | `analyze_model_logs(logs)` | total_requests, success_rate, avg_response_time |
| 17 | `evaluate_model(y_true, y_pred_probs, labels=None)` | accuracy + macro_f1 deterministic |
| 23 | `evaluate_model(y_true, y_pred_logits)` | accuracy từ logits qua argmax |
| 25 | `aggregate_tokens(logs)` | Tổng tokens theo model_name |
| 26 | `compute_avg_response_time(logs)` | Avg response time chỉ khi status=success |

---

## Q5 — `select_model(models, task)`

**Đề bài:** Một AI Marketplace deploy nhiều model (summarization, sentiment, embeddings...). Mỗi model có metadata: name, provider, version, supported tasks, health_status. Chọn model phù hợp theo rules:
1. Chỉ dùng model có `health_status == "healthy"`.
2. Phải support `task` đã yêu cầu.
3. Nếu nhiều model qualify → chọn `version` cao nhất.
4. Nếu vẫn tie → chọn `provider` lexicographically smallest.
5. Không có match → return `"NO_MODEL_AVAILABLE"`.

**Phân tích:** Lọc theo (1)+(2), sort key composite `(-version, provider)` để (3)+(4) cùng lúc, lấy phần tử đầu. Nếu rỗng trả "NO_MODEL_AVAILABLE".

**Solution:**
```python
def select_model(models, task):
    candidates = [
        m for m in models
        if m["health_status"] == "healthy" and task in m["tasks"]
    ]
    if not candidates:
        return "NO_MODEL_AVAILABLE"
    candidates.sort(key=lambda m: (-m["version"], m["provider"]))
    return candidates[0]["name"]
```

**Test case mẫu:**
- Input: 2 models (modelA OpenAI v2 summarization healthy, modelB Azure v3 summarization healthy), task="summarization"
- Cả hai healthy + support → tie ở (1)(2) → so version → modelB v3 thắng → output "modelB" ✓

---

## Q7 — `clean_predictions(data, valid_labels)`

**Đề bài:** Pre-processing pipeline cho classification model. Input có thể có:
- Missing labels (`None`)
- Unknown labels (không thuộc valid set)
- Inconsistent casing (`'Cat'` vs `'cat'`)
- Duplicate `id` (giữ lần xuất hiện cuối)

Rules:
1. Normalize tất cả labels về lowercase
2. Bỏ record nếu `predicted_label` hoặc `true_label` là None
3. Bỏ record nếu label không thuộc valid set
4. Nếu duplicate id → keep last occurrence
5. Return list of tuples `(id, predicted_label, true_label)` sorted by id ascending

**Phân tích:** Dùng dict `{id: tuple}` để tự động overwrite (giữ last). Iterate tuần tự để đảm bảo "last" đúng nghĩa. Cuối cùng sort theo id.

**Solution:**
```python
def clean_predictions(data, valid_labels):
    valid_set = {l.lower() for l in valid_labels}
    seen = {}
    for rec in data:
        pred = rec.get("predicted_label")
        true = rec.get("true_label")
        if pred is None or true is None:
            continue
        pred_l = pred.lower()
        true_l = true.lower()
        if pred_l not in valid_set or true_l not in valid_set:
            continue
        seen[rec["id"]] = (rec["id"], pred_l, true_l)
    return sorted(seen.values(), key=lambda t: t[0])
```

**Test case mẫu:**
- data = [{id:'1', pred:'Cat', true:'cat'}, {id:'2', pred:'Dog', true:None}, {id:'3', pred:'Fish', true:'fish'}], valid=['cat','dog']
- id 1: cả hai sau lower → 'cat' ∈ valid → giữ
- id 2: true=None → bỏ
- id 3: 'fish' ∉ valid → bỏ
- Output: `[('1', 'cat', 'cat')]` ✓

---

## Q8 — `get_stable_models(logs, threshold)`

**Đề bài:** Logs deployment dạng `"timestamp | model_name | environment | status"` (env ∈ {staging, production}, status ∈ {SUCCESS, FAIL}). Một model "stable" nếu **success rate trong production** ≥ threshold. Return list model_names sorted alphabetically. Bỏ model không có production logs.

**Phân tích:** Chỉ đếm logs có `environment == "production"`. Tách `success_count` và `total_count` theo model. Lọc theo threshold rồi sort.

**Solution:**
```python
from collections import defaultdict

def get_stable_models(logs, threshold):
    counts = defaultdict(lambda: [0, 0])  # [success, total]
    for log in logs:
        parts = [p.strip() for p in log.split("|")]
        if len(parts) != 4:
            continue
        _, name, env, status = parts
        if env != "production":
            continue
        counts[name][1] += 1
        if status == "SUCCESS":
            counts[name][0] += 1
    return sorted(
        name for name, (s, t) in counts.items()
        if t > 0 and s / t >= threshold
    )
```

**Test case mẫu:**
- logs = [modelA prod SUCCESS, modelA prod FAIL, modelB prod SUCCESS, modelB staging FAIL], threshold=0.5
- modelA: 1/2 = 0.5 ≥ 0.5 ✓
- modelB: 1/1 = 1.0 ≥ 0.5 ✓ (staging bị skip)
- Output: `["modelA", "modelB"]` ✓

---

## Q11 — `calculate_model_costs(logs)`

**Đề bài:** Mỗi log entry: `{model_name, tokens_used, cost_per_1k_tokens}`. Rules:
- `cost = (tokens_used / 1000) * cost_per_1k_tokens`
- Total cost per model = sum tất cả requests
- Output dict `{model_name: total_cost}` rounded to 4 decimals
- Bỏ entry nếu `tokens_used < 0`
- Empty input → `{}`
- model_names case-sensitive

**Phân tích:** Defaultdict accumulator, round cuối cùng. Note: round(0.06+0.03) = 0.09 nhưng float arithmetic có thể tạo 0.0899999... → round 4 decimals an toàn.

**Solution:**
```python
from collections import defaultdict

def calculate_model_costs(logs):
    totals = defaultdict(float)
    for log in logs:
        tokens = log["tokens_used"]
        if tokens < 0:
            continue
        cost = (tokens / 1000) * log["cost_per_1k_tokens"]
        totals[log["model_name"]] += cost
    return {k: round(v, 4) for k, v in totals.items()}
```

**Test case mẫu:**
- logs = [{gpt-4, 2000, 0.03}, {gpt-4, 1000, 0.03}]
- entry 1: 2000/1000 * 0.03 = 0.06
- entry 2: 1000/1000 * 0.03 = 0.03
- Output: `{"gpt-4": 0.09}` ✓

---

## Q14 — `evaluate_model(y_true, y_pred)`

**Đề bài:** Binary classification (0/1). Tính:
- Accuracy = (TP + TN) / total
- Precision = TP / (TP + FP), nếu mẫu số = 0 → 0
- Recall = TP / (TP + FN), nếu mẫu số = 0 → 0
- Round 2 decimals
- Length của y_true và y_pred luôn bằng nhau, chỉ chứa 0/1.

**Phân tích:** Đếm 4 confusion matrix cells trong 1 vòng for. Áp dụng safe-division.

**Solution:**
```python
def evaluate_model(y_true, y_pred):
    tp = tn = fp = fn = 0
    for t, p in zip(y_true, y_pred):
        if   p == 1 and t == 1: tp += 1
        elif p == 0 and t == 0: tn += 1
        elif p == 1 and t == 0: fp += 1
        elif p == 0 and t == 1: fn += 1
    total = len(y_true)
    accuracy  = (tp + tn) / total       if total       else 0
    precision = tp / (tp + fp)          if (tp + fp)   else 0
    recall    = tp / (tp + fn)          if (tp + fn)   else 0
    return {
        "accuracy":  round(accuracy,  2),
        "precision": round(precision, 2),
        "recall":    round(recall,    2),
    }
```

**Test case mẫu:**
- y_true=[1,0,1,1,0], y_pred=[1,0,0,1,0] → TP=2, TN=2, FP=0, FN=1
- accuracy=4/5=0.8, precision=2/2=1.0, recall=2/3≈0.67
- Output: `{"accuracy": 0.8, "precision": 1.0, "recall": 0.67}` ✓

---

## Q15 — `analyze_model_logs(logs)`

**Đề bài:** Logs là `List[str]`, mỗi entry `"model_id|timestamp_ms|response_time_ms|status"`. Cho mỗi `model_id` tính:
1. `total_requests`: tổng số request
2. `success_rate`: success / total, round 2 decimals
3. `avg_response_time`: avg của **chỉ requests success**, round nearest integer (= 0 nếu không có success)

Logs có thể chưa sort. Return dict `{model_id: {...}}`.

**Phân tích:** Một pass aggregate sum/count theo model. Cuối cùng tính rate và avg an toàn.

**Solution:**
```python
from collections import defaultdict

def analyze_model_logs(logs):
    data = defaultdict(lambda: {"total": 0, "success": 0, "rt_sum": 0})
    for log in logs:
        mid, _, rt, status = log.split("|")
        d = data[mid]
        d["total"] += 1
        if status == "success":
            d["success"] += 1
            d["rt_sum"] += int(rt)
    out = {}
    for mid, d in data.items():
        avg = round(d["rt_sum"] / d["success"]) if d["success"] else 0
        out[mid] = {
            "total_requests":     d["total"],
            "success_rate":       round(d["success"] / d["total"], 2),
            "avg_response_time":  avg,
        }
    return out
```

**Test case mẫu:**
- logs = ["m1|1000|120|success", "m1|1010|130|fail", "m2|1020|200|success"]
- m1: total=2, success=1, rate=0.5, avg=120
- m2: total=1, success=1, rate=1.0, avg=200
- Output: `{"m1": {total_requests:2, success_rate:0.5, avg_response_time:120}, "m2": {total_requests:1, success_rate:1.0, avg_response_time:200}}` ✓

---

## Q17 — `evaluate_model(y_true, y_pred_probs, labels=None)`

**Đề bài:** Compute deterministic accuracy + macro_f1.
1. `y_true`: list class labels (strings)
2. `y_pred_probs`: list of dicts `{label: probability}`
3. `labels`: optional. Nếu None → derive từ `y_true ∪ keys(y_pred_probs)` rồi sort lex
4. **Prediction rule:**
   - Chọn label có prob cao nhất
   - Nếu 2+ labels prob bằng nhau trong tolerance `1e-12` → chọn lex smallest
   - Round probs về 8 decimals trước khi so sánh (chống floating drift)
5. **Numerical stability:**
   - Round accuracy, macro_f1 về 2 decimals
   - Tránh ZeroDivision (precision/recall fallback = 0)
6. Output: `{"accuracy": float, "macro_f1": float}`

**Phân tích:**
- **Bước 1:** Determine label set. **Bước 2:** Convert probs → predicted label deterministic (round 8 decimals + tie-break lex). **Bước 3:** Tính TP/FP/FN per label, F1 từng label, macro_f1 = mean. **Bước 4:** Round 2 decimals.

**Solution:**
```python
from typing import List, Dict

def evaluate_model(y_true: List[str], y_pred_probs: List[Dict[str, float]],
                   labels=None) -> Dict[str, float]:
    # 1) Determine label universe
    if labels is None:
        all_labels = set(y_true)
        for p in y_pred_probs:
            all_labels.update(p.keys())
        labels = sorted(all_labels)

    # 2) Deterministic argmax with tie-break (lex smallest)
    y_pred = []
    for probs in y_pred_probs:
        rounded = {k: round(v, 8) for k, v in probs.items()}
        max_p = max(rounded.values())
        winners = sorted(k for k, v in rounded.items() if abs(v - max_p) < 1e-12)
        y_pred.append(winners[0])

    # 3) Accuracy
    n = len(y_true)
    correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    accuracy = correct / n if n else 0.0

    # 4) Per-label F1 → macro F1
    f1_list = []
    for lbl in labels:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == lbl and p == lbl)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != lbl and p == lbl)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == lbl and p != lbl)
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall    = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
        f1_list.append(f1)
    macro_f1 = sum(f1_list) / len(f1_list) if f1_list else 0.0

    return {"accuracy": round(accuracy, 2), "macro_f1": round(macro_f1, 2)}
```

**Test case mẫu:**
- y_true=["cat","dog","cat"], probs=[{cat:0.9,dog:0.1},{cat:0.4,dog:0.6},{cat:0.5,dog:0.5}]
- predict: cat, dog, cat (sample 3 tie → lex smallest "cat")
- accuracy = 3/3 = 1.0
- cat: TP=2, FP=0, FN=0 → F1=1.0; dog: TP=1, FP=0, FN=0 → F1=1.0
- macro_f1 = 1.0
- Output: `{"accuracy": 1.0, "macro_f1": 1.0}` ✓

---

## Q23 — `evaluate_model(y_true, y_pred_logits)`

**Đề bài:** Multi-class classification accuracy từ logits.
- `y_true`: list of true class labels (int starting from 0)
- `y_pred_logits`: 2D list, `y_pred_logits[i][c]` = logit của class c cho sample i
- Convert logits → predicted class via argmax
- Accuracy = correct / total, round 2 decimals
- Constraints: 1 ≤ samples ≤ 1000, 2 ≤ classes ≤ 10, chỉ dùng standard Python hoặc NumPy

**Phân tích:** Argmax từng row, đếm match, chia tổng. Đơn giản nhất.

**Solution:**
```python
def evaluate_model(y_true, y_pred_logits):
    correct = 0
    for t, logits in zip(y_true, y_pred_logits):
        pred = max(range(len(logits)), key=lambda i: logits[i])
        if pred == t:
            correct += 1
    return round(correct / len(y_true), 2)
```

**Test case mẫu:**
- y_true=[0,1,2], logits=[[2.0,1.0,0.1],[0.5,2.5,0.3],[0.2,0.1,3.0]]
- argmax: 0,1,2 → all correct → 1.0 ✓

---

## Q25 — `aggregate_tokens(logs)`

**Đề bài:** Logs streaming format `"client_id|model_name|tokens_used|timestamp"`. Inconsistencies cần ignore:
- `tokens_used` phải là **positive integer**
- Malformed rows: sai số fields, tokens_used non-integer, hoặc negative → bỏ
- Return dict `{model_name: total_tokens}` sorted ascending khi printed.

**Phân tích:** Tách từng entry, validate 4 fields + parse int. Tích lũy theo model_name. Cuối cùng sort key.

**Solution:**
```python
from collections import defaultdict

def aggregate_tokens(logs):
    totals = defaultdict(int)
    for log in logs:
        parts = log.split("|")
        if len(parts) != 4:
            continue
        _, name, tokens_str, _ = parts
        try:
            t = int(tokens_str)
        except ValueError:
            continue
        if t <= 0:
            continue
        totals[name] += t
    return dict(sorted(totals.items()))
```

**Test case mẫu:**
- logs = ["c1|gpt-4|100|169...0", "c2|gpt-4|200|169...1", "c3|bert|50|169...2"]
- gpt-4: 100+200=300, bert: 50
- Output: `{"bert": 50, "gpt-4": 300}` ✓

> **Lưu ý:** Nếu spec yêu cầu cho phép `tokens_used == 0`, đổi `t <= 0` thành `t < 0`. Đề ghi rõ "positive integer" nên ưu tiên `> 0`.

---

## Q26 — `compute_avg_response_time(logs)`

**Đề bài:** Logs format `"timestamp|model_name|response_time_ms|status"`. Rules:
- Bỏ malformed records (sai fields hoặc response_time non-integer)
- Bỏ records nếu `status != "success"`
- Group by `model_name`, tính avg response time **chỉ trên successful requests**, **floor xuống integer** (rounded down to nearest integer)
- Model không có valid successful records → không xuất hiện trong output

**Phân tích:** Một pass: validate fields, parse int, filter status=success, accumulate sum+count. Cuối cùng `floor(sum/count)`. Dùng `math.floor` thay vì `int()` để đúng nghĩa "rounded down" (an toàn cho trường hợp nếu giá trị âm — dù ở đây không có).

**Solution:**
```python
import math
from collections import defaultdict

def compute_avg_response_time(logs):
    data = defaultdict(lambda: [0, 0])  # [sum, count]
    for log in logs:
        parts = log.split("|")
        if len(parts) != 4:
            continue
        _, name, rt_str, status = parts
        if status != "success":
            continue
        try:
            r = int(rt_str)
        except ValueError:
            continue
        data[name][0] += r
        data[name][1] += 1
    return {k: math.floor(s / c) for k, (s, c) in data.items() if c > 0}
```

**Test case mẫu:**
- logs = ["...|gpt-vision|120|success", "...|gpt-vision|150|success", "...|gpt-text|200|fail"]
- gpt-vision: avg(120,150) = 135 → floor = 135
- gpt-text: chỉ fail → loại
- Output: `{"gpt-vision": 135}` ✓

---

## Patterns chung của bộ code

1. **Edge cases để ý:** empty input → trả `{}`/`0`; division-by-zero → fallback giá trị; floating drift → round trước khi so sánh (Q17).
2. **Determinism:** mọi tie-break phải có rule rõ ràng (Q5: version desc + provider asc; Q17: lex smallest).
3. **Validation parsing:** Q25/Q26 cần `try/except int()` + check `len(parts) == 4`.
4. **Aggregation pattern:** `defaultdict` + 1 pass duyệt logs → tính metric ở pass thứ 2.
5. **Sort cho output ổn định:** `sorted()` cuối cùng để dễ test.

## Checklist trước khi submit

- [ ] Đọc kỹ ràng buộc (positive vs non-negative, round vs floor, empty input behavior)
- [ ] Đối chiếu lại format chính xác từng test case mẫu
- [ ] Kiểm tra tie-break / determinism
- [ ] Test edge: empty list, all malformed, single record, duplicate keys
- [ ] Đảm bảo không in/print dư (chỉ return)
