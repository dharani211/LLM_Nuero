#make a call to llm to get neuroimaging papers using API key
#Assignment for Sprouts.AI
import requests

def get_neuroimaging_publications(term="neuroimaging", count=5):
    """
    Query Crossref for the most recent works matching the given term.
    Returns a list of dicts containing title, authors, date, and DOI link.
    """
    api_url = "https://api.crossref.org/works"
    query_params = {
        "query": term,
        "rows": count,
        "sort": "published",
        "order": "desc"
    }
    response = requests.get(api_url, params=query_params, timeout=10)
    response.raise_for_status()
    entries = response.json().get("message", {}).get("items", [])
    
    publications = []
    for entry in entries:
        # Title and DOI or fallback URL
        title = entry.get("title", [""])[0]
        doi   = entry.get("DOI", "")
        link  = f"https://doi.org/{doi}" if doi else entry.get("URL", "")
        
        # Determine publication date
        date_info = entry.get("published-print") or entry.get("published-online") or {}
        parts     = date_info.get("date-parts", [[]])[0]
        pub_date  = "-".join(str(x) for x in parts) if parts else "N/A"
        
        # Assemble author list
        authors = []
        for author in entry.get("author", []):
            given  = author.get("given", "")
            family = author.get("family", "")
            full_name = f"{given} {family}".strip()
            if full_name:
                authors.append(full_name)
        
        publications.append({
            "title":     title,
            "authors":   authors or ["N/A"],
            "published": pub_date,
            "link":      link
        })
    
    return publications

def display_publications(publications):
    if not publications:
        print("No publications found.")
        return
    
    for idx, pub in enumerate(publications, start=1):
        print(f"{idx}. {pub['title']}")
        print(f"   • Authors:   {', '.join(pub['authors'])}")
        print(f"   • Published: {pub['published']}")
        print(f"   • Link:      {pub['link']}\n")

def main():
    try:
        pubs = get_neuroimaging_publications(count=5)
    except Exception as err:
        print(f"Error fetching data: {err}")
        return
    
    display_publications(pubs)

if __name__ == "__main__":
    main()
