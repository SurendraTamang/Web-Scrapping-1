import requests
import pandas as pd
import xlrd
import concurrent.futures
import csv


class LinkExtractor():
    df = pd.read_excel('''D:/upworkWorkspace/Testing/betalist/BetaList Mastersheet.xlsx''', sheet_name='sheet2')
    query = df['query'].tolist()

    # def clean_url(self, url):
    #     try:
    #         if url.endswith("?ref=producthunt") or url.endswith("&ref=producthunt"):
    #             return url[:-16]
    #         else:
    #             return url
    #     except:
    #         return url

    def get_final_url(self, query):
        li = query.split("||")
        url = li[0]
        try:
            r_url = requests.get(url,timeout=10,verify=False)
            final_url = r_url.url
            li.append(final_url)
            with open('BL1.csv','a',newline='',encoding='utf-8') as f:
                linkwriter = csv.writer(f)
                linkwriter.writerow(li)
                print(f'              Fteching for: {li[0]} => SUCCESS')
        except:
            li.append('NA')
            with open('BL1.csv','a',newline='',encoding='utf-8') as f:
                linkwriter = csv.writer(f)
                linkwriter.writerow(li)
                print(f'Fteching for: {li[0]} => FAILURE')


if __name__ == "__main__":
    link_obj = LinkExtractor()                   
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(link_obj.get_final_url, link_obj.query)


