import csv
import os


dataPoints = 0
_,_,files = next(os.walk('Lahore'))
FIELD_NAMES = [
        'Plot Area',
        'Name',
        'Number1',
        'Number2',
        'Company Name',
        'Status',
        'Ad Status',
        'Property ID'
    ]

def writeCSV(data, fieldName, file_name):
    fileExists = os.path.isfile(file_name)
    with open(file_name, 'a', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldName, lineterminator='\n')
        if not fileExists:
            writer.writeheader()
        writer.writerow(data)
            
for fName in files:
    uniqueDataLi = []
    with open(f'LahoreWD/{fName}') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for indx,data in enumerate(csv_reader):
            dataWD = f'''{data[1]} | {data[2]} | {data[3]}'''
            if indx != 0 and dataWD not in uniqueDataLi:
                uniqueDataLi.append(dataWD)
                dataDict = {
                    FIELD_NAMES[0]: data[0],
                    FIELD_NAMES[1]: data[1],
                    FIELD_NAMES[2]: data[2],
                    FIELD_NAMES[3]: data[3],
                    FIELD_NAMES[4]: data[4],
                    FIELD_NAMES[5]: data[5],
                    FIELD_NAMES[6]: data[6],
                    FIELD_NAMES[7]: data[7],
                }
                writeCSV(dataDict, FIELD_NAMES, f'''LahoreWD/{fName}''')
    print(f'''{len(uniqueDataLi)} unique values found.''')