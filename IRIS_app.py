import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load the Iris dataset 
@st.cache_data
def load_data():
    from sklearn.datasets import load_iris
    iris = load_iris()
    iris_df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    iris_df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
    return iris_df

iris_df = load_data()

st.title("Iris Flower Classification App")

# Display the dataset
st.subheader("Iris Dataset")
st.dataframe(iris_df.head())

# Pair Plot
st.subheader("Pair Plot of Iris Features")
fig_pairplot = sns.pairplot(iris_df, hue="species")
st.pyplot(fig_pairplot)

# Model Training
st.subheader("Model Training")

X = iris_df.drop('species', axis=1)
y = iris_df['species']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

k_value = st.slider("Select k value for KNN", min_value=1, max_value=20, value=3)

knn = KNeighborsClassifier(n_neighbors=k_value)
knn.fit(X_train_scaled, y_train)

y_pred = knn.predict(X_test_scaled)

accuracy = accuracy_score(y_test, y_pred)
st.write(f"Accuracy: {accuracy}")

st.write("Classification Report:")
st.text(classification_report(y_test, y_pred))

# Prediction Section
st.subheader("Make a Prediction")

sepal_length = st.number_input("Sepal Length (cm)", min_value=4.0, max_value=8.0, value=5.8)
sepal_width = st.number_input("Sepal Width (cm)", min_value=2.0, max_value=4.5, value=3.0)
petal_length = st.number_input("Petal Length (cm)", min_value=1.0, max_value=7.0, value=3.7)
petal_width = st.number_input("Petal Width (cm)", min_value=0.1, max_value=2.5, value=1.2)

if st.button("Predict"):
    input_data = [[sepal_length, sepal_width, petal_length, petal_width]]
    input_scaled = scaler.transform(input_data)
    prediction = knn.predict(input_scaled)[0]
    st.write(f"Predicted Species: {prediction}")