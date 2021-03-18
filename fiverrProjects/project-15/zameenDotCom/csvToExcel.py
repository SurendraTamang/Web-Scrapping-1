import pandas as pd
import os


dataPoints = 0
_,_,files = next(os.walk('Lahore'))
for fName in files:
    df = pd.read_csv(f'Lahore/{fName}')
    df.replace("None","",inplace=True)
    df.replace("--","",inplace=True)
    df.replace("(null)","",inplace=True)
    dataPoints += df.shape[0]
    df.to_excel(f'''{fName.replace("csv","xlsx")}''', index=False, engine="xlsxwriter")
    print(dataPoints)