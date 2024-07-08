import os
import streamlit as st
import plotly.graph_objects as go

# Get the current working directory
current_dir = os.getcwd()

# Navigate to the directory containing the file
file_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_dir)

# Create a title
st.title("CHÀO MỪNG")

# Display the title on the Streamlit app
st.write("Hello, world!")

# Create data for the first bar chart
x1 = ['A', 'B', 'C', 'D']
y1 = [10, 15, 7, 12]

# Create data for the second bar chart
x2 = ['E', 'F', 'G', 'H']
y2 = [5, 8, 3, 10]

# Create the first bar chart
fig1 = go.Figure(data=go.Bar(x=x1, y=y1))

# Create the second bar chart
fig2 = go.Figure(data=go.Bar(x=x2, y=y2))

# Display the first bar chart
st.plotly_chart(fig1, use_container_width=True)

# Display the second bar chart
st.plotly_chart(fig2, use_container_width=True)
