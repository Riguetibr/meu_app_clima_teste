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

# --- BANCO DE DADOS ---
CAPITAIS_SUGESTOES = ["Brasília", "São Paulo", "Rio de Janeiro", "Londres", "Paris", "Tóquio", "Nova York"]
DIAS_SEMANA = {"Monday": "Segunda-feira", "Tuesday": "Terça-feira", "Wednesday": "Quarta-feira", "Thursday": "Quinta-feira", "Friday": "Sexta-feira", "Saturday": "Sábado", "Sunday": "Domingo"}
FOTOS_CLIMA = {
    "Clear": "https://plus.unsplash.com/premium_photo-1733306531071-087c077e1502?q=80&w=1170&auto=format&fit=crop", 
    "Clouds": "https://images.unsplash.com/photo-1534088568595-a066f410bcda?q=80&w=1920", 
    "Rain": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?q=80&w=1920", 
    "Default": "https://images.unsplash.com/photo-1778483154534-8290a142eb2d?q=80&w=1170&auto=format&fit=crop"
}

def obter_emoji(main):
    return {"Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️", "Drizzle": "🌦️", "Thunderstorm": "⛈️", "Snow": "❄️"}.get(main, "🌡️")

def aplicar_estilo(url):
    st.markdown(f"""
        <style>
        .stApp {{ background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("{url}"); background-size: cover; background-attachment: fixed; }}
        .caixa-central {{ background: rgba(255, 255, 255, 0.12); backdrop-filter: blur(25px); padding: 25px; border-radius: 30px; border: 1px solid rgba(255, 255, 255, 0.2); text-align: center; margin: auto; }}
        h1, h2, h3, h4, p {{ color: white !important; font-family: 'sans-serif'; margin: 0; }}
        </style>
    """, unsafe_allow_html=True)

if 'cidade_ativa' not in st.session_state: st.session_state.cidade_ativa = None

st.markdown("<h1 style='text-align: center; margin-bottom:20px;'>🌍 Monitor de Clima</h1>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    aba = st.radio("Menu", ["Dados", "Mapa"], horizontal=True, label_visibility="collapsed")
    busca = st.text_input("", placeholder="🔍 Digite a cidade...", label_visibility="collapsed")
    if busca: st.session_state.cidade_ativa = busca

if st.session_state.cidade_ativa:
    try:
        res = requests.get(BASE_URL, params={"q": st.session_state.cidade_ativa, "appid": API_KEY, "units": "metric", "lang": "pt_br"}).json()
        if res.get("cod") == 200:
            fuso = res.get('timezone')
            hora_local = datetime.now(pytz.utc) + timedelta(seconds=fuso)
            aplicar_estilo(FOTOS_CLIMA.get(res['weather'][0]['main'], FOTOS_CLIMA["Default"]))

            if aba == "Dados":
                # --- BUSCA PREVISÃO ---
                f_res = requests.get(FORECAST_URL, params={"q": st.session_state.cidade_ativa, "appid": API_KEY, "units": "metric", "lang": "pt_br"}).json()
                
                # Montando os 3 dias (HTML Limpo para evitar erro de código branco)
                cards_html = ""
                for i, idx in enumerate([8, 16, 24]):
                    item = f_res['list'][idx]
                    emoji = obter_emoji(item['weather'][0]['main'])
                    borda = "border-right: 1px solid rgba(255,255,255,0.15);" if i < 2 else ""
                    cards_html += f"""
                    <div style="flex: 1; {borda} padding: 5px;">
                        <p style="font-size: 11px; opacity: 0.7;">{(hora_local + timedelta(days=i+1)).strftime("%d/%m")}</p>
                        <p style="font-size: 22px; margin: 5px 0;">{emoji}</p>
                        <p style="font-size: 18px; font-weight: bold;">{int(item['main']['temp'])}°C</p>
                    </div>"""

                # --- RENDERIZAÇÃO FINAL ---
                st.markdown(f"""
                <div class="caixa-central" style="max-width: 600px;">
                    <p style="font-size: 14px; opacity: 0.8;">{res['name']}</p>
                    <div style="display: flex; align-items: center; justify-content: center; gap: 20px; margin: 10px 0;">
                        <h1 style="font-size: 60px;">{int(res['main']['temp'])}°C</h1>
                        <div style="text-align: left; border-left: 1px solid rgba(255,255,255,0.3); padding-left: 15px;">
                            <p style="font-size: 12px; letter-spacing: 2px;">{DIAS_SEMANA.get(hora_local.strftime("%A"))}</p>
                            <p style="font-size: 20px; font-weight: bold;">{hora_local.strftime("%H:%M")}</p>
                        </div>
                    </div>
                    <h2 style="font-weight: 300; margin-bottom: 20px;">{res['weather'][0]['description'].title()}</h2>
                    
                    <div style="display: flex; justify-content: space-around; background: rgba(0,0,0,0.2); padding: 10px; border-radius: 15px; margin-bottom: 25px;">
                        <div><p style="font-size: 9px; opacity: 0.7;">NUVENS</p><p>{res['clouds']['all']}%</p></div>
                        <div style="border-left: 1px solid rgba(255,255,255,0.1); border-right: 1px solid rgba(255,255,255,0.1); padding: 0 15px;">
                            <p style="font-size: 9px; opacity: 0.7;">UMIDADE</p><p>{res['main']['humidity']}%</p>
                        </div>
                        <div><p style="font-size: 9px; opacity: 0.7;">VENTO</p><p>{int(res['wind']['speed']*3.6)}km/h</p></div>
                    </div>

                    <p style="font-size: 11px; letter-spacing: 2px; opacity: 0.9; margin-bottom: 15px;">PREVISÃO PRÓXIMOS DIAS</p>
                    <div style="display: flex; justify-content: center; width: 100%;">
                        {cards_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="caixa-central" style="max-width: 800px;">', unsafe_allow_html=True)
                folium_static(folium.Map(location=[res['coord']['lat'], res['coord']['lon']], zoom_start=10), width=700, height=400)
                st.markdown('</div>', unsafe_allow_html=True)

            if st.button("⬅️ Voltar"):
                st.session_state.cidade_ativa = None
                st.rerun()
    except: st.error("Erro na busca.")
else:
    aplicar_estilo(FOTOS_CLIMA["Default"])
    st.markdown('<div class="caixa-central" style="max-width: 400px;"><h2>Olá! 👋</h2><p>Digite uma cidade.</p></div>', unsafe_allow_html=True)
