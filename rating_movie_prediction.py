import streamlit as st
import pandas as pd
import numpy as np
from sklearn.svm import LinearSVR
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load and preprocess data (cached for performance)
@st.cache_data
def load_and_preprocess_data(file_path, encoding='latin-1'): 
    try:
        df = pd.read_csv(file_path, encoding=encoding)
    except UnicodeDecodeError:
        st.error(f"Error decoding file with {encoding} encoding. Trying utf-8")
        df = pd.read_csv(file_path, encoding='utf-8')
    df.dropna(subset=['Rating', 'Votes'], inplace=True)
    df['Votes'] = df['Votes'].str.replace(',', '').astype(int)
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Duration'] = df['Duration'].str.replace(' min', '', regex=False)
    df['Duration'] = pd.to_numeric(df['Duration'], errors='coerce')
    categorical_cols = ['Genre', 'Director', 'Actor 1', 'Actor 2', 'Actor 3']
    for col in categorical_cols:
        df.loc[:, col] = df[col].fillna('Unknown')
    max_categories = 20
    for col in categorical_cols:
        top_categories = df[col].value_counts().nlargest(max_categories).index
        df.loc[:, col] = df[col].where(df[col].isin(top_categories), 'Other')
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded_features = encoder.fit_transform(df[['Genre', 'Director', 'Actor 1', 'Actor 2', 'Actor 3']])
    feature_names = encoder.get_feature_names_out(categorical_cols)
    encoded_df = pd.DataFrame(encoded_features, index=df.index, columns=feature_names)
    df = pd.concat([df, encoded_df], axis=1)
    features = encoded_df.columns
    target = 'Rating'
    X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test, encoder, feature_names

# Load data and train model
@st.cache_resource
def train_model(file_path):
    X_train, X_test, y_train, y_test, encoder, feature_names = load_and_preprocess_data(file_path)
    best_linear_svr = LinearSVR(C=0.1, epsilon=0.2, loss='epsilon_insensitive', dual='auto', random_state=42)
    best_linear_svr.fit(X_train, y_train)
    return best_linear_svr, encoder, feature_names, X_test, y_test

# Load data and train model
best_linear_svr, encoder, feature_names, X_test, y_test = train_model('/workspaces/CODSOFT/IMDb Movies India2.csv')

# Streamlit App
st.title('Movie Rating Prediction')

# Get unique values for dropdowns
genre_options = ['Other'] + [col.split('_')[1] for col in feature_names if col.startswith('Genre_')]
director_options = ['Other'] + [col.split('_')[1] for col in feature_names if col.startswith('Director_')]
actor1_options = ['Other'] + [col.split('_')[1] for col in feature_names if col.startswith('Actor 1_')]
actor2_options = ['Other'] + [col.split('_')[1] for col in feature_names if col.startswith('Actor 2_')]
actor3_options = ['Other'] + [col.split('_')[1] for col in feature_names if col.startswith('Actor 3_')]

# Create input fields
genre = st.selectbox('Genre', genre_options)
director = st.selectbox('Director', director_options)
actor1 = st.selectbox('Actor 1', actor1_options)
actor2 = st.selectbox('Actor 2', actor2_options)
actor3 = st.selectbox('Actor 3', actor3_options)

# Prediction function
def predict_rating(genre, director, actor1, actor2, actor3, encoder, model, feature_names):
    input_data = pd.DataFrame([[genre, director, actor1, actor2, actor3]], columns=['Genre', 'Director', 'Actor 1', 'Actor 2', 'Actor 3'])
    encoded_input = encoder.transform(input_data)
    input_df = pd.DataFrame(encoded_input, columns=feature_names)
    prediction = model.predict(input_df)
    return prediction[0]

# Make prediction
if st.button('Predict Rating'):
    rating = predict_rating(genre, director, actor1, actor2, actor3, encoder, best_linear_svr, feature_names)
    st.write(f'Predicted Rating: {rating:.2f}')

# Model Evaluation (optional)
st.subheader('Model Evaluation (Test Set)')
y_pred = best_linear_svr.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
st.write(f'MAE: {mae:.4f}')
st.write(f'MSE: {mse:.4f}')
st.write(f'RMSE: {rmse:.4f}')