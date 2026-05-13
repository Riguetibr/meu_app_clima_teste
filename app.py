import streamlit as st
import requests

# --- CONFIGURAÇÃO DA API ---
API_KEY = "d02f718aeb19fadc0a02515451c9e180"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Clima Pro Ultra", layout="wide")

# --- BIBLIOTECA DE GIFS E IMAGENS ---
# Você pode misturar .jpg e .gif aqui sem problemas!
FOTOS_CLIMA = {
    "Clear": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueXFid3B6Z3B6Z3B6Z3B6Z3B6Z3B6Z3B6Z3B6Z3B6Z3B6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/01o9WCMW7m2znSayGO/giphy.gif", # Exemplo de Sol
    "Clouds": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueXFid3B6Z3B6Z3B6Z3B6Z3B6Z3B6Z3B6Z3B6Z3B6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/u01ioCe6GQNpL51LMR/giphy.gif", # Exemplo de Nuvens
    "Rain": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueXFid3B6Z3B6Z3B6Z3B6Z3B6Z3B6Z3B6Z3B6Z3B6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/t7Qb8655Z1VfBGr5XB/giphy.gif", # Exemplo de Chuva
    "Snow": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueXFid3B6Z3B6Z3B6Z3B6Z3B6Z3B6Z3B6Z3B6Z3B6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/129NVCr1UfsGTS/giphy.gif", # Exemplo de Neve
    "Thunderstorm": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueXFid3B6Z3B6Z3B6Z3B6Z3B6Z3B6Z3B6Z3B6Z3B6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/iLpky2P3E3u1S/giphy.gif",
    "Default": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=1920"
}

def aplicar_estilo(url_foto):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("{url_foto}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            transition: background 1s ease-in-out;
        }}
        .caixa-central {{
            background: rgba(255, 255, 255, 0.1); 
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            padding: 40px;
            border-radius: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center;
            max-width: 550px;
            margin: auto;
            margin-top: 3vh;
        }}
        .stTextInput > div > div > input {{
            color: #111111 !important; 
            background-color: rgba(255, 255, 255, 0.9) !important;
            border-radius: 12px !important;
        }}
        h1, h2, h3, p, span {{
            color: white !important;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.8) !important;
        }}
        .metric-container {{
            display: flex !important;
            flex-direction: row !important;
            justify-content: space-around !important;
            margin-top: 25px;
            background: rgba(0, 0, 0, 0.3);
            padding: 20px;
            border-radius: 20px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.markdown("<h1 style='text-align: center;'>🌍 Monitor de Clima Global</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    cidade = st.text_input("Pesquise uma cidade", label_visibility="collapsed", placeholder="🔍 Digite a cidade...")

if not cidade:
    aplicar_estilo(FOTOS_CLIMA["Default"])
    st.markdown('<div class="caixa-central"><h2>Olá! 🌍</h2><p>Coloque o nome da cidade acima e veja seu clima</p></div>', unsafe_allow_html=True)
else:
    params = {"q": cidade, "appid": API_KEY, "units": "metric", "lang": "pt_br"}
    try:
        response = requests.get(BASE_URL, params=params)
        dados = response.json()
        if response.status_code == 200:
            clima_main = dados['weather'][0]['main']
            url_fundo = FOTOS_CLIMA.get(clima_main, FOTOS_CLIMA["Default"])
            aplicar_estilo(url_fundo)
            
            # (O restante do código de exibição continua igual...)
            st.success(f"Clima em {dados['name']} carregado com fundo animado!")
            # Reutilize aqui aquele bloco de st.markdown(html_content) das mensagens anteriores
        else:
            st.error("Cidade não encontrada.")
    except:
        st.error("Erro de conexão.")