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
from PIL import Image


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


def read_img(file, size = (256,256)):
    '''
    reads the images and transforms them to the desired size
    '''
    img = Image.open(file)
    
    return st.image(img,width=750)


def data_model():
    
    read_img("mutual_fund_example.png")
    st.text("Investment funds make investing easier. You don't have to choose the best bonds or stocks, but you can get a basket of them in one fund.")
    
    
    
    read_img("feature_importance2.png")
    st.text("The top 22 features that help predict the Value At Risk.")
    
    read_img('random_forest_n_estimators.png')
    st.text("Optimizing number of estimators to get highest accuracy score.")

#load model()

def main():
    
    
    st.sidebar.title("What do you want to do?")
    app_mode = st.sidebar.selectbox("Choose the mode", ["Model and Data", "Choose By Features","Run Fund Recommendation"])

    if app_mode == "Run Fund Recommendation":
        with st.spinner('Loading Fund Information'):
            st.title("Picking Investments Doesn't Have To Be Hard")
            st.markdown("With Over 10,000 mutual funds and multiple share classes, choosing the perfect fund can be exhausting, here's another way.")
            run_rec()


    elif app_mode == "Model and Data":
        with st.spinner("How hard can it be?"):
            st.title("Model and Data")
            st.markdown("18,000 Funds and 36 Different Features")
            data_model()
    
    elif app_mode == "Choose By Features":
        with st.spinner("Loading the Learning Machine..."):
            st.title("What Matters To You?")
            slide_c = st.slider("Fee", 0.0, .99, (.5))
            #st.radio('What image do you want to look at', ['Girls in Flowers','Dog','Coast'])
            run_rec2(slide_c)
     
    elif app_mode == "Color Your Own Image":
        with st.spinner("Coloring..."):
            st.title("Pick any image and lets color it in!")
            st.text_input('Put Image URL Here', 'Type Here')

    elif app_mode == "justin suck":
        with st.spinner("Coloring..."):
            st.title("Pick any image and lets color it in!")
            st.text_input('Put Image URL Here', 'Type Here')
              
            
def run_rec2(slide):
    indices = pd.Series(df.index)
    
    #st.dataframe(df.head())
    #st.dataframe(df2.head())
    
    
    #percentage to filter funds that are lower than slide_c
    if any(df2["expense_ratio"] <= slide):
        asset1 = st.selectbox('Pick Asset Class', sorted(df2.loc[df2['expense_ratio'] <= slide]['broad_asset class'].unique()))
        name_1= st.selectbox('Pick Funds', sorted(df2.loc[(df2['broad_asset class'] == asset1) & (df2['expense_ratio'] <= slide)].fund_name))
        name = df2[df2['fund_name'] == name_1].index.values[0]


    
    def recommendations_holdings_full(similarity_matrix_full2 = similarity_matrix_full2):
        recommended_funds = []
        
        # gettin the index of the hotel that matches the name

        idx = indices[indices == name].index[0]

        
        # creating a Series with the similarity scores in descending order
        score_series = pd.Series(similarity_matrix_full2[idx]).sort_values(ascending = False)
    
        # getting the indexes of the 10 most similar hotels except itself
        top_100_indexes = list(score_series.iloc[1:25].index)
        
        # populating the list with the names of the top 10 matching hotels
        for i in top_100_indexes:
            recommended_funds.append(list(df.index)[i])
            
        return recommended_funds
    
    answer = recommendations_holdings_full()
        
    
    #answer = recommendations_holdings_full()
    #st.write(answer)
    st.table(df2.loc[name][['fund_name','broad_asset class','risk_monthly_VAR','30_day_sec_yield_real','total_return_3y','expense_ratio','position_bond_long', 'total_return_10y', 'leverage_y',
       'position_stock_net', 'total_return_3m']].transpose())
    
    
    st.table(df2.loc[answer][['fund_name','broad_asset class','risk_monthly_VAR','30_day_sec_yield_real','total_return_3y','expense_ratio','position_bond_long', 'total_return_10y', 'leverage_y',
       'position_stock_net', 'total_return_3m']])
    #st.write((df2.head()))
            
            
            
            
            
def run_rec():
    indices = pd.Series(df.index)
    
    #st.dataframe(df.head())
    #st.dataframe(df2.head())
    choice = st.radio('How would you like to search?', ('By Name','By Ticker'))
    if choice == 'By Ticker':
        name = st.selectbox('Type in the fund ticker',sorted(df.index))
    elif choice == 'By Name':
        family = st.selectbox('Fund Family Name', sorted(df2['fund_family'].unique()))
        asset = st.selectbox('Pick Asset Class', sorted(df2.loc[df2['fund_family'] == family]['broad_asset class'].unique()))
        name_1= st.selectbox('Pick Ticker', sorted(df2.loc[(df2['fund_family'] == family) & (df2['broad_asset class'] == asset)].fund_name))

        name = df2[df2['fund_name'] == name_1].index.values[0]


    
    def recommendations_holdings_full(similarity_matrix_full2 = similarity_matrix_full2):
        recommended_funds = []
        
        # gettin the index of the hotel that matches the name

        idx = indices[indices == name].index[0]

        
        # creating a Series with the similarity scores in descending order
        score_series = pd.Series(similarity_matrix_full2[idx]).sort_values(ascending = False)
    
        # getting the indexes of the 10 most similar hotels except itself
        top_100_indexes = list(score_series.iloc[1:25].index)
        
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
    st.table(df2.loc[name][['fund_name','broad_asset class','risk_monthly_VAR','30_day_sec_yield_real','total_return_3y','expense_ratio','position_bond_long', 'total_return_10y', 'leverage_y',
       'position_stock_net', 'total_return_3m']].transpose())
    
    
    st.table(df2.loc[answer][['fund_name','broad_asset class','risk_monthly_VAR','30_day_sec_yield_real','total_return_3y','expense_ratio','position_bond_long', 'total_return_10y', 'leverage_y',
       'position_stock_net', 'total_return_3m']])
    #st.write((df2.head()))









if __name__ == "__main__":
    main()
