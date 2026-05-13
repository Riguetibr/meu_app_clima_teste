import streamlit as st
import requests

# --- CONFIGURAÇÃO DA API ---
API_KEY = "d02f718aeb19fadc0a02515451c9e180"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Clima Pro", layout="wide")

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

# Função de Estilo (CSS Avançado com Glassmorphism)
def aplicar_estilo(url_foto):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url("{url_foto}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            transition: background 0.5s ease-in-out;
        }}
        .caixa-central {{
            background: rgba(255, 255, 255, 0.15); /* Transparência para o efeito vidro */
            backdrop-filter: blur(15px);           /* O desfoque (Glassmorphism) */
            -webkit-backdrop-filter: blur(15px);
            padding: 40px;
            border-radius: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2); /* Bordinha sutil */
            text-align: center;
            max-width: 550px;
            margin: auto;
            margin-top: 5vh;
            box-shadow: 0 15px 35px rgba(0,0,0,0.4);
            color: white;
        }}
        h1, h2, p {{
            color: white !important;
            text-shadow: 1px 1px 5px rgba(0,0,0,0.2);
        }}
        /* Estilo para o input ficar bonitinho no vidro */
        .stTextInput > div > div > input {{
            background: rgba(255, 255, 255, 0.2) !important;
            color: white !important;
            border-radius: 15px !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Título Principal
st.markdown("<h1 style='text-align: center; margin-bottom: 20px;'>🌤️ Monitor de Clima Global</h1>", unsafe_allow_html=True)

# Busca de cidade
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    cidade = st.text_input("", placeholder="🔍 Digite o nome da cidade e aperte Enter...")

# Imagem padrão caso nada seja pesquisado
url_dinamica = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1920&q=80"

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
            chuva_prob = dados.get('clouds', {}).get('all', 0) 
            
            # 1. Busca imagem do Unsplash baseada no clima atual
            url_dinamica = f"https://source.unsplash.com/featured/1600x900/?weather,{clima_main},{nome}"
            
            aplicar_estilo(url_dinamica)
            
            emoji = obter_emoji(clima_main)
            
            # Lógica de Dicas
            dicas = []
            if temp < 15: dicas.append("🧥 Agasalhe-se")
            elif 15 <= temp <= 25: dicas.append("🌤️ Clima agradável")
            else: dicas.append("🥵 Hidrate-se")
            
            if "Rain" in clima_main or "Drizzle" in clima_main:
                dicas.append("☔ Leve guarda-chuva")

            st.markdown(
                f"""
                <div class="caixa-central">
                    <p style="font-size: 20px; opacity: 0.8; margin-bottom: 0;">{nome}</p>
                    <h1 style="font-size: 100px; margin: 0; font-weight: bold;">{int(temp)}°C</h1>
                    <h2 style="margin-top: 0;">{emoji} {condicao.title()}</h2>
                    <div style="display: flex; justify-content: space-around; margin-top: 20px; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 20px;">
                        <div>
                            <p style="margin:0; font-size: 14px;">Nuvens</p>
                            <p style="margin:0; font-weight: bold;">{chuva_prob}%</p>
                        </div>
                        <div>
                            <p style="margin:0; font-size: 14px;">Dica</p>
                            <p style="margin:0; font-weight: bold;">{" | ".join(dicas)}</p>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            aplicar_estilo(url_dinamica)
            st.error("Ops! Cidade não encontrada.")
    except:
        aplicar_estilo(url_dinamica)
        st.error("Erro na conexão com o servidor.")
else:
    aplicar_estilo(url_dinamica)
    st.markdown(
        """
        <div class="caixa-central">
            <h2>Bem-vindo! 🌍</h2>
            <p>Descubra o clima em tempo real em qualquer lugar do mundo com visual imersivo.</p>
        </div>
        """,
        unsafe_allow_html=True
    )