from xlsxwriter.workbook import Workbook
import sqlite3
import os

script_path = os.path.realpath(os.path.dirname(__file__))

workbook = Workbook(script_path + '/temoa_schema.xlsx')

conn = sqlite3.connect(script_path + '/temoa_schema.sqlite')
cur = conn.cursor()
cur.execute("""SELECT name FROM sqlite_master WHERE type='table';""")

all_tables = [table[0] for table in cur.fetchall()]

tables = []
for table in all_tables:
    if not table.startswith('Output'):
      tables.append(table)

tables.sort()
for table in tables:
    
    rows = cur.execute("SELECT * FROM " + table)

    worksheet = workbook.add_worksheet(name=table[0:31])

    headers = []

    for column_number, desc in enumerate(rows.description): # row is a tuple here
        # try: worksheet.write(0, column_number, desc[0]) # Write the cell in the current sheet
        # except:pass
        headers.append({"header": desc[0]})

    headers.append({"header": "reference"})
    headers.append({"header": "additional notes"})

    worksheet.add_table(0,0,100,len(headers)-1,{"columns": headers})
    worksheet.set_column(0,len(headers)-3,20)
    worksheet.set_column(len(headers)-2,len(headers)-1,60)

workbook.close()