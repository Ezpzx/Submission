import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import os
sns.set(style='dark')


def month_bike_demand(df,user):
    month_bike_df = df.resample(rule='M', on='dteday').agg({
        user: "sum",
    })
    month_bike_df.index = month_bike_df.index.strftime('%B')
    month_bike_df = month_bike_df.reset_index()
    
    return month_bike_df

def hour_bike_demand(df,user):
    bike_hr=df.groupby("hr").agg({
    user:"mean"
    })
    return bike_hr
bike = pd.read_csv("https://raw.githubusercontent.com/Ezpzx/Bike_Sharing/main/Dataset/bike.csv")
bike["dteday"]=pd.to_datetime(bike["dteday"])
min_date = bike["dteday"].min()
max_date = bike["dteday"].max()


with st.sidebar:
    st.header('Bike Sharing Dicoding ')
    st.image("https://raw.githubusercontent.com/Ezpzx/Bike_Sharing/main/Picture/logo.png")
    jenis_user = st.selectbox(
    label="Jenis Pengguna",
    options=('Registered', 'Casual', 'Registered & Casual')
    )
    date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date-pd.DateOffset(years=1)]
    )
jenis_pengguna={
    'Registered': 'registered',
    'Casual': 'casual',
    'Registered & Casual': 'cnt'
}
try:
    start_date, end_date = date
except ValueError:
    st.error("You must pick a start and end date")
    st.stop()
main_df = bike[(bike["dteday"] >= str(start_date)) & 
                (bike["dteday"] <= str(end_date))]

month_resume=month_bike_demand(main_df,jenis_pengguna[jenis_user])
hour_resume=hour_bike_demand(main_df,jenis_pengguna[jenis_user])


st.subheader('Average User by Hour')
coll1, coll2 = st.columns(2)
with coll1:
    mean_hour_user=hour_resume[jenis_pengguna[jenis_user]].max()
    st.metric(f"Maximum Average User:", value=int(mean_hour_user))
with coll2:
    mean_hour_users=hour_resume[jenis_pengguna[jenis_user]].min()
    st.metric(f"Minimum Average User:", value=int(mean_hour_users))
fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(hour_resume.index, hour_resume[jenis_pengguna[jenis_user]], marker='o', linewidth=1, color="#72BCD4")
ax.set_title("Average User Bike Sharing per Hour", loc="center", fontsize=20)
ax.set_xticks(hour_resume.index)
ax.set_xticklabels(hour_resume.index, fontsize=10)
ax.tick_params(axis='both', which='major', labelsize=10)

st.pyplot(fig)

st.subheader('Bike Sharing Users by Month')
col1, col2,col3 = st.columns(3)
 
with col1:
    maximum_user = month_resume[jenis_pengguna[jenis_user]].max()   
    st.metric(f"Maximum {jenis_user} User in Month :", value=maximum_user)
with col2:
    minimum_user = month_resume[jenis_pengguna[jenis_user]].min()   
    st.metric(f"Minimum {jenis_user} User in Month :", value=minimum_user)
with col3:
    mean_user=month_resume[jenis_pengguna[jenis_user]].mean()
    st.metric(f"Average Monthly Users :", value=int(mean_user))
fig, ax = plt.subplots(figsize=(18, 8))
ax.plot(
    month_resume["dteday"],
    month_resume[jenis_pengguna[jenis_user]],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)