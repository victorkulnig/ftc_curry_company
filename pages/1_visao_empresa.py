# Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

# bibliotecas necessárias
import folium
import pandas as pd
import streamlit as st
from PIL import Image
import datetime
from streamlit_folium import folium_static

st.set_page_config(page_title='Visão Empresa', page_icon='grafico', layout='wide')

# Import dataset
df = pd.read_csv( 'dataset/train.csv' )

df1 = df.copy()

# 1. convertando a coluna Age de texto para numero
linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ') 
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ') 
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['City'] != 'NaN ') 
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['Festival'] != 'NaN ') 
df1 = df1.loc[linhas_selecionadas, :].copy()

df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )

# 2. convertando a coluna Ratings de texto para numero decimal ( float )
df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )

# 3. convertando a coluna order_date de texto para data
df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y' )

# 4. convertendo multiple_deliveries de texto para numero inteiro ( int )
linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()
df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

## 5. Removendo os espacos dentro de strings/texto/object
#df1 = df1.reset_index( drop=True )
#for i in range( len( df1 ) ):
#  df1.loc[i, 'ID'] = df1.loc[i, 'ID'].strip()

# 6. Removendo os espacos dentro de strings/texto/object
df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

# 7. Limpando a coluna de time taken
df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min) ')[1] )
df1['Time_taken(min)']  = df1['Time_taken(min)'].astype( int )


# =======================================
# Barra Lateral
# =======================================
st.header( 'Marketplace - Visão Entregadoress' )

image = Image.open('logo.png' )
st.sidebar.image( image, width=120 )


st.sidebar.markdown('### Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""___""")

# Definindo as datas de início e fim no formato datetime
min_date = datetime.datetime(2022, 2, 11)
max_date = datetime.datetime(2022, 4, 6)
default_date = datetime.datetime(2022, 4, 2)

# Slider para selecionar uma data
date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=default_date,
    min_value=min_date,
    max_value=max_date)

# Formatar a data selecionada
formatted_date = date_slider.strftime('%d-%m-%Y')

st.sidebar.markdown("""___""")

traffic_options = st.sidebar.multiselect( 
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'], 
    default=['Low', 'Medium', 'High', 'Jam'] )

st.sidebar.markdown("""___""")
st.sidebar.markdown('### Powered by Victor Kulnig')

# Filtros de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas,:]

# Filtros de data
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas,:]


# =======================================
# Layout no Streamlit
# =======================================

tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'] )

with tab1:
    with st.container():
        # Order Metric
        st.markdown('# Orders by Day')
        cols = ['ID', 'Order_Date']

        # selecao de linhas
        df_aux = df1.loc[:, cols].groupby('Order_Date').count().reset_index()

        # desenhar o gráfico de linhas

        fig = px.bar( df_aux, x='Order_Date', y='ID')

        st.plotly_chart(fig, use_container_width=True)


    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.header('Traffic Order Share')
            columns = ['ID', 'Road_traffic_density']
            df_aux = df1.loc[:, columns].groupby( 'Road_traffic_density' ).count().reset_index()
            df_aux['perc_ID'] = 100 * ( df_aux['ID'] / df_aux['ID'].sum() )
            # gráfico
            fig = px.pie( df_aux, values='perc_ID', names='Road_traffic_density' )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.header('Traffic Order City')
            columns = ['ID', 'City', 'Road_traffic_density']
            df_aux = df1.loc[:, columns].groupby( ['City', 'Road_traffic_density'] ).count().reset_index()
            df_aux = df_aux.loc[df_aux['City'] != 'NaN', :]
            df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]
            # gráfico
            fig = px.scatter( df_aux, x='City', y='Road_traffic_density', size = 'ID', color='City')
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    with st.container():    
        st.markdown('# Order by Week')

        # Quantidade de pedidos por Semana
        df1['week_of_year'] = df1['Order_Date'].dt.strftime( "%U" )
        df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
        # gráfico
        fig = px.line( df_aux, x='week_of_year', y='ID' )
        st.plotly_chart(fig, use_container_width=True)
    with st.container():
        st.markdown('# Order Share by Week')
        # Quantas entregas na semana / Quantos entregadores únicos por semana
        df_aux1 = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
        df_aux2 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby( 'week_of_year').nunique().reset_index()
        df_aux = pd.merge( df_aux1, df_aux2, how='inner', on='week_of_year' )
        df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
        # gráfico
        fig = px.line( df_aux, x='week_of_year', y='order_by_delivery' )
        st.plotly_chart(fig, use_container_width=True)
with tab3:
    st.header('Country Maps')
    columns = [
    'City',
    'Road_traffic_density',
    'Delivery_location_latitude',
    'Delivery_location_longitude'
    ]
    columns_groupby = ['City', 'Road_traffic_density']
    data_plot = df1.loc[:, columns].groupby( columns_groupby ).median().reset_index()
    data_plot = data_plot.loc[data_plot['City'] != 'NaN', :]
    data_plot = data_plot.loc[data_plot['Road_traffic_density'] != 'NaN', :]
    # Desenhar o mapa
    map = folium.Map( zoom_start=11 )
    for index, location_info in data_plot.iterrows():
        folium.Marker( [location_info['Delivery_location_latitude'],
                        location_info['Delivery_location_longitude']],
                        popup=location_info[['City', 'Road_traffic_density']] ).add_to( map )
    folium_static(map, width=1024, height=600)

