import pandas as pd
import os
import csv


#-- Convet csv files into Excel --#

# dataPoints = 0
BASE_DIR = "data/plot1/csvFormat"
_,_,files = next(os.walk(BASE_DIR))
for fName in files:
    df = pd.read_csv(f'{BASE_DIR}/{fName}')
    df.to_excel(f'''data/plot1/excelFormat/{fName.replace("csv","xlsx")}''', index=False, engine="xlsxwriter")
    # df.replace("None","",inplace=True)
    # df.replace("--","",inplace=True)
    # df.replace("(null)","",inplace=True)
    # dataPoints += df.shape[0]
    # print(dataPoints)



#-- Convet csv files into Excel --#

# def writeCSV(data, fieldName, file_name):
#         fileExists = os.path.isfile(file_name)
#         with open(file_name, 'a', encoding='utf-8') as csvfile:
#             writer = csv.DictWriter(csvfile, fieldnames=fieldName, lineterminator='\n')
#             if not fileExists:
#                 writer.writeheader()
#             writer.writerow(data)

# df = pd.read_excel("data/plot1/1_Plots_Raw.xlsx")
# FIELD_NAMES = [
#         'Type',
#         'Area',
#         'Price',
#         'Purpose',
#         'Location',
#         'Added',
#         'Number1',
#         'Number2',
#         'Customer Name',
#         'Company Name',
#         'Ad Status',
#         'Company Status',
#         'Property ID',
#         'Ad Link'
#     ]

# for _,val in df.iterrows():
#     dataDict = {
#         FIELD_NAMES[0]: val['Type'],
#         FIELD_NAMES[1]: val['Area'],
#         FIELD_NAMES[2]: val['Price'],
#         FIELD_NAMES[3]: val['Purpose'],
#         FIELD_NAMES[4]: val['Location'],
#         FIELD_NAMES[5]: val['Added'],
#         FIELD_NAMES[6]: val['Number1'],
#         FIELD_NAMES[7]: val['Number2'],
#         FIELD_NAMES[8]: val['Customer Name'],
#         FIELD_NAMES[9]: val['Company Name'],
#         FIELD_NAMES[10]: val['Ad Status'],
#         FIELD_NAMES[11]: val['Company Status'],
#         FIELD_NAMES[12]: val['Property ID'],
#         FIELD_NAMES[13]: val['Ad Link']
#     }

#     writeCSV(dataDict, FIELD_NAMES, f"data/plot1/csvFormat/{val['City Name']}.csv")