from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables
import pandas as pd

import streamlit as st
import os
import sqlite3
import numpy as np

import google.generativeai as genai
## Configure Genai Key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Fucntion To retrieve query from the database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    column_names = [description[0] for description in cur.description]  # Fetch column names
    conn.commit()
    conn.close()
    return column_names, rows

## Define Your Prompt
prompt=["""
    You are an expert in converting English questions to SQL query!
    The SQL database has the name covid19 and has the following columns - ObservationDate, State, 
    Region, LastUpdate,Confirmed,Deaths,Recovered
    \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM covid19 ;
    \nExample 2 - Tell me all the different State?, 
    the SQL command will be something like this SELECT State FROM covid19; 
    \nExample 3 - Tell me all the total Deaths?, 
    the SQL command will be something like this SELECT COUNT(Deaths) FROM covid19;
    also the sql code should not have ``` in beginning or end and sql word in output,
    also the sql code should not have , in end and sql word in output
    """]

## Using Streamlit App for Frontend

st.set_page_config(page_title="Pass Any SQL query")
st.header("Covid19 Application")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    # aa = [("ObservationDate",0), ("State",1), ("Region",2),( "LastUpdate",3), ("Confirmed",4), ("Deaths",5), ("Recovered",6)]
    print(response)
    try:
        column_names, data = read_sql_query(response,"covid19.db")
        st.subheader("The Response is")
        # Displaying the columns
        if data:  # Checking if data is not empty
            st.write("Columns:", ", ".join(column_names))
            df = pd.DataFrame(data, columns=column_names)
            st.dataframe(df)
            # Choose the appropriate chart type based on data characteristics
            if any(df.select_dtypes(include=[np.number])):
                if df.shape[1] == 1:  
                    st.bar_chart(df)
                elif df.shape[1] == 2: 
                    x_axis = st.selectbox("Select X Axis", options=df.columns.tolist())
                    y_axis = st.selectbox("Select Y Axis", options=df.columns.tolist(), index=1)
                    st.line_chart(df, x=x_axis, y=y_axis)
                else: 
                    st.line_chart(df)
            else:
                st.warning("Data is not suitable for numerical charts.")
        else:
            st.warning("No data retrieved from the database.")

    except Exception as e:
        st.error(f"Error retrieving data: {e}")
else:
    # Handle cases where no data is retrieved (e.g., empty query result)
    st.warning("No data retrieved from the database.")