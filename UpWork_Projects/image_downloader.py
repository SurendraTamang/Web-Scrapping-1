import concurrent.futures
import pandas as pd
import time
import requests

cntr = True
while cntr:
    try:
        excel_path = input("Enter the file path: ")
        sheet = input("Enter the sheet name: ")
        if excel_path and sheet:
            cntr = False
        else:
            print("Please enter a valid file path / sheet name")
    except:
        pass
#df = pd.read_excel('./List 2 - location 1-17000.xlsx', sheet_name='Sheet1')
df = pd.read_excel(excel_path, sheet_name=sheet)
listings = df['merge'].tolist()


def download_img(listings):
    li = listings.split("|")
    img_url = li[4]
    img_name = li[3]
    time.sleep(3)
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
    img_bytes = requests.get(img_url, headers={'User-Agent': user_agent}).content
    
    with open(f"./Download/{img_name}", 'wb') as img_file:
        img_file.write(img_bytes)
        print(f'{img_name} is downloaded !!')

if __name__ == "__main__":            
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(download_img, listings)


# Packages need to be installed. Run the below command:
# pip install pandas, xlrd, requests