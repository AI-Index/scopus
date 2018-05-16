import requests

api_key = "REPLACE_WITH_API_KEY____________"

def scopus_query_request(query, api_key):
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

def query_over_time(query_items, start_year=1995, end_year=2018):

    print (" AND ".join(query_items) + "\n")

    results = []

    tmp_query_items = query_items + ["PUBYEAR BEF %d" % (start_year + 1)]
    query_string = " AND ".join(tmp_query_items)
    response = scopus_query_request(query_string, api_key)
    data = response.json()
    count = data["search-results"]["opensearch:totalResults"]
    print("X-%d:" % start_year, count)

    for i in range(start_year, end_year):
        tmp_query_items = (query_items + [
            "PUBYEAR AFT %d" % (i),
            "PUBYEAR BEF %d" % (i + 2)
            ])
        query_string = " AND ".join(tmp_query_items)
        response = scopus_query_request(query_string, api_key)
        data = response.json()
        count = data["search-results"]["opensearch:totalResults"]

        result = (i + 1, count)
        results.append(result)

        print("%d: %s" % result)

if __name__ == "__main__":
    title_abs_key_terms = ([
        "artificial intelligence",
        # "deep learning",
        # "reinforcement learning",
        # "computer vision",
        # "speech recognition"
        ])

    query_items = ([
        # " OR ".join(["title-abs-key(%s)" % term for term in title_abs_key_terms]),
        # "SUBJAREA(COMP)"
        ])
    query_over_time(query_items)

