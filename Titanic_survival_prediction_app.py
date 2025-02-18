# %%
import streamlit as st
import pandas as pd
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from sklearn.pipeline import make_pipeline
import pickle
import warnings

#Suppress the specific warning
warnings.filterwarnings("ignore", message="missing ScriptRunContext")

# --- Data Loading ---
df = pd.read_csv("C:\\Users\\Dwi Fitria\\Intern\\CODSOFT\\CODSOFT\\4. Titanic Survival Prediction\\4. Titanic Survival Dataset.csv")

# --- Define features and target ---
numerical_features = ['Age', 'SibSp', 'Parch', 'Fare'] # Exclude 'FamilySize'
categorical_features = ['Pclass', 'Sex', 'Embarked']  # Exclude 'AgeGroup' and 'FareGroup'
target = 'Survived'

# --- Split data ---
X = df[numerical_features + categorical_features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Preprocessor (One-Hot Encoding and Scaling) ---
preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline([('scaler', StandardScaler()), ('passthrough', 'passthrough')]), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# --- Pipeline with SMOTE and Model ---
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('smote', SMOTE(random_state=42)),  
    ('classifier', RandomForestClassifier(random_state=42, n_estimators=100, n_jobs=-1))  
])

# --- Train the model ---
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=UserWarning)
    pipeline.fit(X_train, y_train)

save_path = os.path.join(os.path.expanduser("~"), "titanic_model.pkl")  # Saves to your home directory
with open(save_path, 'wb') as file:
    pickle.dump(pipeline, file)

print(f"Model saved to: {save_path}") # Print the path so you know where it is.

st.title("Titanic Survival Prediction App")

# --- Input Form ---
st.sidebar.header("Passenger Information")

# Numerical Inputs (Consistent Float Type)
age = st.sidebar.number_input("Age", min_value=0.0, value=90.0, step=1.0)  # All floats
sibsp = st.sidebar.number_input("Siblings/Spouses Aboard", min_value=0, value=0, step=1) # All ints
parch = st.sidebar.number_input("Parents/Children Aboard", min_value=0, value=0, step=1) # All ints
fare = st.sidebar.number_input("Fare", min_value=0.0, value=1000.0, step=0.1)  # All floats
family_size = sibsp + parch + 1  # Calculate family size


# Categorical Inputs
pclass = st.sidebar.selectbox("Passenger Class", [1, 2, 3])
sex = st.sidebar.selectbox("Sex", ["male", "female"])
embarked = st.sidebar.selectbox("Port of Embarkation", ["S", "C", "Q"])


# --- Prediction ---
if st.sidebar.button("Predict"):
    input_data = pd.DataFrame({
        'Age': [age],
        'SibSp': [sibsp],
        'Parch': [parch],
        'Fare': [fare],
        'FamilySize': [family_size],
        'Pclass': [pclass],
        'Sex': [sex],
        'Embarked': [embarked]
    })

    prediction = pipeline.predict(input_data)[0]
    probability = pipeline.predict_proba(input_data)[0][1] # Probability of survival

    st.write(f"**Prediction:** {'Survived' if prediction == 1 else 'Did Not Survive'}")
    st.write(f"**Probability of Survival:** {probability:.2f}")

    # --- Feature Importance (Optional) ---
    importances = pipeline.named_steps['classifier'].feature_importances_
    onehot_features = pipeline.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out(categorical_features)
    numerical_features_used = pipeline.named_steps['preprocessor'].named_transformers_['num'].get_feature_names_out(numerical_features)
    feature_names = list(numerical_features_used) + list(onehot_features)
    feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
    feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

    st.subheader("Feature Importances")
    st.bar_chart(feature_importance_df.set_index('Feature'))  # Streamlit bar chart


