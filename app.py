import streamlit as st

# Configuração da página para ficar bonita no celular
st.set_page_config(page_title="Clima Simples", layout="centered")

# Dados fictícios (Troque os números como quiser!)
dados_ficticios = {
    "Londres": "12°C",
    "Rio de Janeiro": "32°C",
    "Roma": "22°C"
}

# Título centralizado
st.markdown("<h1 style='text-align: center; color: #31333F;'>🌡️ Previsão do Tempo</h1>", unsafe_allow_html=True)
st.write("---")

# Seletor centralizado
col1, col2, col3 = st.columns([1, 4, 1])

with col2:
    cidade = st.selectbox(
        "Selecione a cidade para ver o clima:",
        options=["Selecione...", "Londres", "Rio de Janeiro", "Roma"],
        index=0
    )

st.write("") # Espaço em branco

# Lógica de exibição: Só mostra o número se escolher uma cidade
if cidade != "Selecione...":
    temperatura = dados_ficticios[cidade]
    
    # Card visual com o número grande no meio
    st.markdown(
        f"""
        <div style="
            text-align: center; 
            padding: 50px; 
            border-radius: 25px; 
            background-color: #f0f2f6;
            border: 2px solid #e0e0e0;
            box-shadow: 2px 2px 15px rgba(0,0,0,0.05);">
            <h2 style="color: #555; margin-bottom: 5px;">{cidade}</h2>
            <h1 style="font-size: 100px; color: #ff4b4b; margin: 0;">{temperatura}</h1>
            <p style="color: #888; font-size: 14px; margin-top: 10px;">Céu limpo e ensolarado</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
else:
    st.info("👆 Por favor, selecione uma cidade acima para visualizar a temperatura.")

# Rodapé simples
st.markdown("<br><p style='text-align: center; color: #aaa;'>App de Teste v1.0</p>", unsafe_allow_html=True)