import streamlit as st
import requests

# --- CONFIGURAÇÃO DA API ---
API_KEY = "d02f718aeb19fadc0a02515451c9e180"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Clima Premium Global", layout="wide")

# Função para buscar dados da API
def buscar_clima(cidade):
    params = {
        "q": cidade,
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt_br"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    return None

# Função de Estilo (Mantendo sua estética original)
def aplicar_estilo(url_foto):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url("{url_foto}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .caixa-central {{
            background-color: rgba(255, 255, 255, 0.95);
            padding: 45px;
            border-radius: 25px;
            text-align: center;
            max-width: 500px;
            margin: auto;
            margin-top: 10vh;
            border: 1px solid #ddd;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- INTERFACE ---
st.markdown("<h1 style='text-align: center; color: white; text-shadow: 2px 2px 4px #000;'>🌍 Monitor de Clima Global</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Mudamos para text_input para você digitar QUALQUER cidade
    cidade_digitada = st.text_input("Digite o nome da cidade (ex: Londres, Tokyo, São Paulo):", "")

if cidade_digitada:
    dados = buscar_clima(cidade_digitada)
    
    if dados:
        nome_cidade = dados['name']
        temp = dados['main']['temp']
        condicao = dados['weather'][0]['description']
        clima_geral = dados['weather'][0]['main'] # Ex: Clear, Clouds, Rain
        
        # Lógica para mudar o fundo baseada no tipo de clima
        if clima_geral == "Clear":
            foto = "https://images.unsplash.com/photo-1506466010722-395aa2bef877?w=1200"
        elif clima_geral == "Clouds":
            foto = "https://images.unsplash.com/photo-1483702721041-b23de737a886?w=1200"
        elif clima_geral == "Rain":
            foto = "https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?w=1200"
        else:
            foto = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200"
            
        aplicar_estilo(foto)

        # Dicas inteligentes baseadas na temperatura real
        dicas = []
        if temp < 15: dicas.append("Melhor levar um casaco pesado! 🧥")
        elif temp < 22: dicas.append("Um agasalho leve resolve. 🧣")
        if temp > 28: dicas.append("Beba muita água e use protetor! 🧴")
        
        dica_texto = " | ".join(dicas)

        st.markdown(
            f"""
            <div class="caixa-central">
                <h2 style="color: #444; margin: 0;">{nome_cidade}</h2>
                <h1 style="font-size: 100px; color: #222; margin: 0;">{int(temp)}°C</h1>
                <p style="color: #666; font-size: 20px; text-transform: capitalize;">{condicao}</p>
                <p style="color: #d32f2f; font-size: 15px; font-weight: bold;">{dica_texto}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error("Cidade não encontrada! Tente digitar o nome corretamente.")
else:
    # Tela inicial antes de digitar
    aplicar_estilo("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200")
    st.markdown(
        """
        <div class="caixa-central">
            <h2 style="color: #333;">Aguardando sua busca...</h2>
            <p style="color: #777;">Digite o nome de uma cidade acima para ver o clima em tempo real.</p>
        </div>
        """,
        unsafe_allow_html=True
    )