from bs4 import BeautifulSoup

def load_context_text():
    with open(
        "data/sec_data/extracted_2019q1/readme.htm",
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as f:
        html = f.read()

    soup = BeautifulSoup(html, "lxml")

    # Remove scripts, styles, tables
    for tag in soup(["script", "style", "table"]):
        tag.decompose()

    text = soup.get_text(separator=" ")

    # Clean whitespace
    text = " ".join(text.split())

    return text

