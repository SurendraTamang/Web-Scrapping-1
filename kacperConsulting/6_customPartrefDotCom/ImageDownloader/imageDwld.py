import pandas as pd
import os
import requests


pa_df = pd.read_excel("./prodAttr.xlsx", sheet_name="data")
ip_df = pd.read_excel("./prodAttr.xlsx", sheet_name="inp")
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"

def imgDownloader(img_url, path):
    try:
        img_bytes = requests.get(img_url, headers={'User-Agent': USER_AGENT}).content
        
        with open(path, 'wb') as img_file:
            img_file.write(img_bytes)
            print(f'{path} is downloaded !!')
    except:
        pass


for _,val1 in pa_df.iterrows():
    imgNameList = []
    for _,val2 in ip_df.iterrows():
        if str(val1['interchange value']) == str(val2['Interchange']):
            imgNameList.append(val2['Part Number to label images'])
    # print(f"{val1['interchange value']} - {imgNameList}")
    for name in imgNameList:

        #   CODE SNIPPET TO DOWNLOAD PARTS IMAGE    #
        if val1['Part Image Url'] != "BLANKS":
            partImgLi = val1['Part Image Url'].split(",")
            for partImg in partImgLi:
                if os.path.exists(f"./images/{name}"):
                    _, _, files = next(os.walk(f"./images/{name}"))
                    cntr1 = 0
                    for file in files:
                        if file.startswith(name) and not file.startswith(f"{name}_Plug"):
                                cntr1 += 1
                    if cntr1 == 0:
                        imgDownloader(partImg, f"./images/{name}/{name}_001.jpg")
                    elif cntr1 > 0 and cntr1 < 9:
                        imgDownloader(partImg, f"./images/{name}/{name}_00{cntr1+1}.jpg")
                    elif cntr1 > 8 and cntr1 < 99:
                        imgDownloader(partImg, f"./images/{name}/{name}_0{cntr1+1}.jpg")
                    else:
                        imgDownloader(partImg, f"./images/{name}/{name}_{cntr1+1}.jpg")                    
                else:
                    os.mkdir(f"./images/{name}")
                    imgDownloader(partImg, f"./images/{name}/{name}_001.jpg")
        #   CODE SNIPPET TO DOWNLOAD PARTS IMAGE ENDS    #

        #   CODE SNIPPET TO DOWNLOAD PLUG IMAGE    #
        if val1['Plug Image Url'] != "BLANKS":
            plugImgLi = val1['Plug Image Url'].split(",")
            for plugImg in plugImgLi:
                if os.path.exists(f"./images/{name}"):
                    _, _, files = next(os.walk(f"./images/{name}"))
                    cntr2 = 0
                    for file in files:
                        if file.startswith(f"{name}_Plug"):
                                cntr2 += 1
                    if cntr2 == 0:
                        imgDownloader(plugImg, f"./images/{name}/{name}_Plug.jpg")
                    elif cntr2 > 0 and cntr2 < 9:
                        imgDownloader(plugImg, f"./images/{name}/{name}_Plug_{cntr2+1}.jpg")
                    elif cntr2 > 8 and cntr2 < 99:
                        imgDownloader(plugImg, f"./images/{name}/{name}_Plug_{cntr2+1}.jpg")
                    else:
                        imgDownloader(plugImg, f"./images/{name}/{name}_Plug_{cntr2+1}.jpg")
                else:
                    os.mkdir(f"./images/{name}")
                    imgDownloader(plugImg, f"./images/{name}/{name}_Plug.jpg")
        #   CODE SNIPPET TO DOWNLOAD PLUG IMAGE ENDS    #