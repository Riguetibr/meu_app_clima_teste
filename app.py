import streamlit as st
import requests

# Configurações iniciais
API_KEY = "d02f718aeb19fadc0a02515451c9e180"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

st.set_page_config(page_title="Clima Premium", layout="wide")

# Função para aplicar o visual
def aplicar_estilo(url_foto):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("{url_foto}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .caixa-central {{
            background-color: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            max-width: 500px;
            margin: auto;
            margin-top: 5vh;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.markdown("<h1 style='text-align: center; color: white; text-shadow: 2px 2px 4px #000;'>🌍 Monitor de Clima Global</h1>", unsafe_allow_html=True)

# Campo de busca
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    cidade = st.text_input("📍 Digite o nome de uma cidade:", placeholder="Ex: Rio de Janeiro, Tokyo, Paris...")

if cidade:
    # Buscando os dados na API
    params = {
        "q": cidade,
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt_br"
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        dados = response.json()

        if response.status_code == 200:
            nome = dados['name']
            temp = dados['main']['temp']
            condicao = dados['weather'][0]['description']
            
            # Imagem de fundo padrão (pode ser personalizada depois)
            aplicar_estilo("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200")

            st.markdown(
                f"""
                <div class="caixa-central">
                    <h2 style="color: #333; margin-bottom: 0;">{nome}</h2>
                    <h1 style="font-size: 80px; color: #111; margin: 10px 0;">{int(temp)}°C</h1>
                    <p style="color: #666; font-size: 22px; text-transform: capitalize;">{condicao}</p>
                    <hr>
                    <p style="color: #ff4b4b; font-weight: bold;">API Conectada com Sucesso! ✅</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("Ops! Não encontrei essa cidade. Verifique se o nome está correto.")
            aplicar_estilo("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200")
    except:
        st.error("Houve um erro ao conectar com o serviço de clima.")
else:
    # Tela Inicial
    aplicar_estilo("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200")
    st.markdown(
        """
        <div class="caixa-central">
            <h2 style="color: #333;">Bem-vindo!</h2>
            <p style="color: #777;">Digite uma cidade acima para ver a temperatura agora.</p>
        </div>
        """,
        unsafe_allow_html=True
    )