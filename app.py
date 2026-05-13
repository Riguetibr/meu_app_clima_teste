import streamlit as st
import requests

# --- CONFIGURAÇÃO DA API ---
API_KEY = "d02f718aeb19fadc0a02515451c9e180"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

st.set_page_config(page_title="Clima Pro", layout="wide")

# --- BIBLIOTECA CURADA (Imagens HD que não quebram) ---
FOTOS_CLIMA = {
    "Clear": "https://plus.unsplash.com/premium_photo-1733306531071-087c077e1502?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", # Sol limpo e suave
    "Clouds": "https://unsplash.com/pt-br/fotografias/clousd-branco-ZaCPb3xIqrg", # Nuvens volumosas cinematográficas
    "Rain": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?q=80&w=1920", # Chuva estética em janela
    "Thunderstorm": "https://images.unsplash.com/photo-1559087867-ce4c91325525?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", # Tempestade épica
    "Snow": "https://images.unsplash.com/photo-1477601263568-180e2c6d046e?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", # Neve real HD
    "Mist": "https://images.unsplash.com/photo-1485236715568-ddc5ee6ca227?q=80&w=1920", # Neblina limpa
    "Fog": "https://images.unsplash.com/photo-1485236715568-ddc5ee6ca227?q=80&w=1920",
    "Default": "https://images.unsplash.com/photo-1778483154534-8290a142eb2d?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
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