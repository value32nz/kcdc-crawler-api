"""
crawler.py
Find every PDF link on the KCDC District Plan page and save them to data/links.json
"""

import requests, bs4, json, pathlib, re

BASE_URL = "https://www.kapiticoast.govt.nz"
START_PAGE = f"{BASE_URL}/council/forms-documents/district-plan/operative-district-plan-2021/"
PDF_RE = re.compile(r"\.pdf$", re.I)


def crawl():
    html = requests.get(START_PAGE, timeout=30).text
    soup = bs4.BeautifulSoup(html, "html.parser")

    pdf_links = {
        BASE_URL + a["href"]
        for a in soup.select("a[href]") if PDF_RE.search(a["href"])
    }

    pathlib.Path("data").mkdir(exist_ok=True)
    with open("data/links.json", "w") as fp:
        json.dump(sorted(pdf_links), fp, indent=2)

    print(f"✔ Found {len(pdf_links)} PDFs and saved them to data/links.json")


if __name__ == "__main__":
    crawl()
