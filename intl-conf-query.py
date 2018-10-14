import csv
from config import config
from utils import scopus_query_request, get_total, countries
"""
Collect stats on papers accepted to conferences over many years broken down
by country of affiliation of accepted paper.
"""

if __name__ == "__main__":
    api_key = config.api_key
    conferences = [
        "AAAI",
        "IJCAI",
        "NIPS",
        "CVPR",
        "ICML",
        "ICRA"
    ]

    query_tmpl = "CONF( {} ) AND PUBYEAR = {} AND AFFILCOUNTRY( {} )"
    all_querty_tmpl = "CONF( {} ) AND PUBYEAR = {}"

    # Loop over years, conferences and countries to get counts by country
    # This is automatic in the web-ui but requires this loop through the API
    # NOTE: Super slow, API might have better way of doing this.
    outfile = 'intl-scopus-2018.csv'
    with open(outfile, 'w') as fh:
        writer = csv.writer(fh)
        for year in range(1995, 2019):
            print("Year: ", year)
            writer.writerow([year])
            writer.writerow([""] + conferences)
            totals_row = ["Query Total"]
            for conf in conferences:
                query_string = all_querty_tmpl.format(conf, year)
                response = scopus_query_request(query_string, api_key)
                full_total = get_total(response)
                totals_row.append(full_total)
            writer.writerow(totals_row)

            for country in countries:
                print("Country:", country)
                country_row = [country]
                for conf in conferences:
                    query_string = query_tmpl.format(conf, year, country)
                    response = scopus_query_request(query_string, api_key)
                    conf_total = get_total(response)
                    country_row.append(conf_total)
                writer.writerow(country_row)
