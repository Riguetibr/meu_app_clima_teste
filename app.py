import streamlit as st
import requests
import random
from datetime import datetime

# --- CONFIGURAÇÃO DA API ---
API_KEY = "d02f718aeb19fadc0a02515451c9e180"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

st.set_page_config(page_title="Clima Pro", layout="wide")

# --- BANCO DE CIDADES ---
CAPITAIS_SUGESTOES = [
    "Brasília", "São Paulo", "Rio de Janeiro", "Londres", "Paris", 
    "Tóquio", "Nova York", "Lisboa", "Roma", "Berlim", 
    "Madrid", "Buenos Aires", "Montevidéu", "Cairo", "Pequim", 
    "Moscou", "Atenas", "Washington", "Ottawa", "Sidney"
]

# --- BIBLIOTECA DE LINKS ---
FOTOS_CLIMA = {
    "Clear": "https://plus.unsplash.com/premium_photo-1733306531071-087c077e1502?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", 
    "Clouds": "https://images.unsplash.com/photo-1534088568595-a066f410bcda?q=80&w=1920", 
    "Rain": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?q=80&w=1920", 
    "Thunderstorm": "https://images.unsplash.com/photo-1559087867-ce4c91325525?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", 
    "Snow": "https://images.unsplash.com/photo-1477601263568-180e2c6d046e?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", 
    "Mist": "https://images.unsplash.com/photo-1485236715568-ddc5ee6ca227?q=80&w=1920", 
    "Fog": "https://images.unsplash.com/photo-1485236715568-ddc5ee6ca227?q=80&w=1920",
    "Default": "https://images.unsplash.com/photo-1778483154534-8290a142eb2d?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
}

def aplicar_estilo(url_foto):
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("{url_foto}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .caixa-central {{
            background: rgba(255, 255, 255, 0.1); 
            backdrop-filter: blur(20px);
            padding: 35px;
            border-radius: 25px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center;
            max-width: 600px;
            margin: auto;
        }}
        .card-sugestao {{
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(15px);
            padding: 20px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
        }}
        h1, h2, h3, p {{ color: white !important; font-family: 'sans-serif'; }}
        .metric-container {{
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 15px;
        }}
        .voltar-btn-container {{
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }}
        </style>
    """, unsafe_allow_html=True)

def card_mini_clima(cidade_nome):
    params = {"q": cidade_nome, "appid": API_KEY, "units": "metric", "lang": "pt_br"}
    try:
        r = requests.get(BASE_URL, params=params).json()
        temp = int(r['main']['temp'])
        clima_tipo = r['weather'][0]['main']
        icons = {"Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️", "Thunderstorm": "⛈️", "Snow": "❄️"}
        icon = icons.get(clima_tipo, "🌍")
        st.markdown(f"""
            <div class="card-sugestao">
                <p style="margin:0; font-size: 14px; opacity: 0.7;">{cidade_nome.upper()}</p>
                <h2 style="margin: 10px 0;">{icon} {temp}°C</h2>
                <p style="margin:0; font-size: 13px;">{r['weather'][0]['description'].title()}</p>
            </div>
        """, unsafe_allow_html=True)
    except:
        pass

# --- CONTROLE DE ESTADO ---
if 'cidade_ativa' not in st.session_state:
    st.session_state.cidade_ativa = None

st.markdown("<h1 style='text-align: center; margin-bottom: 20px;'>🌍 Monitor de Clima</h1>", unsafe_allow_html=True)

# Barra de busca (Sempre visível ou limpa ao voltar)
c_in1, c_in2, c_in3 = st.columns([1, 2, 1])
with c_in2:
    busca = st.text_input("", placeholder="🔍 Digite a cidade...", label_visibility="collapsed", key="search_input")
    if busca:
        st.session_state.cidade_ativa = busca

# --- LÓGICA DE EXIBIÇÃO ---
if st.session_state.cidade_ativa:
    params = {"q": st.session_state.cidade_ativa, "appid": API_KEY, "units": "metric", "lang": "pt_br"}
    try:
        res = requests.get(BASE_URL, params=params).json()
        if res.get("cod") == 200:
            clima = res['weather'][0]['main']
            temp = int(res['main']['temp'])
            desc = res['weather'][0]['description']
            humidade = res['main']['humidity']
            nuvens = res['clouds']['all']
            
            # Data e Hora Atual
            agora = datetime.now()
            data_formatada = agora.strftime("%d/%m/%Y")
            hora_formatada = agora.strftime("%H:%M")
            
            aplicar_estilo(FOTOS_CLIMA.get(clima, FOTOS_CLIMA["Default"]))
            icones = {"Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️", "Thunderstorm": "⛈️", "Snow": "❄️"}
            icon = icones.get(clima, "🌍")
            dica = "Hidrate-se 💧" if temp > 25 else "Agasalhe-se 🧥" if temp < 15 else "Clima agradável 😎"

            st.markdown(f"""
                <div class="caixa-central">
                    <p style="font-size: 18px; opacity: 0.8; margin: 0;">{res['name']}</p>
                    <div style="display: flex; align-items: center; justify-content: center; gap: 20px;">
                        <h1 style="font-size: 90px; margin: 0;">{temp}°C</h1>
                        <div style="text-align: left; border-left: 2px solid rgba(255,255,255,0.3); padding-left: 15px;">
                            <p style="margin:0; font-size: 16px; font-weight: bold;">{data_formatada}</p>
                            <p style="margin:0; font-size: 24px; letter-spacing: 1px;">{hora_formatada}</p>
                        </div>
                    </div>
                    <h2 style="margin: 10px 0 20px 0;">{icon} {desc.title()}</h2>
                    <div class="metric-container">
                        <div style="flex:1;">
                            <p style="margin:0; font-size: 12px; opacity: 0.7;">☁️ Nuvens</p>
                            <p style="margin:0; font-size: 18px; font-weight: bold;">{nuvens}%</p>
                        </div>
                        <div style="flex:1; border-left: 1px solid rgba(255,255,255,0.2); border-right: 1px solid rgba(255,255,255,0.2);">
                            <p style="margin:0; font-size: 12px; opacity: 0.7;">💧 Umidade</p>
                            <p style="margin:0; font-size: 18px; font-weight: bold;">{humidade}%</p>
                        </div>
                        <div style="flex:1;">
                            <p style="margin:0; font-size: 12px; opacity: 0.7;">💡 Dica</p>
                            <p style="margin:0; font-size: 15px; font-weight: bold;">{dica}</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Botão Centralizado
            st.write("") # Espaçador
            col_b1, col_b2, col_b3 = st.columns([1, 0.4, 1])
            with col_b2:
                if st.button("⬅️ Voltar", use_container_width=True):
                    st.session_state.cidade_ativa = None
                    st.rerun()
        else:
            st.error("Cidade não encontrada.")
            if st.button("Voltar ao Início"):
                st.session_state.cidade_ativa = None
                st.rerun()
    except:
        st.error("Erro na conexão.")
else:
    # TELA INICIAL
    aplicar_estilo(FOTOS_CLIMA["Default"])
    st.markdown("""
        <div class="caixa-central" style="margin-bottom: 50px;">
            <h2 style="font-size: 30px;">Seja Bem-vindo! 👋</h2>
            <p style="opacity: 0.9;">Descubra o clima em qualquer lugar do mundo agora mesmo.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sorteio Aleatório
    cidades_sorteadas = random.sample(CAPITAIS_SUGESTOES, 3)
    st.markdown("<h3 style='text-align: center; margin-bottom: 20px; font-size: 18px;'>Destaques do Momento 🌍</h3>", unsafe_allow_html=True)
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1: card_mini_clima(cidades_sorteadas[0])
    with col_s2: card_mini_clima(cidades_sorteadas[1])
    with col_s3: card_mini_clima(cidades_sorteadas[2])