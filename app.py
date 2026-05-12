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