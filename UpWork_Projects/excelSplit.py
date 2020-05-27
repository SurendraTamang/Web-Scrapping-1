import pandas as pd


file_path = input("Enter the excel file path: ")
no_of_rows = int(input("Enter the no. of rows per excel: "))
header_copy = input("Do you want to copy headers into all the sheets? yes/no : ")

#df = pd.read_excel("D:/sipun/List1-MasterSheet.xlsx")
df = pd.read_excel(file_path)
start_position = 0
end_position = no_of_rows
#df = pd.read_excel("D:/sipun/test1.xlsx", header=None, skiprows=1)
df_columnNames = df[0:0]
df_rows = df.shape[0]
no_of_files = df_rows//no_of_rows

if df_rows%no_of_rows != 0:
    remaining = df_rows-(no_of_files*no_of_rows)
    for i in range(1,no_of_files+1):
        end_position += no_of_rows
        df_split_data = df[start_position:end_position]
        if header_copy.lower()=="yes" and i != 1:
            frames = [df_columnNames, df_split_data]
            result = pd.concat(frames)
        elif i==1:
            frames = [df_columnNames, df_split_data]
            result = pd.concat(frames)
        else:
            result = df_split_data
        start_position += no_of_rows
        result.to_excel(f"output_{i}.xlsx", index=False)
    end_position += remaining
    df_split_data = df[start_position:end_position]
    result = df_split_data
    start_position += no_of_rows
    result.to_excel(f"output_{i+1}.xlsx", index=False)
else:
    for i in range(1,no_of_files+1):
        result = pd.DataFrame()
        # end_position += (no_of_rows-1)
        df_split_data = df[start_position:end_position]
        if header_copy.lower()=="yes":
            frames = [df_columnNames, df_split_data]
            result = pd.concat(frames)
            result.to_excel(f"output_{i}.xlsx", index=False)
        elif header_copy.lower()=="no" and i==1:
            frames = [df_columnNames, df_split_data]
            result = pd.concat(frames)
            result.to_excel(f"output_{i}.xlsx", index=False)
        else:
            result = df_split_data
            result.to_excel(f"output_{i}.xlsx", index=False, header=False)
        start_position += end_position-1
        end_position += no_of_rows+1
        # print(result.head(10))
        # print("______________________\n")
        #result.to_excel(f"output_{i}.xlsx", index=False)


# pip instll openpyxl, xlrd, pandas
