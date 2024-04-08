# Phonepe-pulse-Data-visualization-and-exploration
Introduction:

PhonePe has become one of the most popular digital payment platforms in India, with millions of users relying on it for their day-to-day transactions. The app is known for its simplicity, user-friendly interface, and fast and secure payment processing. It has also won several awards and accolades for its innovative features and contributions to the digital payments industry.

We create a web app to analyse the Phonepe transaction and users depending on various Years, Quarters, States, and Types of transaction and give a Geographical and Geo visualization output based on given requirements.

1.Tools to install

  virtual code.
  
  Jupyter notebook.
  
  Python 3.11.0 or higher.
  
  MySQL

  Git

2.Import Libraries

  import streamlit as st
  
  import pandas as pd
  
  import mysql.connector
  
  import plotly.express as px
  
  import json
  
  import requests
  
  from streamlit_option_menu import option_menu
  
  from PIL import Image
  
3.E T L Process

a) Extract data

Initially, we Clone the data from the Phonepe GitHub repository by using Python libraries. https://github.com/PhonePe/pulse.git

b) Process and Transform the data

Process the clone data by using Python and transform the processed data into DataFrame format.

c) Load data

Finally, create a connection to the MySQL server and create a Database and stored the Transformed data in mysql.

4.E D A Process and Frame work

a) Access MySQL DB

Create a connection to the MySQL server and access the specified MySQL DataBase by using pymysql library

b) Filter the data

Filter and process the collected data depending on the given requirements by using SQL queries

c) Visualization

Finally, create a Dashboard by using Streamlit and show the output in Geo visualization, bar chart, and pie chart format.
