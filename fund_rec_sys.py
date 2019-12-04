#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 14:29:05 2019

@author: johnrick
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity



@st.cache
def df_pickle(file):
    return pickle.load(open(file, 'rb'))


@st.cache
def df_pickle2(file):
    return pickle.load(open(file, 'rb'))




df= df_pickle('df_final_final.pkl')


df2 = df_pickle2('df_streamlit.pkl')

@st.cache
def load_matrix():
    return np.load('cosine_sim.npy')

similarity_matrix_full2 = load_matrix()


#load model()

def main():
    
    
    st.sidebar.title("What do you want to do?")
    app_mode = st.sidebar.selectbox("Choose the mode", ["Model and Data", "Best Image Transformation","From Real to Fake","Color Your Own Image","justin suck","Run Fund Recommendation"])

    if app_mode == "Run Fund Recommendation":
        with st.spinner('Gathering the data...'):
            st.title("Coloring Images with a Generative Adversarial Network")
            st.markdown("Welcome to my black and white to color image generator! Let me introduce you to the model and data")
            run_rec()


    elif app_mode == "Best Image Transformation":
        with st.spinner("Showing you the Best..."):
            st.title("The best results so far")
    
    elif app_mode == "From Real to Fake":
        with st.spinner("Merging Photos..."):
            st.title("Seeing images transform from real to fake")
            st.slider("Percentage of real and fake", 0.0, .99, (0.0))
            st.radio('What image do you want to look at', ['Girls in Flowers','Dog','Coast'])
     
    elif app_mode == "Color Your Own Image":
        with st.spinner("Coloring..."):
            st.title("Pick any image and lets color it in!")
            st.text_input('Put Image URL Here', 'Type Here')

    elif app_mode == "justin suck":
        with st.spinner("Coloring..."):
            st.title("Pick any image and lets color it in!")
            st.text_input('Put Image URL Here', 'Type Here')
                
def run_rec():
    indices = pd.Series(df.index)
    
    #st.dataframe(df.head())
    #st.dataframe(df2.head())
    choice = st.radio('How would you like to search?', ('By Name','By Ticker'))
    if choice == 'By Ticker':
        name = st.selectbox('Give a ticker for a fund you own',df.index)
    elif choice == 'By Name':
        family = st.selectbox('Fund Name', df2['fund_family'].unique())
        asset = st.selectbox('Pick Asset Class',df2.loc[df2['fund_family'] == family]['broad_asset class'].unique())
        name_1= st.selectbox('Pick Ticker',df2.loc[(df2['fund_family'] == family) & (df2['broad_asset class'] == asset)].fund_name)

        name = df2[df2['fund_name'] == name_1].index.values[0]


    
    def recommendations_holdings_full(similarity_matrix_full2 = similarity_matrix_full2):
        recommended_funds = []
        
        # gettin the index of the hotel that matches the name

        idx = indices[indices == name].index[0]

        
        # creating a Series with the similarity scores in descending order
        score_series = pd.Series(similarity_matrix_full2[idx]).sort_values(ascending = False)
    
        # getting the indexes of the 10 most similar hotels except itself
        top_100_indexes = list(score_series.iloc[1:10].index)
        
        # populating the list with the names of the top 10 matching hotels
        for i in top_100_indexes:
            recommended_funds.append(list(df.index)[i])
            
        return recommended_funds
    if choice == 'By Name':
        answer = recommendations_holdings_full()
    elif choice =='By Ticker':
        answer = recommendations_holdings_full()
        
    
    #answer = recommendations_holdings_full()
    #st.write(answer)
    st.table(df2.loc[name][['fund_name','broad_asset class','risk_monthly_VAR','30_day_sec_yield_real','total_return_3y','expense_ratio','risk_total','risk_score_risky_bonds','risk_score_PE_expensive']].transpose())
    
    
    st.table(df2.loc[answer][['fund_name','broad_asset class','risk_monthly_VAR','30_day_sec_yield_real','total_return_3y','expense_ratio','risk_total','risk_score_risky_bonds','risk_score_PE_expensive']])
    #st.write((df2.head()))
    




if __name__ == "__main__":
    main()
