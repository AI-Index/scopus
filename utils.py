import requests

countries = [
    "United States",
    "China",
    "United Kingdom",
    "Australia",
    "Japan",
    "Germany",
    "Canada",
    "Singapore",
    "France",
    "Italy",
    "India",
    "Hong Kong",
    "Spain",
    "Switzerland",
    "Brazil",
    "South Korea",
    "Israel",
    "Austria",
    "Netherlands",
    "Qatar",
    "Sweden",
    "Belgium",
    "Finland",
    "Poland",
    "Ireland",
    "Czech Republic",
    "Cyprus",
    "Georgia",
    "Greece",
    "New Zealand",
    "Chile",
    "Iran",
    "Portugal",
    "Russian Federation",
    "Saudi Arabia",
    "South Africa",
    "Taiwan",
    "United Arab Emirates",
    "Bangladesh",
    "Denmark",
    "Egypt",
    "Estonia",
    "Hungary",
    "Lebanon",
    "Luxembourg",
    "Mexico",
    "Norway",
    "Pakistan",
    "Romania",
    "Venezuela"
]


def scopus_query_request(query, api_key):
    if 'REPLACE' in api_key:
        raise Exception("Invalid API key. Please update config.py")
    # Request
    # GET http://api.elsevier.com/content/search/scopus
    try:
        response = requests.get(
            url="https://api.elsevier.com/content/search/scopus",
            params={
                "query": query,
                "apiKey": api_key,
            },
        )
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
    return response


def get_total(response):
    """
    Returns the 'total results' count from a scopus query response
    """
    data = response.json()
    results = data['search-results']
    total = results['opensearch:totalResults']

    return int(total)
