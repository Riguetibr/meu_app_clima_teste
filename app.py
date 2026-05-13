import streamlit as st
import requests

# --- CONFIGURAÇÃO DA API ---
API_KEY = "d02f718aeb19fadc0a02515451c9e180"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Clima", layout="wide")

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
        }}
        .caixa-central {{
            background-color: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 25px;
            text-align: center;
            max-width: 500px;
            margin: auto;
            margin-top: 5vh;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.markdown("<h1 style='text-align: center; color: white; text-shadow: 2px 2px 4px #000;'> Monitor de Clima Global</h1>", unsafe_allow_html=True)

# Busca de cidade
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    cidade = st.text_input("", placeholder="Digite o nome da cidade...")

if cidade:
    params = {
        "q": cidade,
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt_br"
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        dados = response.json()

        if response.status_code == 200:
            nome = dados['name']
            temp = dados['main']['temp']
            condicao = dados['weather'][0]['description']
            clima_main = dados['weather'][0]['main']
            
            # Tenta pegar a probabilidade de chuva (algumas cidades/momentos a API não envia esse dado no plano free)
            # Como alternativa, verificamos a umidade ou nuvens para dar uma estimativa se 'pop' não existir
            chuva_prob = dados.get('clouds', {}).get('all', 0) 
            
            emoji = obter_emoji(clima_main)
            
            # Lógica de Dicas
            dicas = []
            if temp < 15: dicas.append("🧥 Está frio, agasalhe-se!")
            elif 15 <= temp <= 25: dicas.append("🌤️ O clima está agradável.")
            else: dicas.append("🥵 Está calor, hidrate-se bem!")
            
            if "Rain" in clima_main or "Drizzle" in clima_main:
                dicas.append("☔ Não esqueça o guarda-chuva!")

            # Background padrão
            aplicar_estilo("https://s2.static.brasilescola.uol.com.br/be/2023/01/vista-da-atmosfera-camada-gasosa-que-envolve-a-terra.jpg")

            st.markdown(
                f"""
                <div class="caixa-central">
                    <h2 style="color: #444; margin: 0;">{nome} {emoji}</h2>
                    <h1 style="font-size: 85px; color: #111; margin: 10px 0;">{int(temp)}°C</h1>
                    <p style="color: #555; font-size: 22px; text-transform: capitalize; font-weight: 500;">{condicao}</p>
                    <p style="color: #007BFF; font-size: 18px;">💧 Chance de chuva/nuvens: {chuva_prob}%</p>
                    <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                    <p style="color: #d32f2f; font-size: 16px; font-weight: bold;">{" | ".join(dicas)}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("Cidade não encontrada. Verifique a digitação!")
            aplicar_estilo("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200")
    except:
        st.error("Erro ao carregar dados.")
else:
    aplicar_estilo("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200")
    st.markdown(
        """
        <div class="caixa-central">
            <h2 style="color: #333;">Olá!</h2>
            <p style="color: #777;">Digite uma cidade para ver as condições atuais.</p>
        </div>
        """,
        unsafe_allow_html=True
    )