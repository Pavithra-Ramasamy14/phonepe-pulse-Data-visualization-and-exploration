import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import json
import requests
from streamlit_option_menu import option_menu
from PIL import Image

#Dataframe creation
#mysql connection
config = {
        'user':'root', 'password':'pavi',
        'host':'127.0.0.1', 'database':'phonepe_data'
    }
connection=mysql.connector.connect(**config)
cursor=connection.cursor()

#Aggregated_transsaction
cursor.execute("select * from aggregated_transaction;")
table1 = cursor.fetchall()
Aggregated_transaction = pd.DataFrame(table1,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))

#Aggregated_user
cursor.execute("select * from aggregated_user")
table2 = cursor.fetchall()
Aggregated_user = pd.DataFrame(table2,columns = ("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))

#Map_transaction
cursor.execute("select * from map_transaction")
table3 = cursor.fetchall()
Map_transaction = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))

#Map_user
cursor.execute("select * from map_user")
table4 = cursor.fetchall()
Map_user = pd.DataFrame(table4,columns = ("States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"))

#Top_transaction
cursor.execute("select * from top_transaction")
table5 = cursor.fetchall()
Top_transaction = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#Top_user
cursor.execute("select * from top_user")
table6 = cursor.fetchall()
Top_user = pd.DataFrame(table6, columns = ("States", "Years", "Quarter", "Pincodes", "RegisteredUser"))



def Transaction_Y(df,year):
    tr_y= df[df["Years"] == year]
    tr_y.reset_index(drop= True, inplace= True)

    tr_yg=tr_y.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tr_yg.reset_index(inplace= True)
    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(tr_yg, x="States", y= "Transaction_amount",title= f"{year} TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,width=600, height= 650)
        st.plotly_chart(fig_amount)
    
    with col2:
        fig_count= px.bar(tr_yg, x="States", y= "Transaction_count",title= f"{year} TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,width=600, height= 650)
        st.plotly_chart(fig_count)
    
    col1,col2= st.columns(2)
    with col1:
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        
        states_name_trans=[feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_trans.sort()
        fig_india_1= px.choropleth(tr_yg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                    range_color= (tr_yg["Transaction_amount"].min(),tr_yg["Transaction_amount"].max()),
                                    hover_name= "States",title = f"{year} TRANSACTION AMOUNT",
                                    fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)
        st.plotly_chart(fig_india_1)
    with col2:    
        fig_india_2= px.choropleth(tr_yg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                    range_color= (tr_yg["Transaction_count"].min(),tr_yg["Transaction_count"].max()),
                                    hover_name= "States",title = f"{year} TRANSACTION COUNT",
                                    fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)
        st.plotly_chart(fig_india_2)

    return tr_y


def Transaction_Y_Q(df,quarter):
    tr_y= df[df["Quarter"] == quarter]
    tr_y.reset_index(drop= True, inplace= True)

    tr_yg=tr_y.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tr_yg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_q_amount= px.bar(tr_yg, x="States", y= "Transaction_amount",title= f"{tr_y['Years'].min()} YEAR AND {quarter} QUARTER TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_q_amount)
    
    with col2:
        fig_q_count= px.bar(tr_yg, x="States", y= "Transaction_count",title= f"{tr_y['Years'].min()} YEAR AND {quarter} QUARTER TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_q_count)

    col1,col2= st.columns(2)
    with col1:
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        
        states_name_trans=[feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_trans.sort()
        fig_india_1= px.choropleth(tr_yg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                    range_color= (tr_yg["Transaction_amount"].min(),tr_yg["Transaction_amount"].max()),
                                    hover_name= "States",title = f"{tr_y['Years'].min()} YEAR AND {quarter} QUARTER TRANSACTION AMOUNT",
                                    fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2= px.choropleth(tr_yg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                    range_color= (tr_yg["Transaction_count"].min(),tr_yg["Transaction_count"].max()),
                                    hover_name= "States",title = f"{tr_y['Years'].min()} YEAR AND {quarter} QUARTER TRANSACTION COUNT",
                                    fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)
        st.plotly_chart(fig_india_2)
    return tr_y

def Aggregated_Transaction_type(df,state):
    df_state= df[df["States"] == state]
    df_state.reset_index(drop= True, inplace= True)
    
    agttg= df_state.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    agttg.reset_index(inplace= True)
    

    fig_hbar_1= px.bar(agttg, x= "Transaction_type", y= "Transaction_count",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, width= 600, 
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION COUNT",height= 500)
    st.plotly_chart(fig_hbar_1)

    

    fig_hbar_2= px.bar(agttg, x= "Transaction_type", y= "Transaction_amount",
                        color_discrete_sequence=px.colors.sequential.Greens_r, width= 600,
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION AMOUNT", height= 500)
    st.plotly_chart(fig_hbar_2)

def Aggre_user_plot_1(df,year):
    aguy= df[df["Years"] == year]
    aguy.reset_index(drop= True, inplace= True)
    
    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_line_1= px.bar(aguyg, x="Brands",y= "Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000,color_discrete_sequence=px.colors.sequential.Bluered_r)
    st.plotly_chart(fig_line_1)

    return aguy

def Aggre_user_plot_2(df,quarter):
    auqs= df[df["Quarter"] == quarter]
    auqs.reset_index(drop= True, inplace= True)

    fig_pie_1= px.pie(data_frame=auqs, names= "Brands", values="Transaction_count", hover_data= "Percentage",
                      width=1000,title=f"{quarter} QUARTER TRANSACTION COUNT PERCENTAGE",hole=0.5, color_discrete_sequence= px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_pie_1)

    return auqs

def Aggre_user_plot_3(df,state):
    aguqy= df[df["States"] == state]
    aguqy.reset_index(drop= True, inplace= True)

    aguqyg= pd.DataFrame(aguqy.groupby("Brands")["Transaction_count"].sum())
    aguqyg.reset_index(inplace= True)

    fig_scatter_1= px.line(aguqyg, x= "Brands", y= "Transaction_count", markers= True,width=1000)
    st.plotly_chart(fig_scatter_1)

def Map_transaction_District(df, state):

    tacy= df[df["States"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    
    fig_bar_1= px.bar(tacyg, x= "Districts", y= "Transaction_amount", height= 600,
                        title= f"{state.upper()} AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Mint_r)
    fig_bar_1.show()

    

    fig_bar_2= px.bar(tacyg, x= "Districts", y= "Transaction_count", height= 600,
                        title= f"{state.upper()} AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Bluered_r)
    fig_bar_2.show()

# map_user_plot_1
def map_user_plot_1(df, year):
    muy= df[df["Years"]== year]
    muy.reset_index(drop= True, inplace= True)

    muyg= muy.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_line_1= px.line(muyg, x= "States", y= ["RegisteredUser", "AppOpens"],
                        title= f"{year} REGISTERED USER, APPOPENS",width= 1000, height= 800, markers= True)
    st.plotly_chart(fig_line_1)

    return muy

# map_user_plot_2
def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"]== quarter]
    muyq.reset_index(drop= True, inplace= True)

    muyqg= muyq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_line_1= px.line(muyqg, x= "States", y= ["RegisteredUser", "AppOpens"],
                        title= f"{df['Years'].min()} YEARS {quarter} QUARTER REGISTERED USER, APPOPENS",width= 1000, height= 800, markers= True,
                        color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muyq

#map_user_plot_3
def map_user_plot_3(df, states):
    muyqs= df[df["States"]== states]
    muyqs.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_bar_1= px.bar(muyqs, x= "RegisteredUser", y= "Districts",
                                title= f"{states.upper()} REGISTERED USER", height= 800, color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:

        fig_map_user_bar_2= px.bar(muyqs, x= "AppOpens", y= "Districts",
                                title= f"{states.upper()} APPOPENS", height= 800, color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)

#top transaction
def Top_transaction_plot_1(df, state):
    tiy= df[df["States"]== state]
    tiy.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_top_trans_bar_1= px.bar(tiy, x= "Quarter", y= "Transaction_amount", hover_data= "Pincodes",
                                title= "TRANSACTION AMOUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_trans_bar_1)

    with col2:

        fig_top_trans_bar_2= px.bar(tiy, x= "Quarter", y= "Transaction_count", hover_data= "Pincodes",
                                title= "TRANSACTION COUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_trans_bar_2)

def top_user_plot_1(df, year):
    tuy= df[df["Years"]== year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUser"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "RegisteredUser", color= "Quarter", width= 1000, height= 800,
                        color_discrete_sequence= px.colors.sequential.Burgyl, hover_name= "States",
                        title= f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy


# top_user_plot_2
def top_user_plot_2(df, state):
    tuys= df[df["States"]== state]
    tuys.reset_index(drop= True, inplace= True)

    fig_top_plot_2= px.bar(tuys, x= "Quarter", y= "RegisteredUser", title= "REGISTERED USERS, PINCODES, QUARTER",
                        width= 1000, height= 800, color= "RegisteredUser", hover_data= "Pincodes",
                        color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)

#top chart
def top_chart_transaction_amount(table_name):
    #plot_1
    query1= f'''SELECT States, SUM(Transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_amount DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    connection.commit()

    df_1= pd.DataFrame(table_1, columns=("States", "Transaction_amount"))

    col1,col2= st.columns(2)
    with col1:

        fig_amount1= px.bar(df_1, x="States", y="Transaction_amount", title="TOP 10 OF TRANSACTION AMOUNT", hover_name= "States",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount1)

    #plot_2
    query2= f'''SELECT States, SUM(Transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_amount
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    connection.commit()

    df_2= pd.DataFrame(table_2, columns=("States", "Transaction_amount"))

    
    with col2:

        fig_amount2= px.bar(df_2, x="States", y="Transaction_amount", title="LAST 10 OF TRANSACTION AMOUNT", hover_name= "States",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount2)

    #plot_3
    query3= f'''SELECT States, AVG(Transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_amount;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    connection.commit()

    df_3= pd.DataFrame(table_3, columns=("States", "Transaction_amount"))

    fig_amount_3= px.bar(df_3, y="States", x="Transaction_amount", title="AVERAGE OF TRANSACTION AMOUNT", hover_name= "States", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)    

def top_chart_transaction_count(table_name):
    #plot_1
    query1= f'''SELECT States, SUM(Transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_count DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    connection.commit()

    df_1= pd.DataFrame(table_1, columns=("States", "Transaction_count"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="States", y="Transaction_count", title="TOP 10 OF TRANSACTION COUNT", hover_name= "States",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT States, SUM(Transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_count
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    connection.commit()

    df_2= pd.DataFrame(table_2, columns=("States", "Transaction_count"))

    with col2:
        fig_amount_2= px.bar(df_2, x="States", y="Transaction_count", title="LAST 10 OF TRANSACTION COUNT", hover_name= "States",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT States, AVG(Transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_count;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    connection.commit()

    df_3= pd.DataFrame(table_3, columns=("States", "Transaction_count"))

    fig_amount_3= px.bar(df_3, y="States", x="Transaction_count", title="AVERAGE OF TRANSACTION COUNT", hover_name= "States", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

def top_chart_registered_user(table_name, state):

    #plot_1
    query1= f'''SELECT Districts, SUM(RegisteredUser) AS registereduser
                FROM {table_name}
                WHERE States= '{state}'
                GROUP BY Districts
                ORDER BY RegisteredUser DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    connection.commit()

    df_1= pd.DataFrame(table_1, columns=("Districts", "RegisteredUser"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="Districts", y="RegisteredUser", title="TOP 10 OF REGISTERED USER", hover_name= "Districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT Districts, SUM(RegisteredUser) AS registereduser
                FROM {table_name}
                WHERE States= '{state}'
                GROUP BY Districts
                ORDER BY Registereduser
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    connection.commit()

    df_2= pd.DataFrame(table_2, columns=("Districts", "RegisteredUser"))

    with col2:
        fig_amount_2= px.bar(df_2, x="Districts", y="RegisteredUser", title="LAST 10 REGISTERED USER", hover_name= "Districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT Districts, AVG(RegisteredUser) AS registereduser
                FROM {table_name}
                WHERE States= '{state}'
                GROUP BY Districts
                ORDER BY RegisteredUser;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    connection.commit()

    df_3= pd.DataFrame(table_3, columns=("Districts", "RegisteredUser"))

    fig_amount_3= px.bar(df_3, x="RegisteredUser", y="Districts", title="AVERAGE OF REGISTERED USER", hover_name= "Districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

def top_chart_appopens(table_name, state):
    #plot_1
    query1= f'''SELECT Districts, SUM(AppOpens) AS AppOpens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY Districts
                ORDER BY AppOpens DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    connection.commit()

    df_1= pd.DataFrame(table_1, columns=("Districts", "AppOpens"))


    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="Districts", y="AppOpens", title="TOP 10 OF APPOPENS", hover_name= "Districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT Districts, SUM(AppOpens) AS AppOpens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY Districts
                ORDER BY AppOpens
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    connection.commit()

    df_2= pd.DataFrame(table_2, columns=("Districts", "AppOpens"))

    with col2:

        fig_amount_2= px.bar(df_2, x="Districts", y="AppOpens", title="LAST 10 APPOPENS", hover_name= "Districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT Districts, AVG(AppOpens) AS AppOpens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY Districts
                ORDER BY AppOpens;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    connection.commit()

    df_3= pd.DataFrame(table_3, columns=("Districts", "AppOpens"))

    fig_amount_3= px.bar(df_3, y="Districts", x="AppOpens", title="AVERAGE OF APPOPENS", hover_name= "Districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

def top_chart_registered_users(table_name):
    
    #plot_1
    query1= f'''SELECT states, SUM(RegisteredUser) AS RegisteredUser
                FROM {table_name}
                GROUP BY states
                ORDER BY RegisteredUser DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    connection.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "RegisteredUser"))
    
    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="states", y="RegisteredUser", title="TOP 10 OF REGISTERED USERS", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT states, SUM(RegisteredUser) AS RegisteredUser
                FROM {table_name}
                GROUP BY states
                ORDER BY RegisteredUser
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    connection.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "RegisteredUser"))

    with col2:

        fig_amount_2= px.bar(df_2, x="states", y="RegisteredUser", title="LAST 10 REGISTERED USERS", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT states, AVG(RegisteredUser) AS RegisteredUser
                FROM {table_name}
                GROUP BY states
                ORDER BY RegisteredUser;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    connection.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "RegisteredUser"))

    fig_amount_3= px.bar(df_3, y="states", x="RegisteredUser", title="AVERAGE OF REGISTERED USERS", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

#streamlit part
st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")
with st.sidebar:
    select=option_menu("Main menu",["HOME","DATA EXPLORATION","TOP CHARTS"])
if select=="HOME":
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.image(Image.open(r"C:\Users\Admin\phone pulse project\phonepe img2.jpeg"),width= 400)

    col3,col4= st.columns(2)
    
    with col3:
        st.image(Image.open(r"C:\Users\Admin\phone pulse project\phonepe img.jpeg"),width=400)

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.image(Image.open(r"C:\Users\Admin\phone pulse project\phonepe img3.jpeg"),width= 400)


elif select=="DATA EXPLORATION":
    tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])
    with tab1:
        method_1=st.radio("Select the method",["Aggregated Transaction Analysis","Aggregated User Analysis"])
        if method_1=="Aggregated Transaction Analysis":
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select the Year",Aggregated_transaction["Years"].min(),Aggregated_transaction["Years"].max(),Aggregated_transaction["Years"].min(),key=1)
            aggtr_y=Transaction_Y(Aggregated_transaction,years)
            

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select the Quarter",aggtr_y["Quarter"].min(),aggtr_y["Quarter"].max(),aggtr_y["Quarter"].min(),key=2)

            aggtr_Y_Q=Transaction_Y_Q(aggtr_y,quarters)

            #Select the State for Analyse the Transaction type
            state_Y_Q= st.selectbox("**Select the State**",aggtr_Y_Q["States"].unique(),key=10)

            Aggregated_Transaction_type(aggtr_Y_Q,state_Y_Q)
        
    

        elif method_1=="Aggregated User Analysis":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",Aggregated_user["Years"].min(), Aggregated_user["Years"].max()
                              ,Aggregated_user["Years"].min(),key=3)

            agg_u_y=Aggre_user_plot_1(Aggregated_user,years)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.selectbox("Select The Quarter",agg_u_y["Quarter"].unique(),key=11)
                                    
            
            agg_u_y_q=Aggre_user_plot_2(agg_u_y,quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("**Select the State_AU**",agg_u_y_q["States"].unique(),key=12)
            Aggre_user_plot_3(agg_u_y_q,states)

            
    with tab2:
        method_2=st.radio("Select the method",["Map Transaction Analysis","Map User Analysis"])
        if method_2=="Map Transaction Analysis":
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select the Year",Aggregated_transaction["Years"].min(),Aggregated_transaction["Years"].max(),Aggregated_transaction["Years"].min(),key=4)
            maptr_y=Transaction_Y(Map_transaction,years)
            

            col1,col2=st.columns(2)
            with col1:
                quarters=st.selectbox("Select the Quarter",maptr_y["Quarter"].unique(),key=13)

            maptr_Y_Q=Transaction_Y_Q(maptr_y,quarters)

            #Select the State for Analyse the Transaction type
            state_Y_Q= st.selectbox("**Select the State**",maptr_Y_Q["States"].unique(),key=14)

            Map_transaction_District(maptr_Y_Q,state_Y_Q)
        

        elif method_2=="Map User Analysis":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",Map_user["Years"].min(), Map_user["Years"].max()
                                 ,Map_user["Years"].min(),key=5)
            map_user_Y= map_user_plot_1(Map_user, years)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.selectbox("Select The Quarter",map_user_Y["Quarter"].unique(),key=15)
            map_user_Y_Q= map_user_plot_2(map_user_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State", map_user_Y_Q["States"].unique(),key=16)

            map_user_plot_3(map_user_Y_Q,states)

    with tab3:
        method_3=st.radio("Select the method",["Top Transaction Analysis","Top User Analysis"])
        if method_3=="Top Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",Top_transaction["Years"].min(),Top_transaction["Years"].max(),Top_transaction["Years"].min(),key=6)
            top_t_Y= Transaction_Y(Top_transaction, years)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.selectbox("Select The Quarter",top_t_Y["Quarter"].unique(),key=17)
            top_t_Y_Q= Transaction_Y_Q(top_t_Y, quarters)
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State", top_t_Y_Q["States"].unique(),key=18)

            Top_transaction_plot_1(top_t_Y_Q, states)

            
        elif method_3=="Top User Analysis":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",Top_user["Years"].min(), Top_user["Years"].max(),Top_user["Years"].min(),key=7)
            top_user_Y= top_user_plot_1(Top_user, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State", top_user_Y["States"].unique(),key=19)

            top_user_plot_2(top_user_Y, states)
elif select=="TOP CHARTS":
    question= st.selectbox("Select the Question",["1. Transaction Amount and Count of Aggregated Transaction",
                                                    "2. Transaction Amount and Count of Map Transaction",
                                                    "3. Transaction Amount and Count of Top Transaction",
                                                    "4. Transaction Count of Aggregated User",
                                                    "5. Registered users of Map User",
                                                    "6. App opens of Map User",
                                                    "7. Registered users of Top User",
                                                    ])
    
    if question == "1. Transaction Amount and Count of Aggregated Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")
    elif question == "2. Transaction Amount and Count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")
    elif question == "3. Transaction Amount and Count of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")    
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")
    elif question == "4. Transaction Count of Aggregated User":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")
    elif question == "5. Registered users of Map User":
        
        states= st.selectbox("Select the State", Map_user["States"].unique())   
        st.subheader("REGISTERED USERS")
        top_chart_registered_user("map_user", states)
    elif question == "6. App opens of Map User":
        
        states= st.selectbox("Select the State", Map_user["States"].unique())   
        st.subheader("APPOPENS")
        top_chart_appopens("map_user", states)
    elif question == "7. Registered users of Top User":
          
        st.subheader("REGISTERED USERS")
        top_chart_registered_users("top_user")



