import streamlit as st
import requests

# --- CONFIGURAÇÃO DA API ---
API_KEY = "d02f718aeb19fadc0a02515451c9e180"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

st.set_page_config(page_title="Clima Pro", layout="wide")

# --- SUA BIBLIOTECA DE LINKS (EXATAMENTE COMO VOCÊ MANDOU) ---
FOTOS_CLIMA = {
    "Clear": "https://plus.unsplash.com/premium_photo-1733306531071-087c077e1502?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", 
    "Clouds": "https://images.unsplash.com/photo-1531147637440-2fb367004900?q=80&w=1920", 
    "Rain": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?q=80&w=1920", 
    "Thunderstorm": "https://images.unsplash.com/photo-1559087867-ce4c91325525?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", 
    "Snow": "https://images.unsplash.com/photo-1477601263568-180e2c6d046e?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", 
    "Mist": "https://images.unsplash.com/photo-1485236715568-ddc5ee6ca227?q=80&w=1920", 
    "Fog": "https://images.unsplash.com/photo-1485236715568-ddc5ee6ca227?q=80&w=1920",
    "Default": "https://images.unsplash.com/photo-1778483154534-8290a142eb2d?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
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
        }}
        .caixa-central {{
            background: rgba(255, 255, 255, 0.1); 
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            padding: 40px;
            border-radius: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center;
            max-width: 550px;
            margin: auto;
            margin-top: 5vh;
        }}
        h1, h2, p {{ color: white !important; font-family: 'sans-serif'; }}
        
        .metric-container {{
            display: flex;
            justify-content: space-around;
            margin-top: 25px;
            background: rgba(0, 0, 0, 0.2);
            padding: 15px;
            border-radius: 20px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.markdown("<h1 style='text-align: center;'>🌍 Monitor de Clima</h1>", unsafe_allow_html=True)
cidade = st.text_input("", placeholder="Digite a cidade e pressione Enter...")

if cidade:
    params = {"q": cidade, "appid": API_KEY, "units": "metric", "lang": "pt_br"}
    try:
        res = requests.get(BASE_URL, params=params).json()
        if res.get("cod") == 200:
            clima = res['weather'][0]['main']
            temp = res['main']['temp']
            desc = res['weather'][0]['description']
            humidade = res['main']['humidity']
            # Usamos a cobertura de nuvens como indicador de chance de chuva para a versão gratuita da API
            nuvens = res['clouds']['all']
            
            aplicar_estilo(FOTOS_CLIMA.get(clima, FOTOS_CLIMA["Default"]))
            
            # Lógica da Dica
            dica = "Hidrate-se 💧" if temp > 25 else "Agasalhe-se 🧥" if temp < 15 else "Clima agradável 😎"
            
            st.markdown(f"""
                <div class="caixa-central">
                    <p style="font-size: 20px; opacity: 0.8;">{res['name']}</p>
                    <h1 style="font-size: 80px; margin: 0;">{int(temp)}°C</h1>
                    <h2 style="text-transform: capitalize; margin-bottom: 20px;">{desc}</h2>
                    
                    <div class="metric-container">
                        <div>
                            <p style="margin:0; font-size: 13px; opacity: 0.7;">💧 Umidade</p>
                            <p style="margin:0; font-size: 18px; font-weight: bold;">{humidade}%</p>
                        </div>
                        <div style="border-left: 1px solid rgba(255,255,255,0.2); border-right: 1px solid rgba(255,255,255,0.2); padding: 0 20px;">
                            <p style="margin:0; font-size: 13px; opacity: 0.7;">🌧️ Chuva</p>
                            <p style="margin:0; font-size: 18px; font-weight: bold;">{nuvens}%</p>
                        </div>
                        <div>
                            <p style="margin:0; font-size: 13px; opacity: 0.7;">💡 Dica</p>
                            <p style="margin:0; font-size: 16px; font-weight: bold;">{dica}</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Cidade não encontrada.")
    except:
        st.error("Erro na conexão.")
else:
    # TELA INICIAL COM O CARD DE BOAS-VINDAS
    aplicar_estilo(FOTOS_CLIMA["Default"])
    st.markdown("""
        <div class="caixa-central">
            <h2 style="font-size: 35px;">Olá! 🌍</h2>
            <p>Coloque o nome da cidade acima para ver o clima em tempo real.</p>
        </div>
    """, unsafe_allow_html=True)