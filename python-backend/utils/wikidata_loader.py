import requests
import json

# SPARQL query
sparql_query = """
SELECT ?word ?wordLabel ?description WHERE {
    ?word wdt:P31 wd:Q20747295;  # Instance of a word
          wdt:P279 wd:Q186165;   # Subclass of English word
          schema:description ?description.
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    FILTER (LANG(?description) = "en")         # Description in English
}
LIMIT 1000
"""

# Wikidata SPARQL endpoint
url = "https://query.wikidata.org/sparql"

# Query headers
headers = {
    "User-Agent": "WikidataWordExtractor/1.0 (https://your-website.com)",
    "Accept": "application/json"
}

# Send the SPARQL query
response = requests.get(url, params={"query": sparql_query, "format": "json"}, headers=headers)

# Check the response
if response.status_code == 200:
    data = response.json()
    
    # Extract results
    words = []
    for item in data["results"]["bindings"]:
        word = {
            "id": item["word"]["value"],
            "label": item["wordLabel"]["value"],
            "description": item["description"]["value"]
        }
        words.append(word)
    
    # Save as JSON file
    with open("popular_words.json", "w") as f:
        json.dump(words, f, indent=4)
    
    print("Words successfully saved to 'popular_words.json'")
else:
    print("Failed to fetch data:", response.status_code, response.text)
