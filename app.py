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
        "Fog": "🌫️"
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
            transition: background 1s ease-in-out; /* Transição suave na troca de foto */
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
    cidade = st.text_input("Pesquise uma cidade", label_visibility="collapsed", placeholder="🔍 Digite a cidade e tecle Enter...")

# Imagem padrão inicial
url_exibicao = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1920&q=80"

if cidade:
    params = {"q": cidade, "appid": API_KEY, "units": "metric", "lang": "pt_br"}
    try:
        response = requests.get(BASE_URL, params=params)
        dados = response.json()

        if response.status_code == 200:
            nome = dados['name']
            temp = dados['main']['temp']
            condicao = dados['weather'][0]['description']
            clima_main = dados['weather'][0]['main'] # Ex: 'Clear', 'Rain'
            nuvens = dados.get('clouds', {}).get('all', 0)
            humidade = dados['main']['humidity']
            
            # --- LÓGICA DE IMAGEM DINÂMICA CORRIGIDA ---
            # Criamos uma busca específica: clima + nome da cidade para ser mais preciso
            busca_termo = f"{clima_main},{nome},weather"
            url_exibicao = f"https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?auto=format&fit=crop&q=80&w=1920&sig={cidade.replace(' ', '')}&keywords={busca_termo}"
            
            # Se for ensolarado, tentamos uma foto de sol, se chover, de chuva, etc.
            mapeamento_fotos = {
                "Clear": "sunny,sky",
                "Clouds": "cloudy,overcast",
                "Rain": "rain,wet",
                "Drizzle": "drizzle",
                "Thunderstorm": "storm,lightning",
                "Snow": "snow,winter",
                "Mist": "fog,mist",
                "Fog": "fog"
            }
            termo_clima = mapeamento_fotos.get(clima_main, "weather")
            url_exibicao = f"https://loremflickr.com/1920/1080/{termo_clima},{nome.replace(' ', '')}/all"

            aplicar_estilo(url_exibicao)
            emoji = obter_emoji(clima_main)
            
            dicas = []
            if temp < 15: dicas.append("Agasalhe-se")
            elif 15 <= temp <= 25: dicas.append("Clima agradável")
            else: dicas.append("Hidrate-se")
            if "Rain" in clima_main: dicas.append("Leve guarda-chuva")

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
            aplicar_estilo(url_exibicao)
            st.error("Cidade não encontrada.")
    except:
        aplicar_estilo(url_exibicao)
        st.error("Erro na conexão.")
else:
    aplicar_estilo(url_exibicao)
    st.markdown('<div class="caixa-central"><h2 style="font-size: 40px;">Olá! 🌍</h2><p style="font-size: 18px;">Coloque o nome da cidade acima e veja seu clima</p></div>', unsafe_allow_html=True)