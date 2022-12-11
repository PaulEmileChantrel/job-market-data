import streamlit as st
import pandas as pd
from process_data import *
import altair as alt
import matplotlib.pyplot as plt

companies_df,via_df,job_title_df,key_df,work_df,schedule_type_df=process_data('data_analyst_toronto.csv')

st.write("Here's our first attempt at using data to create a table:")



# Companies
companies_df.rename(columns={'company_name':'Company Name'},inplace=True)
st.write(alt.Chart(companies_df).mark_bar().encode(
    x=alt.X('Company Name', sort=None),
    y='counts',))

# Job board
via_df.rename(columns={'via':'Job board'},inplace=True)
st.write(alt.Chart(via_df).mark_bar().encode(
    x=alt.X('Job board', sort=None),
    y='counts',))

# Job title
job_title_df.rename(columns={'title':'Job Title'},inplace=True)
st.write(alt.Chart(job_title_df).mark_bar().encode(
    x=alt.X('Job Title', sort=None),
    y='counts',))


x = st.sidebar.slider('Number of key words shown',min_value=4,max_value=28,value=8)  # 👈 this is a widget

# Key words
key_df = key_df[:x]
key_df['Key Words'] = key_df.index
st.write(alt.Chart(key_df).mark_bar().encode(
    x=alt.X('Key Words', sort=None),
    y='counts',))


# Pie chart for work
work_df['work'] = work_df.index
fig1, ax1 = plt.subplots()

ax1.pie(work_df['counts'], labels=work_df['work'], autopct='%1.1f%%',
        shadow=False, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot(fig1)

# Pie chart for schedule type
schedule_type_df['schedual'] = schedule_type_df.index
fig1, ax1 = plt.subplots()

patches,texts,autotext= ax1.pie(schedule_type_df['counts'], labels=schedule_type_df['schedual'],autopct='%1.1f%%',
        shadow=False, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Move a label
try:
    texts[1]._x +=0.05
    texts[1]._y -= 0.05
    texts[3]._x -=0.05
    texts[3]._y += 0.05
    autotext[1]._y -=0.1
    autotext[3]._y += 0.1
except:
    pass
plt.tight_layout()
st.pyplot(fig1)
