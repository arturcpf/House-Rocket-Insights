import pandas as pd
import streamlit as st
import plotly.express as px


pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
pd.set_option('float_format','{:.2f}'.format)
st.set_page_config(layout='wide')

# FUNCTIONS
def get_data(path):
              
       data = pd.read_csv(path)
       return data

def set_feature(data):
       
       data['preço/m2']=data.apply(lambda x: x['price']/(x['sqft_living']*0.092903),axis=1)
       return None
def new_df (data):
       df = data[['zipcode','preço/m2']].groupby('zipcode').mean().reset_index()
       return df
def new_df2 (data, df):
       df2 = pd.merge(data,df,on='zipcode',how='inner')
       return df2
def rename_columns(df2):      
       df2.columns = ['id', 'date', 'price', 'bedrooms', 'bathrooms', 'sqft_living',
       'sqft_lot', 'floors', 'waterfront', 'view', 'condition', 'grade',
       'sqft_above', 'sqft_basement', 'yr_built', 'yr_renovated', 'zipcode',
       'lat', 'long', 'sqft_living15', 'sqft_lot15', 'preço/m2_do_imovel',
       'preço/m2_da_média_do_zipcode']
       return None

def new_feature_status (df2):
       df2['status']=df2.apply(lambda x: 'Compra' if (x['preço/m2_do_imovel']<=(1-in_desv)*x['preço/m2_da_média_do_zipcode']) & 
                                                 (x['condition']>=in_cond)
                                                 else '', axis = 1)
       return None

def mapa(df3):
       mapa = px.scatter_mapbox(df3, lat='lat',
                                   lon = 'long',
                                   hover_name='id',
                                   size = 'price',
                                   hover_data=['price'],
                                   color_discrete_sequence=['cornflowerblue'],
                                   zoom=9,
                                   height=300)
       mapa.update_layout (mapbox_style = 'open-street-map')
       mapa.update_layout(height=600, margin ={'r':0, 't':0,'l':0,'b':0})
       mapa
       return None
if __name__  == '__main__':
       #ETL
       # Data Extraction
       data = get_data('kc_house_data.csv')
       # Data Transformation
       set_feature(data)
       df = new_df(data)
       df2 = new_df2(data,df)
       rename_columns(df2)
       # Data Loading

       # Criando sidebar
       in_desv = st.sidebar.slider('Selecione uma desvalorização mínima do imóvel (%):', min_value = 0, value = 50, max_value = 100, step = 1)
       in_cond = st.sidebar.slider('Selecione um nível mínimo de condição do imóvel:', value = int((data['condition'].min()+data['condition'].max())/2), min_value = int(data['condition'].min()), max_value = int(data['condition'].max()), step = 1)
       

       # FATOR A ESCOLHER DE DESVALORIZAÇÃO DO IMÓVEL
       in_desv = in_desv/100

       new_feature_status(df2)
       
       df3 = df2.loc[df2['status']=='Compra']

       st.header('Data Analytics')
       st.subheader('Imóveis Filtrados') 
       st.dataframe(df3)
       st.subheader('Mapa dos imóveis')
       df3_mapa=df3[['id','lat','long','price',
                     'preço/m2_do_imovel',
                     'preço/m2_da_média_do_zipcode']]
       mapa(df3)