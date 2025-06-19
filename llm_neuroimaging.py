#make a call to llm to get neuroimaging papers using API key
#Assignment for Sprouts.AI
import requests

def fetch_neuroimaging_papers_crossref(query="neuroimaging", rows=5):
    """
    Fetches the most recent Crossref works matching 'neuroimaging'.
    """
    url = "https://api.crossref.org/works"
    params = {
        "query": query,
        "rows": rows,
        "sort": "published",
        "order": "desc"
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json().get("message", {}).get("items", [])
    papers = []
    for item in data:
        title = item.get("title", [""])[0]
        doi   = item.get("DOI", "")
        link  = f"https://doi.org/{doi}" if doi else item.get("URL", "")
        # choose published-print date, else published-online, else skip
        pdate = item.get("published-print", item.get("published-online", {}))
        date_parts = pdate.get("date-parts", [[]])[0]
        published = "-".join(str(x) for x in date_parts) if date_parts else ""
        authors = []
        for a in item.get("author", []):
            given = a.get("given", "")
            family = a.get("family", "")
            authors.append(f"{given} {family}".strip())
        papers.append({
            "title":     title,
            "authors":   authors,
            "published": published,
            "link":      link
        })
    return papers

def main():
    try:
        papers = fetch_neuroimaging_papers_crossref(rows=5)
    except Exception as e:
        print("Error fetching from Crossref:", e)
        return

    if not papers:
        print("No papers found.")
        return

    for i, p in enumerate(papers, 1):
        print(f"{i}. {p['title']}")
        print(f"   • Authors:   {', '.join(p['authors']) or 'N/A'}")
        print(f"   • Published: {p['published'] or 'N/A'}")
        print(f"   • Link:      {p['link'] or 'N/A'}\n")

if __name__ == "__main__":
    main()
