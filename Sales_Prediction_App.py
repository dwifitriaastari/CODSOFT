import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.model_selection import train_test_split, GridSearchCV, KFold, cross_val_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression, HuberRegressor
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv("C:\\Users\\Dwi Fitria\\Intern\\CODSOFT\\CODSOFT\\7. Sales Prediction by Python\\advertising.csv")
df['Newspaper_sqrt'] = np.sqrt(df['Newspaper'])
new_df = df.drop(['Newspaper'], axis=1)

# Prepare the data
X = new_df[['TV', 'Radio', 'Newspaper_sqrt']]
y = new_df['Sales']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Polynomial Regression Pipeline
def PolynomialRegression(degree=2, **kwargs):
    return make_pipeline(PolynomialFeatures(degree), LinearRegression(**kwargs))

# GridSearchCV
param_grid = {
    'polynomialfeatures__degree': [2],
    'linearregression__fit_intercept': [True],
}
grid_search = GridSearchCV(PolynomialRegression(), param_grid, scoring='neg_mean_squared_error', cv=5)
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_

# Test set predictions
y_pred = best_model.predict(X_test)

# Streamlit App
st.title("Sales Prediction App")

st.write("Enter advertising spending values to predict sales.")

tv_spending = st.number_input("TV Spending", min_value=0.0, value=150.0)
radio_spending = st.number_input("Radio Spending", min_value=0.0, value=50.0)
newspaper_spending = st.number_input("Newspaper Spending", min_value=0.0, value=20.0)

if st.button("Predict Sales"):
    new_data = pd.DataFrame({'TV': [tv_spending], 'Radio': [radio_spending], 'Newspaper_sqrt': [np.sqrt(newspaper_spending)]})
    predicted_sales = best_model.predict(new_data)[0]
    st.write(f"Predicted Sales: {predicted_sales:.2f}")
