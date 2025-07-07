import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set seaborn theme for dark background compatibility (optional)
sns.set_theme(style="darkgrid")

st.set_page_config(page_title="Data Analytics Dashboard", layout="wide")
st.title("📊 Data Analytics & Cleaning Dashboard")

# Sidebar - Upload
st.sidebar.header("Upload & Cleaning")

uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.subheader("🔍 Original Data Preview")
    st.dataframe(data.head())

    # Show basic info
    st.write(f"✅ Dataset Shape: {data.shape[0]} rows × {data.shape[1]} columns")
    st.write(f"✅ Columns: {', '.join(data.columns)}")
    
    # Sidebar Cleaning Options
    st.sidebar.subheader("Data Cleaning Options")

    # Remove Duplicates
    if st.sidebar.checkbox("Remove Duplicate Rows"):
        data = data.drop_duplicates()
        st.success(f"Duplicates removed. New shape: {data.shape}")

    # Handle Missing Values
    missing_option = st.sidebar.selectbox("Handle Missing Values", ["None", "Drop rows with missing", "Fill missing with 0"])

    if missing_option == "Drop rows with missing":
        data = data.dropna()
        st.success(f"Missing values dropped. New shape: {data.shape}")

    elif missing_option == "Fill missing with 0":
        data = data.fillna(0)
        st.success(f"Missing values filled with 0.")

    st.subheader("🧹 Cleaned Data Preview")
    st.dataframe(data.head())
    st.write(data.describe())

    # Visualization Section
    st.sidebar.subheader("Visualization Options")

    numeric_cols = data.select_dtypes(include=['float64', 'int64', 'int32']).columns.tolist()
    all_cols = data.columns.tolist()

    if len(all_cols) > 0:
        plot_type = st.sidebar.selectbox("Select Plot Type", ["Histogram", "Boxplot", "Scatter Plot", "Correlation Heatmap", "Barplot"])

        if plot_type == "Histogram":
            selected_col = st.sidebar.selectbox("Select Numeric Column", numeric_cols)
            st.subheader(f"📊 Histogram of {selected_col}")
            fig, ax = plt.subplots()
            sns.histplot(data[selected_col], kde=True, ax=ax, color="#4CAF50")
            st.pyplot(fig)

        elif plot_type == "Boxplot":
            selected_col = st.sidebar.selectbox("Select Numeric Column", numeric_cols)
            st.subheader(f"📦 Boxplot of {selected_col}")
            fig, ax = plt.subplots()
            sns.boxplot(y=data[selected_col], ax=ax, color="#FF5722")
            st.pyplot(fig)

        elif plot_type == "Scatter Plot":
            x_col = st.sidebar.selectbox("X-axis", numeric_cols)
            y_col = st.sidebar.selectbox("Y-axis", numeric_cols)
            st.subheader(f"⚡ Scatter Plot: {x_col} vs {y_col}")
            fig, ax = plt.subplots()
            sns.scatterplot(data=data, x=x_col, y=y_col, ax=ax, color="#2196F3")
            st.pyplot(fig)

        elif plot_type == "Correlation Heatmap":
            st.subheader("🔗 Correlation Heatmap")
            corr = data[numeric_cols].corr()
            fig, ax = plt.subplots()
            sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)

        elif plot_type == "Barplot":
            selected_col = st.sidebar.selectbox("Select Categorical Column", all_cols)
            st.subheader(f"📊 Barplot of {selected_col}")
            fig, ax = plt.subplots()
            data[selected_col].value_counts().plot(kind='bar', color="#4CAF50", ax=ax)
            ax.set_ylabel("Count")
            st.pyplot(fig)
    else:
        st.warning("⚠️ No columns found for visualization.")
else:
    st.info("Please upload a CSV file to get started.")
