"""
extract.py
Download every PDF (if not already saved) and extract its text into data/index.json
"""

import json, pathlib, requests, io, tqdm, pdfminer.high_level

PDF_DIR = pathlib.Path("data/pdfs")
PDF_DIR.mkdir(parents=True, exist_ok=True)


def extract_all():
    with open("data/links.json") as fp:
        urls = json.load(fp)

    index = []
    for url in tqdm.tqdm(urls, desc="Processing PDFs"):
        fname = PDF_DIR / url.split("/")[-1]

        # Download once only
        if not fname.exists():
            r = requests.get(url, timeout=60)
            fname.write_bytes(r.content)

        text = pdfminer.high_level.extract_text(fname)
        index.append({"url": url, "text": text})

    with open("data/index.json", "w") as fp:
        json.dump(index, fp)
    print(f"✔ Indexed {len(index)} PDFs to data/index.json")


if __name__ == "__main__":
    extract_all()