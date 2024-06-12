import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data = pd.read_csv('banana_quality.csv')

# Title of the web app
st.title('Banana Quality Analysis App')

# Introduction text
st.write("""
This app showcases various insights from the Banana Quality dataset. 
The dataset contains information about different predictors such as Size, Weight, Sweetness, Softness, 
HarvestTime, Ripeness, and Acidity, and their impact on the Quality of bananas.
""")

# Display the raw data as a table
st.subheader('Raw Data')
st.write(data)

# Display basic statistics
st.subheader('Basic Statistics')
st.write(data.describe())

# Create a function to plot various charts
def plot_chart(chart_type, x_col, y_col=None):
    plt.figure(figsize=(10, 6))
    if chart_type == 'Bar Chart':
        if data[y_col].dtype == 'object' and data[x_col].dtype in ['int64', 'float64']:
            sns.barplot(x=x_col, y=y_col, data=data)
            plt.title(f'{chart_type} of {x_col} by {y_col}')
        else:
            st.write("For a Bar Chart, the Y-axis should be categorical and the X-axis should be numerical.")
    elif chart_type == 'Scatter Plot':
        if data[x_col].dtype in ['int64', 'float64'] and data[y_col].dtype in ['int64', 'float64']:
            sns.scatterplot(x=x_col, y=y_col, data=data)
            plt.title(f'{chart_type} of {y_col} vs {x_col}')
        else:
            st.write("For a Scatter Plot, both X and Y axes should be numerical.")
    elif chart_type == 'Pie Chart':
        if data[x_col].dtype == 'object':
            pie_data = data[x_col].value_counts()
            plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=140)
            plt.title(f'{chart_type} of {x_col}')
        else:
            st.write("For a Pie Chart, the selected column should be categorical.")
    elif chart_type == 'Histogram':
        if data[x_col].dtype in ['int64', 'float64']:
            sns.histplot(data[x_col])
            plt.title(f'{chart_type} of {x_col}')
        else:
            st.write("For a Histogram, the selected column should be numerical.")
    else:
        st.write("Chart type not supported yet.")
    
    st.pyplot(plt)

# Sidebar for user input
st.sidebar.subheader('Visualization Settings')
chart_type = st.sidebar.selectbox('Select chart type', ['Bar Chart', 'Scatter Plot', 'Pie Chart', 'Histogram'])

# Conditional selections based on chart type
if chart_type in ['Bar Chart', 'Scatter Plot']:
    x_col = st.sidebar.selectbox('Select X-axis', data.columns)
    y_col = st.sidebar.selectbox('Select Y-axis', data.columns)
elif chart_type == 'Pie Chart':
    x_col = st.sidebar.selectbox('Select column for Pie Chart', data.select_dtypes(include=['object']).columns)
    y_col = None
else:  # Histogram
    x_col = st.sidebar.selectbox('Select column for Histogram', data.select_dtypes(include=['int64', 'float64']).columns)
    y_col = None

# Plot the selected chart
st.subheader(f'{chart_type} of {x_col} vs {y_col}' if y_col else f'{chart_type} of {x_col}')
plot_chart(chart_type, x_col, y_col)

# Explanation text for the charts
st.write("""
*Explanation:*

- *Bar Chart*: Shows the comparison between different categories. Y-axis should be categorical and X-axis numerical.
- *Scatter Plot*: Displays the relationship between two numerical variables.
- *Pie Chart*: Represents the proportion of categories in the data.
- *Histogram*: Illustrates the distribution of a numerical variable.
""")
