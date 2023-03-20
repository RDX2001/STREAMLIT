import streamlit as st
import pandas as pd
#import numpy as np
#pip install matplotlib
import matplotlib.pyplot as plt
import logging
#import seaborn as sns


logging.basicConfig(filename="log.txt", level=logging.DEBUG, format="%(asctime)s %(message)s")
logging.debug("Debug logging test...")
st.set_page_config(layout = 'wide',page_title = 'Startup Analysis')


df = pd.read_csv('startup_cleaned_2.csv')
df['date'] = pd.to_datetime(df['date'],errors = 'coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year 


def load_general_analysis():
    st.title('General Analysis')
    #total invested amt
    total = round(df['amount'].sum())
    
    #max amt infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending = False).head(1).values[0]

    mean_funding = df.groupby('startup')['amount'].sum().mean()

    total_funded_stups = round(df['startup'].nunique())
      
    col1,col2,col3,col4 = st.columns(4) 
    with col1: 
         st.metric('Total',str(total) +'Cr')
    with col2:  
         st.metric('Max Funding',str(max_funding)+'Cr')
    with col3:
         st.metric('Average Funding',str(round(mean_funding))+'Cr')
    with col4:
        st.metric('Total Funded Startups',str(total_funded_stups))

    st.header('MoM Graph')
    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year','month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year','month'])['amount'].count().reset_index()    
    #temp_df = df.groupby(['year','month'])['amount'].sum().reset_index()
    temp_df['x_axis']=temp_df['month'].astype(str)+ "_"+ temp_df['year'].astype(str)

    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'],temp_df['amount'])
    st.pyplot(fig3)
    



    



def load_investor_details(investor):
    st.title(investor)
    #load recent 5 investment

    last5_df = df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','round']]

    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)
    #biggest investments
    col1, col2 = st.columns(2)
    with col1:
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head(10)

        st.subheader('Biggest Investments')
        st.dataframe(big_series)
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)

        df['year'] = df['date'].dt.year
        big_series1= df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
        st.subheader('Yearwise Investment( In Cr Rupees)')
        #st.dataframe(big_series1)
        fig2, ax2 = plt.subplots()
        ax2.plot(big_series1.index,big_series1.values)
        st.pyplot(fig2)


    with col2:
        try:
            vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
            st.subheader('Sectors Invested In')
            fig, ax = plt.subplots()
            ax.pie(vertical_series, labels=vertical_series.index, autopct='%1.1f%%')
            st.pyplot(fig)
        except Exception as e:
            logging.debug(e)
            st.write('Data Insufficient')
          
        try:
            vertical_series1 = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
            st.subheader('Types Of Investments')
            fig, ax = plt.subplots()
            ax.pie(vertical_series1, labels=vertical_series1.index, autopct='%1.1f%%')
            st.pyplot(fig)
        except Exception as e:
            logging.debug(e)
            st.write('Data Insufficient') 

        try:
            vertical_series2 = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
            st.subheader('Investments in Cities')
            fig, ax = plt.subplots()
            ax.pie(vertical_series2, labels=vertical_series2.index, autopct='%1.1f%%')
            st.pyplot(fig)
        except Exception as e:
            logging.debug(e)
            st.write('Data Insufficient')       
           

              
st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

if option == 'Overall Analysis':
    #st.title('General Analysis')
    #btn0 = st.sidebar.button('Show General Analysis')
    #if btn0:
    load_general_analysis()
 
    
elif option == 'Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['name'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')

    st.title('Startup Analysis')
else:
    selected_investor = st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))

    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)

    #st.title('Investor Analysis')
