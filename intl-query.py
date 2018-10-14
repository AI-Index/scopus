import csv
from config import config
from utils import scopus_query_request, get_total, countries
"""
Collect stats on AI papers over many years broken down by country of
affiliation
"""

if __name__ == "__main__":

    api_key = config.api_key
    query_tmpl = "title-abs-key(artificial intelligence) AND PUBYEAR = {} AND AFFILCOUNTRY( {} )"

    # Loop over years and countries to get counts by country
    # NOTE: Super slow, API might have better way of doing this.
    outfile = 'intl-ai-papers-scopus-2018.csv'
    years = list(range(1995, 2019))
    with open(outfile, 'w') as fh:
        writer = csv.writer(fh)
        writer.writerow([""] + years)
        for country in countries:
            print("Country: ", country)
            country_row = [country]
            for year in years:
                print("Year:", year)
                query_string = query_tmpl.format(year, country)
                response = scopus_query_request(query_string, api_key)
                year_total = get_total(response)
                country_row.append(year_total)
            writer.writerow(country_row)
