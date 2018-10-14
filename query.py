import csv
import datetime
from config import config
from utils import scopus_query_request
"""
Collect stats on AI papers and AI papers in computer science (a subset) over
many years.
"""


def query_over_time(query_items, start_year=1995, end_year=2019):

    print(" AND ".join(query_items))

    results = []

    api_key = config.api_key
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

        # result = (i + 1, count)
        result = count
        results.append(result)

        print("%d: %s" % (i + 1, result))

    print()

    return results


def create_ai_papers_csv(
    filename,
    ai_data,
    cs_data,
    total_data,
    start_year=1996
):
    year = start_year
    with open(filename, 'w') as csvfile:
        papers_writer = csv.writer(csvfile, delimiter=',')
        papers_writer.writerow(["Year", "AI", "CS", "ALL"])
        for (ai, cs, total) in zip(ai_data, cs_data, total_data):
            papers_writer.writerow([year, ai, cs, total])
            year += 1


if __name__ == "__main__":
    filename = "ai_papers.csv"
    start_year = 1995
    end_year = datetime.datetime.now().year

    title_abs_key_terms = (["artificial intelligence"])

    ai_query = [" OR ".join("title-abs-key(%s)" %
                            term for term in title_abs_key_terms)]
    cs_query = [" OR ".join(
        ["title-abs-key(%s)" % term for term in title_abs_key_terms]),
        "SUBJAREA(COMP)"]
    total_query = []

    ai_data, cs_data, total_data = (query_over_time(
        q, start_year=start_year, end_year=end_year) for q in [ai_query, cs_query, total_query])

    create_ai_papers_csv(
        filename,
        ai_data,
        cs_data,
        total_data,
        start_year=start_year+1
    )
