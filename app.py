import streamlit as st

# Configuração da página
st.set_page_config(page_title="Clima Premium", layout="wide")

# Banco de dados
dados = {
    "Londres": {"temp": 13, "condicao": "Céu limpo com períodos nublados", "foto": "https://cdn.sanity.io/images/mkg24y51/production/8a0c8000dcef4d42162c21c8aa11984dc98617e3-1000x656.webp/big-ben-londres.webp"},
    "Rio de Janeiro": {"temp": 22, "condicao": "Ensolarado", "foto": "https://www.melhoresdestinos.com.br/wp-content/uploads/2019/08/rio-de-janeiro-capa2019-01.jpg"},
    "Roma": {"temp": 18, "condicao": "Céu limpo com períodos nublados", "foto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT1XQguMVngykQm5AMwJmo9w2AN6tle93MUGA&s"},
    "Dubai": {"temp": 29, "condicao": "Céu limpo", "foto": "https://www.civitatis.com/blog/wp-content/uploads/2025/06/shutterstock_1711382014.jpg"},
    "Paris": {"temp": 13, "condicao": "Predominantemente nublado", "foto": "https://www.grayline.com/wp-content/uploads/2025/01/shutterstock_667548661-scaled.jpg"},
    "Pequim": {"temp": 20, "condicao": "Céu limpo com períodos nublados", "foto": "https://www.iroamly.com/images/beijing-china-cover.webp"},
    "Buenos Aires": {"temp": 19, "condicao": "Nublado", "foto": "https://aguiarbuenosaires.com/wp-content/uploads/2022/03/OBELISCO-ADRIANA.jpeg"},
    "Washington": {"temp": 21, "condicao": "Predominantemente ensolarado", "foto": "https://estadosunidosbrasil.com.br/wp-content/uploads/sites/6/2022/08/6791202359_9704749dbb_z1.jpg"}
}

# CSS (Fundo e Estética)
def aplicar_estilo(url_foto):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url("{url_foto}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .caixa-central {{
            background-color: rgba(255, 255, 255, 0.95);
            padding: 45px;
            border-radius: 25px;
            text-align: center;
            max-width: 500px;
            margin: auto;
            margin-top: 12vh;
            border: 1px solid #ddd;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.markdown("<h1 style='text-align: center; color: white; text-shadow: 2px 2px 4px #000;'>🌍 Monitor de Clima Global</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    cidade = st.selectbox("Escolha o destino:", ["Selecione..."] + list(dados.keys()))

if cidade != "Selecione...":
    info = dados[cidade]
    temp = info['temp']
    cond = info['condicao']
    aplicar_estilo(info['foto'])
    
    dicas = []
    if temp < 20: dicas.append("Vale a pena se agasalhar!")
    if temp >= 30 and ("ensolarado" in cond.lower() or "limpo" in cond.lower()):
        dicas.append("Recomendamos usar protetor solar!")
    
    dica_texto = f"* {' | '.join(dicas)}" if dicas else ""

    st.markdown(
        f"""
        <div class="caixa-central">
            <h2 style="color: #444; margin: 0;">{cidade}</h2>
            <h1 style="font-size: 100px; color: #222; margin: 0;">{temp}°C</h1>
            <p style="color: #666; font-size: 20px;">{cond}</p>
            <p style="color: #d32f2f; font-size: 15px; font-weight: bold;">{dica_texto}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    # AQUI ESTÁ A MUDANÇA DA PÁGINA INICIAL
    aplicar_estilo("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200")
    st.markdown(
        """
        <div class="caixa-central">
            <h2 style="color: #333; margin-bottom: 10px;">Selecione uma cidade para ver o clima</h2>
            <p style="color: #777;">Utilize o menu acima para explorar as temperaturas mundiais.</p>
        </div>
        """,
        unsafe_allow_html=True
    )