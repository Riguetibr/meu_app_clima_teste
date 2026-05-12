import streamlit as st

# Configuração da página
st.set_page_config(page_title="Clima Premium", layout="wide")

# Banco de dados com suas temperaturas e condições exatas
dados = {
    "Londres": {"temp": 13, "condicao": "Céu limpo com períodos nublados", "foto": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1200"},
    "Rio de Janeiro": {"temp": 22, "condicao": "Ensolarado", "foto": "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5?w=1200"},
    "Roma": {"temp": 18, "condicao": "Céu limpo com períodos nublados", "foto": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=1200"},
    "Dubai": {"temp": 29, "condicao": "Céu limpo", "foto": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1200"},
    "Paris": {"temp": 13, "condicao": "Predominantemente nublado", "foto": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1200"},
    "Pequim": {"temp": 20, "condicao": "Céu limpo com períodos nublados", "foto": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=1200"},
    "Buenos Aires": {"temp": 19, "condicao": "Nublado", "foto": "https://images.unsplash.com/photo-1589909202802-8f4aadce1849?w=1200"},
    "Washington": {"temp": 21, "condicao": "Predominantemente ensolarado", "foto": "https://images.unsplash.com/photo-1501466044931-62695aada8e9?w=1200"}
}

# Função para aplicar o CSS de fundo e estilo da caixa
def aplicar_estilo(url_foto):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url("{url_foto}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        
        .caixa-clima {{
            background-color: rgba(245, 245, 245, 0.9);
            padding: 50px;
            border-radius: 30px;
            text-align: center;
            max-width: 450px;
            margin: auto;
            margin-top: 50px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Interface
st.markdown("<h1 style='text-align: center; color: white; text-shadow: 2px 2px 4px #000;'>🌍 Dashboard de Clima</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    cidade = st.selectbox("Escolha uma cidade:", ["Selecione..."] + list(dados.keys()))

if cidade != "Selecione...":
    info = dados[cidade]
    temp = info['temp']
    cond = info['condicao']
    
    # Aplicar o fundo dinâmico
    aplicar_estilo(info['foto'])
    
    # Lógica de Dicas solicitadas
    dicas = []
    if temp < 20:
        dicas.append("Vale a pena se agasalhar!")
    
    if temp > 30 and ("ensolarado" in cond.lower() or "limpo" in cond.lower()):
        dicas.append("Recomendamos usar protetor solar!")
    
    dica_texto = f"* {' | '.join(dicas)}" if dicas else ""

    # Mostrar a caixa central
    st.markdown(
        f"""
        <div class="caixa-clima">
            <h2 style="color: #444; margin-bottom: 5px;">{cidade}</h2>
            <h1 style="font-size: 90px; color: #222; margin: 0;">{temp}°C</h1>
            <p style="color: #666; font-size: 18px; margin-top: 10px;">{cond}</p>
            <p style="color: #d32f2f; font-size: 14px; font-weight: bold; margin-top: 20px;">{dica_texto}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    aplicar_estilo("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200")
    st.info("Escolha uma cidade acima para ver os detalhes.")