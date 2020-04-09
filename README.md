# Examining Nightly Prices for Airbnb Listings

## Table of contents

1. [Installation](#installation)
2. [Project Motivations](#project-motivation)
3. [File Descriptions](#file-descriptions)
4. [Running the Jupyter Notebook](#running-the-jupyter-notebook)
5. [Acknowledgements](#acknowledgements)
6. [License](#license)


## Installation

#### Dependencies
This project will require:
    
    Python (>=3.7.4)
    Requests (>=2.23.0)
    Numpy (>=1.18.1)
    Pandas (>=1.0.1)
    Plotly (>=4.5.4)
    Scikit-learn (>=0.22.2.post1)



## Project Motivation
This repo contains the assignment for the 'Write a Data Science Blog Post' project for Udacity's Data Scientist Nanodegree curriculum: https://www.udacity.com/course/data-scientist-nanodegree--nd025

I used Airbnb listing data provided from Inside Airbnb. The full dataset, including download links, can be found here: http://insideairbnb.com/get-the-data.html


## File Descriptions

```
├── Data
│   ├── median_prices.json
│   ├── urls_used.json
│   └── us_data.json
├── Notebook.ipynb
└── README.md
```

- Notebook.ipynb contains the Jupyter Notebook with step-by-step instructions and code
- Data directory is used to store necessary data for processing and analysis after retrieving from 'Inside Airbnb'
  

## Running the Jupyter Notebook
Code and accompanying text are provided, so users can follow along or download the notebook and run the code themselves.

### In this project, I examined whether a linear regression model was able to identify factors that played an outsized role in determining nightly rates, and subsequently predict nightly prices, of Airbnb stays across the locations where 'Inside Airbnb' provided listings data. To do this, I asked the following questions:    

#### 1. How have prices historically trended across geographies?   

To get a high-level understanding of how Airbnb prices have historically trended, I compared median prices for each location offered in the Inside Airbnb dataset by date.  

Judging by median prices alone, it's clear that price variation differs greatly between across countries, but not obvious whether prices differ greatly by location within the same country, or if other factors have a greater impact.  

Variation between median prices of listings across all provided locations, by date:  
![All Listings](/images/all_listings.png)

Variation between median prices of listings across all provided locations within the United States, by date:  
![US Listings](/images/us_listings.png)  

#### 2. Which variables appear to be the top indicators for determining a listing's nightly rate?  

I examined data for Airbnb listings in the US by fitting a linear regression model to a number of provided variables and analyzing the estimated coefficients to determine which are the most influential for determining the nightly price.

Similar to our conclusions for question 1, the estimated coefficients for our linear regression model show that the locations of listings appear to be the top indicators for their nightly price. The only other indicator besides location within the top 20 estimated coefficients is room type - showing that certain room types, such as a Shared Room, show strong negative correlation with the listing price.

![Top 20 Coefficients](/images/coef_weights_20.png)  

#### 3. How well would a linear regression model be able to predict the nightly rate for an Airbnb listing, given other categorical and numerical variables?  
Weak r-squared values for predictions on the test data indicate that this model is not well fit to the dataset and would not be able to accurately predict the nightly rate for an Airbnb listing given its other variables. 
Overfitting was also ruled out as a cause for the weak r-squared value.  
A larger dataset, especially with a higher number of variables per datapoint, would likely be able to improve the prediction accuracy of this linear regression model.  

Based on my analysis of this data, it's clear that the location of the listing is the strongest indicator for the its nightly price. However, as evident from the coefficient weights from the linear model, few other variables are strong indicators for listing prices. As a result, the variables used in this analysis are insufficient to reliably predict listings prices - this can be seen from the weak r-squared values for the linear model's predictions on test data.  


## Acknowledgements
Author: Tim Kou (https://github.com/timothykou)

Thanks for 'Inside Airbnb' for hosting the dataset used for this project (http://insideairbnb.com/get-the-data.html)  

## License  
![License](/License.md)
