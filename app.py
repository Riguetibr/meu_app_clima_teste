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

# Função de Estilo (CSS Corrigido para Contraste e Leitura)
def aplicar_estilo(url_foto):
    st.markdown(
        f"""
        <style>
        /* Fundo da aplicação com película escura para dar contraste */
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("{url_foto}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            transition: background 0.8s ease-in-out;
        }}

        /* CAIXA CENTRAL - Glassmorphism */
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
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        }}

        /* CORREÇÃO DO INPUT: Texto preto ao digitar para legibilidade */
        .stTextInput > div > div > input {{
            color: #111111 !important; 
            background-color: rgba(255, 255, 255, 0.9) !important;
            border-radius: 12px !important;
            padding: 10px 15px !important;
            font-size: 18px !important;
        }}

        /* Textos do Site */
        h1, h2, h3, p, span {{
            color: white !important;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.8) !important;
            font-family: 'Source Sans Pro', sans-serif;
        }}

        /* Estilo para métricas rápidas */
        .metric-container {{
            display: flex;
            justify-content: space-around;
            margin-top: 25px;
            background: rgba(0, 0, 0, 0.2);
            padding: 20px;
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Título invisível para acessibilidade, mas estilizado no Markdown
st.markdown("<h1 style='text-align: center;'>🌍 Monitor de Clima Global</h1>", unsafe_allow_html=True)

# Busca de cidade
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    cidade = st.text_input("Pesquise uma cidade", label_visibility="collapsed", placeholder="🔍 Digite a cidade e tecle Enter...")

# Imagem padrão (Montanha/Céu)
url_atual = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1920&q=80"

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
            nuvens = dados.get('clouds', {}).get('all', 0)
            humidade = dados['main']['humidity']
            
            # URL Dinâmica baseada no clima e nome da cidade
            url_atual = f"https://api.unsplash.com/search/photos?query={clima_main}+{nome}&client_id=YOUR_UNSPLASH_KEY" 
            # Como não temos chave API Unsplash agora, usaremos o redirecionador otimizado:
            url_atual = f"https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?auto=format&fit=crop&q=80&w=1920&keywords={clima_main}"
            
            aplicar_estilo(url_atual)
            emoji = obter_emoji(clima_main)
            
            # Lógica de Dicas
            dicas = []
            if temp < 15: dicas.append("🧥 Agasalhe-se")
            elif 15 <= temp <= 25: dicas.append("🌤️ Clima agradável")
            else: dicas.append("🥵 Hidrate-se")
            
            if "Rain" in clima_main: dicas.append("☔ Leve guarda-chuva")

            st.markdown(
                f"""
                <div class="caixa-central">
                    <p style="font-size: 22px; opacity: 0.9; margin-bottom: 0;">{nome}</p>
                    <h1 style="font-size: 110px; margin: 0; line-height: 1;">{int(temp)}°C</h1>
                    <h2 style="margin-bottom: 20px;">{emoji} {condicao.title()}</h2>
                    
                    <div class="metric-container">
                        <div>
                            <p style="margin:0; font-size: 14px; opacity: 0.8;">Nuvens</p>
                            <p style="margin:0; font-size: 20px; font-weight: bold;">{nuvens}%</p>
                        </div>
                        <div>
                            <p style="margin:0; font-size: 14px; opacity: 0.8;">Umidade</p>
                            <p style="margin:0; font-size: 20px; font-weight: bold;">{humidade}%</p>
                        </div>
                        <div>
                            <p style="margin:0; font-size: 14px; opacity: 0.8;">Sugestão</p>
                            <p style="margin:0; font-size: 16px; font-weight: bold;">{" | ".join(dicas)}</p>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            aplicar_estilo(url_atual)
            st.error("Cidade não encontrada. Tente novamente!")
    except Exception as e:
        aplicar_estilo(url_atual)
        st.error(f"Erro ao conectar com a API.")
else:
    aplicar_estilo(url_atual)
    st.markdown(
        """
        <div class="caixa-central">
            <h2 style="font-size: 40px;">Olá! 🌍</h2>
            <p style="font-size: 18px;">Digite o nome de uma cidade acima para ver a mágica acontecer.</p>
        </div>
        """,
        unsafe_allow_html=True
    )