import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon='🏠'
)

image = Image.open( 'logo.png' )
st.sidebar.image( image, width=120 )

st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """---""" )

st.write('# Cury Company Growth Dashboard')

st.markdown(
    """
    O Growth Dashboard foi construído para acompanhar as métricas de crescimento dos entregadores e restaurantes.
    
    ### Como utilizar o Growth Dashboard?
    - **Visão Empresa:**
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
        
    - **Visão Entregador:**
        - Acompanhamento dos indicadores semanais de crescimento.
        
    - **Visão Restaurante:**
        - Indicadores semanais de crescimento dos restaurantes.
        
    ### Precisa de ajuda?
    - Time de Data Science no Discord
        - @victorkulnig
    """
)
