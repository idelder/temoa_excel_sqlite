import sqlite3
import os
import excel_to_sqlite
import shutil

excel_to_sqlite

script_path = os.path.realpath(os.path.dirname(__file__)) + "/"
schema_name = script_path + "temoa_schema.sqlite"
merged_name = script_path + "merged.sqlite"

src_file = schema_name
shutil.copy(src_file,merged_name)


con = sqlite3.connect(merged_name)
curs = con.cursor()

def merge_database(db):
    con.execute("ATTACH '" + db +  "' as dba")

    con.execute("BEGIN")

    master_tables = [table[1] for table in con.execute("SELECT * FROM sqlite_master WHERE type='table'")]
    tables = [table[1] for table in con.execute("SELECT * FROM dba.sqlite_master WHERE type='table'")]

    for t in tables:

        if (t not in master_tables):
            print(f"Table {t} not in target database and so was ignored.")
            continue

        master_columns = [d[0] for d in con.execute(f"SELECT * FROM {t} WHERE 1=0;").description]
        columns = [d[0] for d in con.execute(f"SELECT * FROM dba.{t} WHERE 1=0;").description]
        
        for col in columns:
            if (col not in master_columns):
                sql = con.execute(f"ALTER TABLE dba.{t} DROP COLUMN '{col}'")
                print(f"Column {col} not in target table {t} and so was ignored.")

        combine = f"INSERT OR IGNORE INTO {t} SELECT * FROM dba.{t}"
        con.execute(combine)

    con.commit()
    con.execute("DETACH DATABASE dba")


def read_files(directory):
    fname = []
    for root,d_names,f_names in os.walk(directory):
        for f in f_names:
            c_name = os.path.join(root, f)
            filename, file_extension = os.path.splitext(c_name)
            if (file_extension == '.sqlite'):
                fname.append(c_name)

    return fname


def batch_merge(directory):
    print("\nMerging into:")
    print(merged_name)
    db_files = read_files(directory)
    for db_file in db_files:
        filename = os.path.basename(db_file)
        if (db_file != merged_name) & (db_file != schema_name):
            print("Merging " + filename)
            merge_database(db_file)


batch_merge(script_path)

con.close()