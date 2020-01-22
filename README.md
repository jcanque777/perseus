# Mutual Fund Recommendation
John Canque

- [Data](#data)
- [EDA](#eda)
- [Model](#model)
- [Final Recommendation System](#sys)
- [Futher Steps](#steps)


## Project Goals
The goal of this project is to make it easier to choose a mutual fund and ETFs with a content-based item to item fund recommendar based on the features of the fund. With funds closing, underperforming,  and the sheer amount of investment choices, this recommender allows you to choose a fund based on features that matter to you. As a secondary power of the recommender is seeing what the competitors of your fund should be.


## Data Collection <a name='data'></a>
I used selenium and beautiful soup to scrape all mutual funds from [YCharts](https://www.ycharts.com/). I got the following information for each fund:
- Performance
- Asset Allocation
- Risk Information
- Fund Flows
- Region Exposure
- Sector Exposure (equities)
- Style Exposure
- Stock Market Capitalization
- Top 10 Holdings
- Growth Estimates
- Over 140 others

## EDA <a name='eda'></a>
### Data Cleaning
I chose to drop the funds that had 75% of columns with missing values. Only 300 names were dropped which left me with ~14000 mutual funds.


### Data Exploration
As part of the data exploration, one of the more interesting things I found was the wide range of returns and risk. In a market where most prices have been correlated, I was surprised to see how many funds had performance and risk profiles that were more than 3 standard deviations away from the mean.


### Risk Predictions
As part of the EDA, I wanted to see if I can predict the risk (using Monthly Value at Risk) using the many features of each fund. I used Decision Trees, Random Forests, and Linear Regression to evaluate.


## Recommender Model <a name='model'></a>
I used NLP on the top 25 holdings of each fund to focus on the holdings with the most important frequencies(tf-idf). Then I vectorized into a matrix and added the matrix to my dataframe with the fund features. Finally I used cosine similarity to build the similarity matrix.
 

## Final Recommendation System <a name='sys'></a>
For the final recommender, the user inputs a mutual fund and will get the 10 most similar funds. The user can also filter using any of the features on the fund, ie. can look for cheapest funds in the Healthcare space while focusing on the risk metrics.

I built a front-end using streamlit - here is a look at how it works:

## Further Steps <a name='steps'></a>
- Put app live online
- Add functionality to take in descriptors as user input.
- Add business functionality:
  - Allow for fund families to create portfolios based on their funds based on user's specifications
  - Allow for clients to upload full portfolios to get recommendations
