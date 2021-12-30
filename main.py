import sqlite3 as sq
import time as t
import pandas as pd
import streamlit as st
import os.path
from pathlib import Path


st.set_page_config(
    page_title="Financial Planning Calculator")

select_data = st.selectbox('Select Data', ('סניף דאלי ראשי', 'סניף דאלי (כרכור)',
                                           'סניף דאלי(שלישי)'))


st.header(select_data)



def create_data_and_extract():
    data_to_df = []

    sql_data = Path(str(select_data) + '.db')
    conn = sq.connect(sql_data)
    cur = conn.cursor()

    st.title(" ! מערכת חישוב נתונים כספיים")

    insert_date, supplier_name, total_pay = st.columns(3)

    with insert_date:
        insert_date = st.date_input(' הכנס תאריך ', value=None, min_value=None, max_value=None, key=None, help=None,
                                    on_change=None, args=None, kwargs=None)

    with supplier_name:
        supplier_name = st.text_input(" הכנס שם ספק ")

    with total_pay:
        total_pay = st.number_input('הכנס סה"כ לתשלום')

    st.header("** הוצאות חודשיות **")
    st.subheader("חישוב")
    first_pay, second_pay, third_pay = st.columns(3)

    with first_pay:
        first_pay = st.number_input("(₪) הכנס תשלום ראשון ", min_value=0.0, format='%f')

    with second_pay:
        second_pay = st.number_input("(₪) הכנס תשלום שני ", min_value=0.0, format='%f')

    with third_pay:
        third_pay = st.number_input("(₪) הכנס תשלום שלישי ", min_value=0.0, format='%f')

    sums = sum([first_pay, second_pay, third_pay])

    sum_of_total_pay = total_pay - sums

    average = sums / 3

    data_to_df.append({'date': str(insert_date), 'supplier': str(supplier_name), 'first_pay': str(first_pay),
                       'second_pay': str(second_pay), 'third_pay': str(third_pay), 'sum': str(sums),
                       'avg': str(average),
                       'total_pay': str(sum_of_total_pay)})

    df = pd.DataFrame(data_to_df, columns=['date', 'supplier', 'first_pay', 'second_pay', 'third_pay',
                                           'sum', 'avg', 'total_pay'])

    if st.button('לחץ בשביל לשמור מידע ', key=None, help=None, on_click=None):
        if os.path.isfile(sql_data):
            pass
        else:
            cur.execute(
                "CREATE TABLE suppliers (date, supplier, first_pay, second_pay, third_pay, sum, avg, total_pay)")

        conn.commit()
        df.to_sql('suppliers', conn, if_exists='append', index=False)

        dr = pd.read_sql_query("SELECT * FROM suppliers", conn)
        st.dataframe(dr)

        dr.to_csv(str(select_data) + '.csv')

        conn.close()


    try:
        with open(str(select_data) + '.csv') as f:
            st.download_button('הורד בתור קובץ אקסל', f, file_name=str(select_data) + '.csv')
    except Exception as e:
        print(e)



if select_data == 'סניף דאלי ראשי':
    create_data_and_extract()

elif select_data == 'סניף דאלי(כרכור)':
    create_data_and_extract()

elif select_data == 'סניף דאלי(שלישי)':
    create_data_and_extract()