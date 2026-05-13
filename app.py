import streamlit as st
import requests

# --- CONFIGURAÇÃO DA API ---
API_KEY = "d02f718aeb19fadc0a02515451c9e180"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Clima Pro Ultra", layout="wide")

# Função para definir o Emoji baseado no clima
def obter_emoji(clima_main):
    mapeamento = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Mist": "🌫️",
        "Fog": "🌫️",
        "Haze": "🌫️"
    }
    return mapeamento.get(clima_main, "🌍")

# Função de Estilo (CSS)
def aplicar_estilo(url_foto):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("{url_foto}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            transition: background 1.2s ease-in-out;
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

# 1. BIBLIOTECA DE CLIMA (Imagens focadas apenas no fenômeno)
FOTOS_POR_CLIMA = {
    "Clear": "https://images.unsplash.com/photo-1506452819137-0422416856b8?q=80&w=1920", # Céu limpo/Sol
    "Clouds": "https://images.unsplash.com/photo-1534088568595-a066f410bcda?q=80&w=1920", # Nublado
    "Rain": "https://images.unsplash.com/photo-1534274988757-a28bf1f539cf?q=80&w=1920", # Chuva
    "Drizzle": "https://images.unsplash.com/photo-1541675154750-0444c7d51e8e?q=80&w=1920", # Chuvisco
    "Thunderstorm": "https://images.unsplash.com/photo-1605727281914-5570a9a24d97?q=80&w=1920", # Tempestade
    "Snow": "https://images.unsplash.com/photo-1478265409131-1f65c88f965c?q=80&w=1920", # Neve
    "Mist": "https://images.unsplash.com/photo-1485236715568-ddc5ee6ca227?q=80&w=1920", # Névoa
    "Fog": "https://images.unsplash.com/photo-1485236715568-ddc5ee6ca227?q=80&w=1920", # Nevoeiro
    "Haze": "https://images.unsplash.com/photo-1522163182402-834f871fd851?q=80&w=1920", # Névoa seca
    "Default": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=1920"
}

st.markdown("<h1 style='text-align: center;'>🌍 Monitor de Clima Global</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    cidade = st.text_input("Pesquise uma cidade", label_visibility="collapsed", placeholder="🔍 Digite a cidade e tecle Enter...")

# Imagem inicial (Montanha genérica)
if not cidade:
    aplicar_estilo(FOTOS_POR_CLIMA["Default"])
    st.markdown('<div class="caixa-central"><h2 style="font-size: 40px;">Olá! 🌍</h2><p style="font-size: 18px;">Coloque o nome da cidade acima e veja seu clima</p></div>', unsafe_allow_html=True)
else:
    params = {"q": cidade, "appid": API_KEY, "units": "metric", "lang": "pt_br"}
    try:
        response = requests.get(BASE_URL, params=params)
        dados = response.json()

        if response.status_code == 200:
            clima_agora = dados['weather'][0]['main']
            nome = dados['name']
            temp = dados['main']['temp']
            condicao = dados['weather'][0]['description']
            nuvens = dados.get('clouds', {}).get('all', 0)
            humidade = dados['main']['humidity']
            
            # A MÁGICA ACONTECE AQUI: O fundo é escolhido APENAS pelo clima retornado
            url_fundo = FOTOS_POR_CLIMA.get(clima_agora, FOTOS_POR_CLIMA["Default"])
            
            aplicar_estilo(url_fundo)
            emoji = obter_emoji(clima_agora)
            
            dicas = []
            if temp < 15: dicas.append("Agasalhe-se")
            elif 15 <= temp <= 25: dicas.append("Clima agradável")
            else: dicas.append("Hidrate-se")
            if "Rain" in clima_agora: dicas.append("Leve guarda-chuva")

            html_content = f"""<div class="caixa-central">
<p style="font-size: 22px; opacity: 0.9; margin-bottom: 0;">{nome}</p>
<h1 style="font-size: 110px; margin: 0; line-height: 1;">{int(temp)}°C</h1>
<h2 style="margin-bottom: 20px;">{emoji} {condicao.title()}</h2>
<div class="metric-container">
<div style="flex: 1;"><p style="margin:0; font-size: 14px; opacity: 0.8;">☁️ Nuvens</p><p style="margin:0; font-size: 20px; font-weight: bold;">{nuvens}%</p></div>
<div style="flex: 1; border-left: 1px solid rgba(255,255,255,0.2); border-right: 1px solid rgba(255,255,255,0.2);"><p style="margin:0; font-size: 14px; opacity: 0.8;">💧 Umidade</p><p style="margin:0; font-size: 20px; font-weight: bold;">{humidade}%</p></div>
<div style="flex: 1;"><p style="margin:0; font-size: 14px; opacity: 0.8;">💡 Dica</p><p style="margin:0; font-size: 16px; font-weight: bold;">{" | ".join(dicas)}</p></div>
</div></div>"""
            st.markdown(html_content, unsafe_allow_html=True)
        else:
            aplicar_estilo(FOTOS_POR_CLIMA["Default"])
            st.error("Cidade não encontrada.")
    except:
        aplicar_estilo(FOTOS_POR_CLIMA["Default"])
        st.error("Erro na conexão.")