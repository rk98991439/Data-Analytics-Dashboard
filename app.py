import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Data Analytics Dashboard")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write(data.head())
    st.write(data.describe())

    numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_cols) > 0:
        selected_col = st.selectbox("Select a column for histogram", numeric_cols)
        fig, ax = plt.subplots()
        sns.histplot(data[selected_col], kde=True, ax=ax)
        st.pyplot(fig)
