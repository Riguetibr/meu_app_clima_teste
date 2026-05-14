import streamlit as st
import requests
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO ---
API_KEY = "d02f718aeb19fadc0a02515451c9e180"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

st.set_page_config(page_title="Clima Pro", layout="wide")

# --- ESTILO ---
st.markdown("""
    <style>
    .stApp { background: #0e1117; }
    .caixa-central {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        padding: 20px;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        max-width: 550px;
        margin: auto;
        color: white;
    }
    .grid-previsao {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 20px;
        border-top: 1px solid rgba(255,255,255,0.1);
        padding-top: 15px;
    }
    .item-dia { flex: 1; text-align: center; }
    .borda-r { border-right: 1px solid rgba(255,255,255,0.1); }
    </style>
""", unsafe_allow_html=True)

# --- BUSCA ---
st.markdown("<h2 style='text-align: center; color: white;'>🌍 Monitor de Clima</h2>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    cidade = st.text_input("", placeholder="Digite a cidade e aperte Enter...", label_visibility="collapsed")

if cidade:
    try:
        # Dados Atuais
        res = requests.get(BASE_URL, params={"q": cidade, "appid": API_KEY, "units": "metric", "lang": "pt_br"}).json()
        # Previsão
        f_res = requests.get(FORECAST_URL, params={"q": cidade, "appid": API_KEY, "units": "metric", "lang": "pt_br"}).json()

        if res.get("cod") == 200:
            # Cálculos de tempo
            fuso = res.get('timezone')
            hora_local = datetime.now(pytz.utc) + timedelta(seconds=fuso)
            
            # Montando a Previsão (HTML limpo)
            dias_html = ""
            for i, idx in enumerate([8, 16, 24]):
                item = f_res['list'][idx]
                data = (hora_local + timedelta(days=i+1)).strftime("%d/%m")
                temp = int(item['main']['temp'])
                classe_borda = "borda-r" if i < 2 else ""
                
                dias_html += f"""
                <div class="item-dia {classe_borda}">
                    <p style="font-size: 11px; opacity: 0.7; margin:0;">{data}</p>
                    <p style="font-size: 20px; margin: 5px 0;">🌡️</p>
                    <p style="font-size: 16px; font-weight: bold; margin:0;">{temp}°C</p>
                </div>
                """

            # Layout Principal (Usando apenas UMA chamada de markdown para tudo)
            layout_html = f"""
            <div class="caixa-central">
                <p style="font-size: 14px; opacity: 0.8; margin: 0;">{res['name']}</p>
                <div style="display: flex; align-items: center; justify-content: center; gap: 20px; margin: 15px 0;">
                    <h1 style="font-size: 50px; margin: 0; color: white;">{int(res['main']['temp'])}°C</h1>
                    <div style="text-align: left; border-left: 1px solid rgba(255,255,255,0.3); padding-left: 15px;">
                        <p style="font-size: 18px; font-weight: bold; margin: 0; color: white;">{hora_local.strftime("%H:%M")}</p>
                        <p style="font-size: 12px; margin: 0; color: white; opacity: 0.7;">{res['weather'][0]['description'].upper()}</p>
                    </div>
                </div>
                
                <div style="display: flex; justify-content: space-around; background: rgba(0,0,0,0.2); padding: 10px; border-radius: 15px;">
                    <div><p style="font-size: 9px; opacity: 0.7; margin:0;">UMIDADE</p><p style="margin:0;">{res['main']['humidity']}%</p></div>
                    <div><p style="font-size: 9px; opacity: 0.7; margin:0;">VENTO</p><p style="margin:0;">{int(res['wind']['speed']*3.6)}km/h</p></div>
                </div>

                <div class="grid-previsao">
                    {dias_html}
                </div>
            </div>
            """
            st.markdown(layout_html, unsafe_allow_html=True)
        else:
            st.error("Cidade não encontrada.")
    except:
        st.error("Erro ao carregar dados.")
