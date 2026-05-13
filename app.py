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

# --- BANCO DE DADOS E DICIONÁRIOS ---
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

# --- FUNÇÕES AUXILIARES ---
def obter_emoji_clima(main_clima):
    mapeamento = {
        "Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️", "Drizzle": "🌦️", 
        "Thunderstorm": "⛈️", "Snow": "❄️", "Mist": "🌫️", "Fog": "🌫️"
    }
    return mapeamento.get(main_clima, "🌡️")

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
            padding: 30px; border-radius: 30px; border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center; margin: auto; color: white !important;
        }}
        h1, h2, h3, h4, p {{ color: white !important; font-family: 'sans-serif'; }}
        .font-hora {{ font-family: 'JetBrains Mono', monospace; font-size: 28px; }}
        .font-data {{ font-family: 'Roboto', sans-serif; font-weight: 300; font-size: 16px; text-transform: uppercase; letter-spacing: 2px; }}
        </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE BUSCA ---
if 'cidade_ativa' not in st.session_state: st.session_state.cidade_ativa = None

st.markdown("<h1 style='text-align: center;'>🌍 Monitor de Clima</h1>", unsafe_allow_html=True)

col_menu1, col_menu2, col_menu3 = st.columns([1, 2, 1])
with col_menu2:
    aba = st.radio("Menu", ["Dados do Clima", "Mapa de Radar"], horizontal=True, label_visibility="collapsed")
    busca = st.text_input("", placeholder="🔍 Digite a cidade...", label_visibility="collapsed")
    if busca: st.session_state.cidade_ativa = busca

if st.session_state.cidade_ativa:
    try:
        res = requests.get(BASE_URL, params={"q": st.session_state.cidade_ativa, "appid": API_KEY, "units": "metric", "lang": "pt_br"}).json()
        
        if res.get("cod") == 200:
            clima_principal = res['weather'][0]['main']
            fuso = res.get('timezone')
            hora_local = datetime.now(pytz.utc) + timedelta(seconds=fuso)
            aplicar_estilo(FOTOS_CLIMA.get(clima_principal, FOTOS_CLIMA["Default"]))

            if aba == "Dados do Clima":
                # --- BUSCA DE PREVISÃO ANTES PARA MONTAR O HTML ---
                f_res = requests.get(FORECAST_URL, params={"q": st.session_state.cidade_ativa, "appid": API_KEY, "units": "metric", "lang": "pt_br"}).json()
                
                html_proximos_dias = ""
                for i, idx in enumerate([8, 16, 24]):
                    item = f_res['list'][idx]
                    data_f = (hora_local + timedelta(days=i+1)).strftime("%d/%m")
                    emoji = obter_emoji_clima(item['weather'][0]['main'])
                    desc = item['weather'][0]['description'].title()
                    temp = int(item['main']['temp'])
                    
                    # Estilo de divisória minimalista
                    borda = "border-right: 1px solid rgba(255,255,255,0.15);" if i < 2 else ""
                    
                    html_proximos_dias += f"""
                    <div style="flex: 1; {borda} padding: 10px; text-align: center;">
                        <p style="font-size: 11px; opacity: 0.7; margin: 0;">{data_f}</p>
                        <p style="font-size: 28px; margin: 8px 0;">{emoji}</p>
                        <h3 style="margin: 0; font-size: 20px;">{temp}°C</h3>
                        <p style="font-size: 10px; opacity: 0.6; margin-top: 5px;">{desc}</p>
                    </div>
                    """

                # --- RENDERIZAÇÃO DO CARD ÚNICO ---
                st.markdown(f"""
                <div class="caixa-central" style="max-width: 650px;">
                    <p style="font-size: 14px; opacity: 0.8; margin-bottom: 5px;">{res['name']}, {res['sys']['country']}</p>
                    
                    <div style="display: flex; align-items: center; justify-content: center; gap: 25px; margin-bottom: 10px;">
                        <h1 style="font-size: 70px; margin: 0;">{int(res['main']['temp'])}°C</h1>
                        <div style="text-align: left; border-left: 1px solid rgba(255,255,255,0.3); padding-left: 15px;">
                            <p class="font-data" style="margin: 0; font-size: 12px;">{DIAS_SEMANA.get(hora_local.strftime("%A"))}</p>
                            <p class="font-hora" style="margin: 0; font-size: 22px;">{hora_local.strftime("%H:%M")}</p>
                        </div>
                    </div>
                    
                    <h2 style="margin-bottom: 20px; font-weight: 300;">{res['weather'][0]['description'].title()}</h2>
                    
                    <div style="display: flex; justify-content: space-around; background: rgba(0,0,0,0.2); padding: 12px; border-radius: 15px; margin-bottom: 30px;">
                        <div><p style="font-size: 10px; opacity: 0.7; margin: 0;">☁️ NUVENS</p><p style="margin: 0; font-size: 16px;">{res['clouds']['all']}%</p></div>
                        <div style="border-left: 1px solid rgba(255,255,255,0.1); border-right: 1px solid rgba(255,255,255,0.1); padding: 0 20px;">
                            <p style="font-size: 10px; opacity: 0.7; margin: 0;">💧 UMIDADE</p><p style="margin: 0; font-size: 16px;">{res['main']['humidity']}%</p>
                        </div>
                        <div><p style="font-size: 10px; opacity: 0.7; margin: 0;">🌬️ VENTO</p><p style="margin: 0; font-size: 16px;">{int(res['wind']['speed']*3.6)}km/h</p></div>
                    </div>

                    <h4 style="margin-bottom: 20px; letter-spacing: 2px; font-size: 12px; opacity: 0.9;">PREVISÃO PARA OS PRÓXIMOS DIAS</h4>
                    
                    <div style="display: flex; justify-content: center; align-items: center; width: 90%; margin: 0 auto;">
                        {html_proximos_dias}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            else:
                # --- TELA DE MAPA ---
                lat, lon = res['coord']['lat'], res['coord']['lon']
                st.markdown('<div class="caixa-central" style="max-width: 850px;">', unsafe_allow_html=True)
                m = folium.Map(location=[lat, lon], zoom_start=10, tiles="cartodbpositron")
                folium_static(m, width=750, height=450)
                st.markdown('</div>', unsafe_allow_html=True)

            st.write("")
            if st.button("⬅️ Voltar"):
                st.session_state.cidade_ativa = None
                st.rerun()
                
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
else:
    aplicar_estilo(FOTOS_CLIMA["Default"])
    st.markdown('<div class="caixa-central" style="max-width: 500px;"><h2>Olá! 👋</h2><p>Digite uma cidade para começar.</p></div>', unsafe_allow_html=True)
