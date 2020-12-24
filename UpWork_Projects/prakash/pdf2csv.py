import camelot
import pandas as pd
import os
import csv


def writeCSV(fileName, dict_data, fieldName):
    file_exists = os.path.isfile(fileName)
    with open(fileName, 'a', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldName, lineterminator='\n')
        if not file_exists:
            writer.writeheader()
        for data in dict_data:
            writer.writerow(data)

def fillBlanks(val, cName):
    if val:
        return val
    else:
        if cName:
            return ""
        else:
            return "BLANK"


for fName in os.listdir("./pdfData"):
    if fName.endswith(".pdf"):
        try:
            print(f'''EXTRACTING {fName} TO {fName.replace("pdf","csv")}''')
            tables = camelot.read_pdf(f'''./pdfData/{fName}''', flavor='lattice', strip_text=' .\n')

            df1 = tables[0].df
            df2 = pd.DataFrame()
            df2 = df1[[2,3,4,5,6,7]]
            df2.drop([0,1,2,3], inplace=True)
            df2.columns = ["ctr_nv_prgm","ctr_ofc","ctr_ctr","ind_nv_prgm","ind_ofc","ind_ind"]
            df3 = df1[[8,9,10]]
            df3.drop([0,1,2,3], inplace=True)
            df3.columns = ["ind_nv_prgm","ind_ofc","ind_ind"]

            for _,val in df2.iterrows():
                dataList = []
                if val['ctr_nv_prgm'] and val['ctr_nv_prgm'] != "CONTROLS" and val['ctr_nv_prgm'] != "NVPRGM":
                    dataList.append(
                        {
                            'ctr_nv_prgm':fillBlanks(val['ctr_nv_prgm'], "ctr"),
                            'ctr_ofc':fillBlanks(val['ctr_ofc'], "ctr"),
                            'ctr_ctr':fillBlanks(val['ctr_ctr'], None),
                            'ind_nv_prgm':fillBlanks(val['ind_nv_prgm'], "ind"),
                            'ind_ofc':fillBlanks(val['ind_ofc'], "ind"),
                            'ind_ind':fillBlanks(val['ind_ind'], None),
                        }
                    )
                    writeCSV(f'''./excelData/{fName.replace("pdf","csv")}''', dataList, ["ctr_nv_prgm","ctr_ofc","ctr_ctr","ind_nv_prgm","ind_ofc","ind_ind"])

            for _,val in df3.iterrows():
                dataList = []
                if val['ind_nv_prgm'] and val['ind_nv_prgm'].startswith("I00"):
                    dataList.append(
                        {
                            'ctr_nv_prgm':"",
                            'ctr_ofc':"",
                            'ctr_ctr':"",
                            'ind_nv_prgm':fillBlanks(val['ind_nv_prgm'], "ind"),
                            'ind_ofc':fillBlanks(val['ind_ofc'], "ind"),
                            'ind_ind':fillBlanks(val['ind_ind'], None),
                        }
                    )
                    writeCSV(f'''./excelData/{fName.replace("pdf","csv")}''', dataList, ["ctr_nv_prgm","ctr_ofc","ctr_ctr","ind_nv_prgm","ind_ofc","ind_ind"])
            print(f'''EXTRACTING SUCCESSFUL...!!!''')
        except:
            print(f'''EXTRACTING FAILED...!!!''')