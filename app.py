import streamlit as st
import requests
import random
from datetime import datetime, timedelta
import pytz
import folium
from streamlit_folium import folium_static

# --- CONFIGURAÇÃO DA API ---
API_KEY = "d02f718aeb19fadc0a02515451c9e180"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

st.set_page_config(page_title="Clima Pro", layout="wide")

# --- BANCO DE CIDADES ---
CAPITAIS_SUGESTOES = [
    "Brasília", "São Paulo", "Rio de Janeiro", "Londres", "Paris", 
    "Tóquio", "Nova York", "Lisboa", "Roma", "Berlim", 
    "Madrid", "Buenos Aires", "Montevidéu", "Cairo", "Pequim", 
    "Moscou", "Atenas", "Washington", "Ottawa", "Sidney"
]

DIAS_SEMANA = {
    "Monday": "Segunda-feira", "Tuesday": "Terça-feira", "Wednesday": "Quarta-feira",
    "Thursday": "Quinta-feira", "Friday": "Sexta-feira", "Saturday": "Sábado", "Sunday": "Domingo"
}

FOTOS_CLIMA = {
    "Clear": "https://plus.unsplash.com/premium_photo-1733306531071-087c077e1502?q=80&w=1170&auto=format&fit=crop", 
    "Clouds": "https://images.unsplash.com/photo-1534088568595-a066f410bcda?q=80&w=1920", 
    "Rain": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?q=80&w=1920", 
    "Thunderstorm": "https://images.unsplash.com/photo-1559087867-ce4c91325525?q=80&w=1170&auto=format&fit=crop", 
    "Snow": "https://images.unsplash.com/photo-1477601263568-180e2c6d046e?q=80&w=1170&auto=format&fit=crop", 
    "Default": "https://images.unsplash.com/photo-1778483154534-8290a142eb2d?q=80&w=1170&auto=format&fit=crop"
}

def aplicar_estilo(url_foto):
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500&family=Roboto:wght@100;300;500&display=swap');
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("{url_foto}");
            background-size: cover; background-position: center; background-attachment: fixed;
        }}
        .caixa-central {{
            background: rgba(255, 255, 255, 0.12); backdrop-filter: blur(25px);
            padding: 35px; border-radius: 30px; border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center; margin: auto;
        }}
        /* Centralização forçada para o iframe do mapa */
        iframe {{
            border-radius: 20px;
            display: block;
            margin: 0 auto;
        }}
        .card-previsao {{
            background: rgba(255, 255, 255, 0.08); padding: 15px; border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1); text-align: center;
        }}
        h1, h2, h3, p {{ color: white !important; font-family: 'sans-serif'; }}
        .font-hora {{ font-family: 'JetBrains Mono', monospace; font-size: 28px; }}
        .font-data {{ font-family: 'Roboto', sans-serif; font-weight: 300; font-size: 16px; text-transform: uppercase; letter-spacing: 2px; }}
        
        div.stButton > button {{
            background-color: rgba(255, 255, 255, 0.15) !important; color: white !important;
            border: 2px solid rgba(255, 255, 255, 0.5) !important; border-radius: 12px !important;
            padding: 10px 25px !important; font-weight: bold !important;
        }}
        </style>
    """, unsafe_allow_html=True)

def card_mini_clima(cidade_nome):
    params = {"q": cidade_nome, "appid": API_KEY, "units": "metric", "lang": "pt_br"}
    try:
        r = requests.get(BASE_URL, params=params).json()
        temp = int(r['main']['temp'])
        st.markdown(f"""<div style="background:rgba(255,255,255,0.08); padding:20px; border-radius:20px; text-align:center; border:1px solid rgba(255,255,255,0.1);">
            <p style="margin:0; font-size:12px; opacity:0.6;">{cidade_nome.upper()}</p>
            <h2 style="margin:8px 0; color:white;">{temp}°C</h2></div>""", unsafe_allow_html=True)
    except: pass

# --- CONTROLE DE ESTADO ---
if 'cidade_ativa' not in st.session_state: st.session_state.cidade_ativa = None

st.markdown("<h1 style='text-align: center; margin-bottom: 20px;'>🌍 Monitor de Clima</h1>", unsafe_allow_html=True)

# Layout Superior de Busca e Menu
col_menu1, col_menu2, col_menu3 = st.columns([1, 2, 1])
with col_menu2:
    aba_selecionada = st.radio("Escolha a visualização:", ["Dados do Clima", "Mapa de Radar"], horizontal=True, label_visibility="collapsed")
    busca = st.text_input("", placeholder="🔍 Digite a cidade...", label_visibility="collapsed", key=f"input_{st.session_state.cidade_ativa}")
    if busca: st.session_state.cidade_ativa = busca

if st.session_state.cidade_ativa:
    try:
        res = requests.get(BASE_URL, params={"q": st.session_state.cidade_ativa, "appid": API_KEY, "units": "metric", "lang": "pt_br"}).json()
        
        if res.get("cod") == 200:
            clima = res['weather'][0]['main']
            fuso = res.get('timezone')
            hora_local = datetime.now(pytz.utc) + timedelta(seconds=fuso)
            dia_semana_pt = DIAS_SEMANA.get(hora_local.strftime("%A"), hora_local.strftime("%A"))
            
            aplicar_estilo(FOTOS_CLIMA.get(clima, FOTOS_CLIMA["Default"]))

            if aba_selecionada == "Dados do Clima":
                # --- TELA DE DADOS ---
                st.markdown(f"""
                    <div class="caixa-central" style="max-width: 750px;">
                        <p style="font-size: 18px; opacity: 0.7; margin-bottom: 10px;">{res['name']}, {res['sys']['country']}</p>
                        <div style="display: flex; align-items: center; justify-content: center; gap: 30px;">
                            <h1 style="font-size: 100px; margin: 0;">{int(res['main']['temp'])}°C</h1>
                            <div style="text-align: left; border-left: 1px solid rgba(255,255,255,0.3); padding-left: 20px;">
                                <p class="font-data" style="margin:0; font-weight: 500;">{dia_semana_pt}</p>
                                <p class="font-data" style="margin:0;">{hora_local.strftime("%d %b %Y")}</p>
                                <p class="font-hora" style="margin:0;">{hora_local.strftime("%H:%M")}</p>
                            </div>
                        </div>
                        <h2 style="margin: 20px 0;">{res['weather'][0]['description'].title()}</h2>
                        <div style="display: flex; justify-content: space-around; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 15px; margin-bottom: 30px;">
                            <div><p style="font-size:12px; opacity:0.7; margin:0;">☁️ Nuvens</p><p style="font-size:20px; font-weight:bold; margin:0;">{res['clouds']['all']}%</p></div>
                            <div style="border-left:1px solid rgba(255,255,255,0.2); border-right:1px solid rgba(255,255,255,0.2); padding: 0 20px;"><p style="font-size:12px; opacity:0.7; margin:0;">💧 Umidade</p><p style="font-size:20px; font-weight:bold; margin:0;">{res['main']['humidity']}%</p></div>
                            <div><p style="font-size:12px; opacity:0.7; margin:0;">🌬️ Vento</p><p style="font-size:20px; font-weight:bold; margin:0;">{int(res['wind']['speed']*3.6)}km/h</p></div>
                        </div>
                        <h4 style="text-align: left; margin-bottom: 15px; opacity: 0.8;">Previsão para os próximos dias</h4>
                """, unsafe_allow_html=True)

                f_res = requests.get(FORECAST_URL, params={"q": st.session_state.cidade_ativa, "appid": API_KEY, "units": "metric", "lang": "pt_br"}).json()
                c1, c2, c3 = st.columns(3)
                for i, idx in enumerate([8, 16, 24]):
                    f_item = f_res['list'][idx]
                    f_data = (hora_local + timedelta(days=i+1)).strftime("%d/%m")
                    with [c1, c2, c3][i]:
                        st.markdown(f"""<div class="card-previsao">
                            <p style="margin:0; font-size:13px; font-weight:bold; opacity:0.7;">{f_data}</p>
                            <h3 style="margin:10px 0;">{int(f_item['main']['temp'])}°C</h3>
                            <p style="margin:0; font-size:11px;">{f_item['weather'][0]['description'].title()}</p>
                        </div>""", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            else:
                # --- TELA DE MAPA EXCLUSIVO CENTRALIZADO ---
                col_mapa_1, col_mapa_2, col_mapa_3 = st.columns([0.1, 5, 0.1])
                
                with col_mapa_2:
                    st.markdown('<div class="caixa-central" style="max-width: 950px;">', unsafe_allow_html=True)
                    lat, lon = res['coord']['lat'], res['coord']['lon']
                    m = folium.Map(location=[lat, lon], zoom_start=10, tiles="cartodbpositron")

                    folium.raster_layers.TileLayer(
                        tiles=f"https://tile.openweathermap.org/map/clouds_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
                        attr="OpenWeather", name="Nuvens", overlay=True
                    ).add_to(m)

                    folium_static(m, width=880, height=600)
                    st.markdown('</div>', unsafe_allow_html=True)

            # Botão Voltar
            st.write("")
            col_b1, col_b2, col_b3 = st.columns([1, 0.4, 1])
            with col_b2:
                if st.button("⬅️ Voltar", use_container_width=True):
                    st.session_state.cidade_ativa = None
                    st.rerun()
        else:
            st.error("Cidade não encontrada.")
    except: st.error("Erro na conexão.")
else:
    aplicar_estilo(FOTOS_CLIMA["Default"])
    st.markdown('<div class="caixa-central" style="max-width: 750px;"><h2>Olá! 👋</h2><p>Pesquise uma cidade para ver o clima e o mapa.</p></div>', unsafe_allow_html=True)
    cidades = random.sample(CAPITAIS_SUGESTOES, 3)
    st.write("")
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1: card_mini_clima(cidades[0])
    with col_s2: card_mini_clima(cidades[1])
    with col_s3: card_mini_clima(cidades[2])
