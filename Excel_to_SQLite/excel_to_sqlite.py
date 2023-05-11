from xlsxwriter.workbook import Workbook
import pandas as pd
import os
import sqlite3
import glob

script_path = os.path.realpath(os.path.dirname(__file__)) + "/"
sqlite_path = script_path + "sqlite_files/"

if not os.path.isdir(sqlite_path):
   os.makedirs(sqlite_path)

excel_files = []

print("\nSearching for .xlsx files in directory:")
print(script_path)

print("\nFound:")
for root, dir, files in os.walk(script_path):
    for file in files:
        name = os.path.join(root, file)
        filename, file_extension = os.path.splitext(name)
        if (file_extension == '.xlsx'):
            print(os.path.basename(name))
            excel_files.append(name)

for filename in excel_files:
    target = sqlite_path + os.path.basename(filename).strip(".xlsx") + ".sqlite"

    # This is important as otherwise the excel files will conflict with temp sqlites
    if os.path.exists(target):
        os.remove(target)

    con = sqlite3.connect(target)
    wb = pd.read_excel(filename,sheet_name = None)

    for sheet in wb:
        wb[sheet].to_sql(sheet,con,if_exists='append',index=False,schema=script_path + 'temoa_schema.sqlite')

    con.commit()
    con.close()