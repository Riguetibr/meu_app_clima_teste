import streamlit as st
import requests

# --- CONFIGURAÇÃO DA API ---
API_KEY = "d02f718aeb19fadc0a02515451c9e180"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Clima Pro Ultra", layout="wide")

# --- BIBLIOTECA DE IMAGENS HD (Corrigida com links diretos) ---
FOTOS_CLIMA = {
    "Clear": "https://images.unsplash.com/photo-1506452819137-0422416856b8?q=80&w=1920",
    "Clouds": "https://images.unsplash.com/photo-1534088568595-a066f410bcda?q=80&w=1920",
    "Rain": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?q=80&w=1920",
    "Drizzle": "https://images.unsplash.com/photo-1541675154750-0444c7d51e8e?q=80&w=1920",
    "Thunderstorm": "https://images.unsplash.com/photo-1559087867-ce4c91325525?q=80&w=1920",
    "Snow": "https://images.unsplash.com/photo-1477601263568-180e2c6d046e?q=80&w=1920",
    "Mist": "https://images.unsplash.com/photo-1485236715568-ddc5ee6ca227?q=80&w=1920",
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
            font-family: 'sans-serif';
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
    cidade = st.text_input("Pesquise uma cidade", label_visibility="collapsed", placeholder="🔍 Digite a cidade e tecle Enter...")

# --- LÓGICA DA TELA INICIAL ---
if not cidade:
    aplicar_estilo(FOTOS_CLIMA["Default"])
    st.markdown('''
        <div class="caixa-central">
            <h2 style="font-size: 40px;">Olá! 🌍</h2>
            <p style="font-size: 18px;">Coloque o nome da cidade acima para ver o clima em tempo real com imagens profissionais.</p>
        </div>
    ''', unsafe_allow_html=True)
else:
    params = {"q": cidade, "appid": API_KEY, "units": "metric", "lang": "pt_br"}
    try:
        response = requests.get(BASE_URL, params=params)
        dados = response.json()
        
        if response.status_code == 200:
            clima_main = dados['weather'][0]['main']
            nome = dados['name']
            temp = dados['main']['temp']
            condicao = dados['weather'][0]['description']
            nuvens = dados.get('clouds', {}).get('all', 0)
            humidade = dados['main']['humidity']
            
            # Busca a imagem de fundo
            url_fundo = FOTOS_CLIMA.get(clima_main, FOTOS_CLIMA["Default"])
            aplicar_estilo(url_fundo)

            # Emojis e Lógica de Dica
            mapeamento_emojis = {"Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️", "Drizzle": "🌦️", "Thunderstorm": "⛈️", "Snow": "❄️", "Mist": "🌫️", "Fog": "🌫️"}
            emoji = mapeamento_emojis.get(clima_main, "🌍")
            
            dica = "Hidrate-se 💧" if temp > 25 else "Agasalhe-se 🧥" if temp < 15 else "Clima agradável 😎"

            # Card de Informações
            st.markdown(f"""
                <div class="caixa-central">
                    <p style="font-size: 22px; opacity: 0.9; margin-bottom: 0;">{nome}</p>
                    <h1 style="font-size: 110px; margin: 0; line-height: 1;">{int(temp)}°C</h1>
                    <h2 style="margin-bottom: 20px;">{emoji} {condicao.title()}</h2>
                    
                    <div class="metric-container">
                        <div style="flex: 1;">
                            <p style="margin:0; font-size: 14px; opacity: 0.8;">☁️ Nuvens</p>
                            <p style="margin:0; font-size: 20px; font-weight: bold;">{nuvens}%</p>
                        </div>
                        <div style="flex: 1; border-left: 1px solid rgba(255,255,255,0.2); border-right: 1px solid rgba(255,255,255,0.2);">
                            <p style="margin:0; font-size: 14px; opacity: 0.8;">💧 Umidade</p>
                            <p style="margin:0; font-size: 20px; font-weight: bold;">{humidade}%</p>
                        </div>
                        <div style="flex: 1;">
                            <p style="margin:0; font-size: 14px; opacity: 0.8;">💡 Dica</p>
                            <p style="margin:0; font-size: 16px; font-weight: bold;">{dica}</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            aplicar_estilo(FOTOS_CLIMA["Default"])
            st.error("Cidade não encontrada.")
    except:
        st.error("Erro na conexão.")