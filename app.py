import streamlit as st
import requests

# --- CONFIGURAÇÃO DA API ---
API_KEY = "d02f718aeb19fadc0a02515451c9e180"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

st.set_page_config(page_title="Clima Pro", layout="wide")

# --- BIBLIOTECA CURADA (Imagens HD que não quebram) ---
FOTOS_CLIMA = {
    "Clear": "https://images.unsplash.com/photo-1506452819137-0422416856b8?q=80&w=1920", # Sol limpo e suave
    "Clouds": "https://images.unsplash.com/photo-1534088568595-a066f410bcda?q=80&w=1920", # Nuvens volumosas cinematográficas
    "Rain": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?q=80&w=1920", # Chuva estética em janela
    "Thunderstorm": "https://images.unsplash.com/photo-1605727281914-5570a9a24d97?q=80&w=1920", # Tempestade épica
    "Snow": "https://images.unsplash.com/photo-1478265409131-1f65c88f965c?q=80&w=1920", # Neve real HD
    "Mist": "https://images.unsplash.com/photo-1485236715568-ddc5ee6ca227?q=80&w=1920", # Neblina limpa
    "Fog": "https://images.unsplash.com/photo-1485236715568-ddc5ee6ca227?q=80&w=1920",
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
        }}
        .caixa-central {{
            background: rgba(255, 255, 255, 0.1); 
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            padding: 40px;
            border-radius: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center;
            max-width: 500px;
            margin: auto;
            margin-top: 5vh;
        }}
        h1, h2, p {{ color: white !important; font-family: 'sans-serif'; }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.markdown("<h1 style='text-align: center;'>🌍 Monitor de Clima</h1>", unsafe_allow_html=True)
cidade = st.text_input("", placeholder="Digite a cidade...")

if cidade:
    params = {"q": cidade, "appid": API_KEY, "units": "metric", "lang": "pt_br"}
    try:
        res = requests.get(BASE_URL, params=params).json()
        if res.get("cod") == 200:
            clima = res['weather'][0]['main']
            temp = res['main']['temp']
            desc = res['weather'][0]['description']
            
            aplicar_estilo(FOTOS_CLIMA.get(clima, FOTOS_CLIMA["Default"]))
            
            st.markdown(f"""
                <div class="caixa-central">
                    <p style="font-size: 20px;">{res['name']}</p>
                    <h1 style="font-size: 80px; margin: 0;">{int(temp)}°C</h1>
                    <h2>{desc.title()}</h2>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Cidade não encontrada.")
    except:
        st.error("Erro na conexão.")
else:
    aplicar_estilo(FOTOS_CLIMA["Default"])