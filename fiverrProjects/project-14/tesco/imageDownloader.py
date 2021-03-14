import concurrent.futures
import csv
import requests
# import os

# _, _, files1 = next(os.walk("image_by_product_name"))
# _, _, files2 = next(os.walk("image_by_product_id"))
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50"

def download_img(listings):
    li = listings.split(" | ")
    img_url = li[2]
    img_name_prod_name = li[1]
    img_name_prod_id = li[0]
    try:
      img_bytes = requests.get(img_url, headers={'User-Agent': user_agent}, timeout=10).content 
      try:
        with open(f"./image_by_product_name/{img_name_prod_name}.jpeg", 'wb') as img_file:
            img_file.write(img_bytes)
      except:
        pass
      try:
        with open(f"./image_by_product_id/{img_name_prod_id}.jpeg", 'wb') as img_file:
            img_file.write(img_bytes)
      except:
        pass
    except:
      pass

if __name__ == "__main__":
  urlList = []

  with open('tescoGrocery.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for indx,url in enumerate(csv_reader):
      if url[-1].startswith("http"):
        urlList.append(f'''{url[0]} | {url[1]} | {url[-1]}''')  

  with concurrent.futures.ProcessPoolExecutor() as executor:
      executor.map(download_img, urlList)