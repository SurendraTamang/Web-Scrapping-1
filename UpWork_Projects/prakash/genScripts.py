import pandas as pd
import os


_, _, files = next(os.walk("./excelData"))

print("##\tUSER INPUT TO GENERATE INDICATION QUERIES\t##")
val11 = int(input("Enter Value 1: "))
val21 = int(input("Enter Value 2: "))
val31 = int(input("Enter Value 3: "))
val61 = int(input("Enter Value 6: "))
print("\n\n##\tUSER INPUT TO GENERATE CONTROL QUERIES\t##")
val12 = int(input("Enter Value 1: "))
val22 = int(input("Enter Value 2: "))
val32 = int(input("Enter Value 3: "))
val62 = int(input("Enter Value 6: "))
val72 = 'null'

def extract_Num(val):
    return int("".join(i for i in val if i.isdigit()))

def writeToFile(li, path):
    qfile = open(path,"w",encoding='utf-8')
    qfile.write("\n".join(li)) 
    qfile.close() 

for file in files:
    df = pd.read_csv(f"./excelData/{file}")
    queryLi1 = ["insert all",]
    queryLi2 = ["insert all",]
    for _,val in df.iterrows():
        val41=''
        if pd.notnull(val['ind_nv_prgm']):
            val41 = extract_Num(val['ind_nv_prgm'])
        val51 = val['ind_ind']

        val42 = ''
        if pd.notnull(val['ctr_nv_prgm']):
            if pd.notnull(val42):
                val42 = extract_Num(val['ctr_nv_prgm'])
        val52 = val['ctr_ctr']

        if val41 and val51:
            query1 = f'''\tinto tdms.DVC_CODE_STATION_I_BIT (project_id,project_version,code_station_id,bit_position,bit_mnemonic,active_high,indication_bit_id) values ({val11}, {val21}, {val31}, {val41}, '{val51}', {val61}, )'''
            queryLi1.append(query1)

        if val42 and val52:
            query2 = f'''\tinto tdms.dvc_code_station_c_bit (project_id,project_version,code_station_id,bit_position,bit_mnemonic,active_high,control_boolean_equation,control_bit_id) values ({val12}, {val22}, {val32}, {val42}, '{val52}', {val62}, {val72}, )'''
            queryLi2.append(query2)
    
    queryLi1.append("select 1 from dual;")
    queryLi2.append("select 1 from dual;")

    writeToFile(queryLi1, f'''./indicationQueries/{file.replace("csv","txt")}''')
    print(f'''INDICATION QUERIES GENERATED SUCCESSFULLY! => ./indicationQueries/{file.replace("csv","txt")}''')
    writeToFile(queryLi2, f'''./controlQueries/{file.replace("csv","txt")}''')
    print(f'''CONTROL QUERIES GENERATED SUCCESSFULLY! => ./controlQueries/{file.replace("csv","txt")}''')
    