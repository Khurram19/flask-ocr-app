from msilib.schema import Error
import sqlite3
import csv
import numpy as np
import pandas as pd
from typing import final
from paddleocr import PaddleOCR,draw_ocr
ocr = PaddleOCR(use_angle_cls=True, lang='en') 

def contains_number(string):
    return any(char.isdigit() for char in string)

def db_store(img_path, results):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect('./ocr_database.db')
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS ocr (file_path VARCHAR, search_results VARCHAR)')
        conn.commit()
    except Error as e:
        print(e)
    
    try:
        cur.execute(f'INSERT INTO ocr (file_path, search_results) values ("{img_path}", "{results}")')
        conn.commit()
    except Error as e:
        print(e)

    conn.close()
    return conn


def get_data(img_path, results):
    """select row from database and return in csv

    """
    conn = None
    try:
        conn = sqlite3.connect('./ocr_database.db')
        cur = conn.cursor()
    except Error as e:
        print(e)

    try:
        cur.execute(f'SELECT * FROM ocr WHERE file_path="{img_path}" and search_results="{results}"')
        rows = cur.fetchall()
        conn.commit()
        # print(rows)
        # df = pd.read_sql_query(f'SELECT * FROM ocr WHERE file_path="{img_path}" and search_results="{results}"', conn)
        # df.to_csv(r'./data.csv')
        

        with open('./data.csv', 'w', newline='') as f_handle:
            writer = csv.writer(f_handle)
            # Add the header/column names
            header = ['file_path', 'search_results']
            writer.writerow(header)
            # Iterate over `data`  and  write to the csv file
            for row in rows:
                writer.writerow(row)




    except Error as e:
        print(e)

    conn.close()
    return conn

def ocr_and_store(img_path, search):
    # print(img_path)
    final_results = []
    complete_results =[]
    result = ocr.ocr(img_path, cls=True)
    print(result)

    for line in result:
        # print(line[1][0])
        results=""
        complete_results.append(line[1][0])
        if search.lower() in line[1][0].lower() and contains_number(line[1][0]):
            results = line[1][0]
            final_results.append(line[1][0])
        else:
            pass
    # print(final_results)
    db_store(img_path, final_results)
    get_data(img_path, final_results)
    return final_results, complete_results


