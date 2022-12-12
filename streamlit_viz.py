import streamlit as st
import pandas as pd
from process_data import *
import altair as alt
import matplotlib.pyplot as plt

# Page settings
st.set_page_config(page_title='Job Market',page_icon=":bar_chart:",layout="wide")

# Loading the dataframe file
df = pd.read_csv('data_analyst_toronto.csv')
print(df.shape[0])

#df = preformat(df)


# -- SIDEBARS --#
st.sidebar.header("Please filter here :")

work_types = st.sidebar.multiselect(
    "Select a type of work:",
    options = df['work_type'].unique(),
    default = df['work_type'].unique()
)
n1 = st.sidebar.slider('Number of companies',min_value=4,max_value=28,value=8)  # 👈 this is a widget
n2 = st.sidebar.slider('Number of job board',min_value=4,max_value=18,value=8)  # 👈 this is a widget
n3 = st.sidebar.slider('Number of job titles',min_value=4,max_value=28,value=8)  # 👈 this is a widget
x = st.sidebar.slider('Number of key words shown',min_value=4,max_value=28,value=8)  # 👈 this is a widget

df_selection = df.query(
    "work_type == @work_types"
)
df_selection.reset_index(drop=True,inplace=True)




# Loading all the df
companies_df,via_df,job_title_df,key_df,work_df,schedule_type_df=process_data(df_selection)
companies_df = companies_df[:n1]
via_df = via_df[:n2]
job_title_df = job_title_df[:n3]

## -- Page --
st.title(':bar_chart: Job Market for Data Analyst in Toronto')
st.markdown("##")


number_of_jobs = df_selection.shape[0]

left,right = st.columns(2)
with left:
    st.subheader(f'Total jobs found : {number_of_jobs}jobs')

st.markdown('---')


left,right = st.columns(2)
# Companies
companies_df.rename(columns={'company_name':'Company Name'},inplace=True)
with left :
    st.write('Hiring Companies')
    st.altair_chart(alt.Chart(companies_df).mark_bar().encode(
        x=alt.X('Company Name', sort=None),
        y='counts',).properties(height=400),use_container_width=True)

# Job board
via_df.rename(columns={'via':'Job board'},inplace=True)
with right :
    st.write('Best Job boards')
    st.altair_chart(alt.Chart(via_df).mark_bar().encode(
        x=alt.X('Job board', sort=None),
        y='counts',).properties(height=400),use_container_width=True)

left,right = st.columns(2)
with left :
    # Job title
    st.write('Job Titles')
    job_title_df.rename(columns={'title':'Job Title'},inplace=True)
    st.altair_chart(alt.Chart(job_title_df).mark_bar().encode(
        x=alt.X('Job Title', sort=None),
        y='counts',).properties(height=500),use_container_width=True)



# Key words
key_df = key_df[:x]
key_df['Key Words'] = key_df.index
with right :
    st.write('Most Commun Key Words')
    st.altair_chart(alt.Chart(key_df).mark_bar().encode(
        x=alt.X('Key Words', sort=None),
        y='counts',).properties(height=400),use_container_width=True)


# Pie chart for work
left,right = st.columns(2)
fig1, ax1 = plt.subplots()
fig1.set_facecolor('#00172b')
patches,texts,autotext= ax1.pie(work_df['counts'], labels=work_df['work_type'], autopct='%1.1f%%',
        shadow=False, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
for text in texts:
    text.set_color('white')
with left:
    st.write('Types of work')
    st.pyplot(fig1)

# Pie chart for schedule type
schedule_type_df['schedual'] = schedule_type_df.index
fig1, ax1 = plt.subplots()
fig1.set_facecolor('#00172b')
patches,texts,autotexts= ax1.pie(schedule_type_df['counts'], labels=schedule_type_df['schedual'],autopct='%1.1f%%',
        shadow=False, startangle=90)
for text in texts:
    text.set_color('white')


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
with right:
    st.write('Types of contracts')
    st.pyplot(fig1)



### hide elements
hide_st_style = """
    <style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}
    </style>
"""

st.markdown(hide_st_style,unsafe_allow_html=True)
