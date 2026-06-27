import fitz, sys, os
d = fitz.open("main.pdf")
os.makedirs("_preview", exist_ok=True)
pages = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else range(1, d.page_count+1)
for n in pages:
    d[n-1].get_pixmap(dpi=110).save(f"_preview/p{n:02d}.png")
print("pages:", d.page_count, "rendered:", list(pages))
