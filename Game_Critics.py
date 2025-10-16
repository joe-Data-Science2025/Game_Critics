import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('Video_Games.csv')

st.title('O seu site sobre vendas de jogo')

st.image('mario.png', width=200)

# limpeza de dados

df1 = df.copy()
df1 = df1[df1['Name'].notnull()]
df1 = df1[df1['Year_of_Release'].notnull()]
df1['Year_of_Release'] = df1['Year_of_Release'].astype('Int64')
df1 = df1[df1['Publisher'].notnull()]
df1 = df1[df1['Critic_Score'].notnull()]
df1['Critic_Score'] = df1['Critic_Score'].astype('Int64')
df1 = df1[df1['User_Score'].notnull()]
df1 = df1[df1['User_Score'] != 'tbd']
df1['User_Score'] = df1['User_Score'].astype('Float64')
df1 = df1[df1['User_Count'].notnull()]
df1['User_Count'] = df1['User_Count'].astype('Int64')
df1 = df1[df1['Developer'].notnull()]
df1 = df1[df1['Rating'].notnull()]
df1 = df1[df1['Rating'] != 'RP']
df1['Global_Sales'] = df1['Global_Sales'].apply(lambda x: x * 100000)
df1 = df1[df1['Global_Sales'] >= 10000.0]
df1 = df1.drop(['EU_Sales', 'JP_Sales', 'NA_Sales'], axis=1)

st.dataframe(df1.head())

# sidebar

st.sidebar.title('Game_critics')
st.sidebar.image('R.png')
m = st.sidebar.text_input('Você conhece o mario? s/n: ').lower()
if m == 's':
    st.sidebar.image('sonicsus2.webp')
else:
    st.sidebar.image('s.png')


st.title('Jogos mais vendidos no mundo')
tab1, tab2, tab3, tab4, tab5 = st.tabs(['Gênero', 'Idade', 'Ano', 'vendas de jogos por ano', 'lançamentos por ano'])
with tab1:
    st.subheader('Por gênero')
    st.dataframe(df1.loc[:, ['Genre', 'Global_Sales', 'Name']].groupby('Genre').agg({'Global_Sales': 'max', 'Name': 'last'}).reset_index().sort_values('Global_Sales', ascending=False))
with tab2:
    st.subheader('Por Idade')
    st.dataframe(df1.loc[:, ['Rating', 'Global_Sales', 'Name']].groupby('Rating').agg({'Global_Sales': 'max', 'Name': 'last'}).reset_index().sort_values('Global_Sales', ascending=False))
with tab3:
    st.subheader('Por ano')
    st.dataframe(df1.loc[:, ['Year_of_Release', 'Global_Sales', 'Name']].groupby('Year_of_Release').agg({'Global_Sales': 'max', 'Name': 'last'}).reset_index().sort_values('Year_of_Release', ascending=False))
with tab4:
    st.subheader('Vendas por ano')
    df_aux = df1.loc[:, ['Year_of_Release', 'Global_Sales']].groupby('Year_of_Release').agg({'Global_Sales': 'sum'}).sort_values('Year_of_Release').reset_index()
    fig = px.bar(df_aux, x='Year_of_Release', y='Global_Sales')
    st.plotly_chart(fig)
    fig = px.line(df_aux, x='Year_of_Release', y='Global_Sales')
    st.plotly_chart(fig)
with tab5:
    st.subheader('Lançamentos por ano')
    df_aux = df1.loc[:, ['Year_of_Release', 'Name']].groupby('Year_of_Release').count().reset_index().sort_values('Year_of_Release', ascending=False)
    fig = px.bar(df_aux, x='Year_of_Release', y='Name')
    st.plotly_chart(fig)
    fig = px.line(df_aux, x='Year_of_Release', y='Name')
    st.plotly_chart(fig)