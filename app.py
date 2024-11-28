import streamlit as st
import pandas as pd
import sqlite3

# Função para criar o banco de dados e tabela
def init_db():
    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER NOT NULL,
        email TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Função para inserir dados na tabela
def inserir_registro(nome, idade, email):
    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO registros (nome, idade, email) VALUES (?, ?, ?)", (nome, idade, email))
    conn.commit()
    conn.close()

# Função para carregar os registros
def carregar_registros():
    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registros")
    dados = cursor.fetchall()
    conn.close()
    return dados

# Inicializar o banco de dados
init_db()

# Título do aplicativo
st.title("Gerenciamento de Dados com Streamlit e SQLite")

# Seção para upload de arquivo CSV
st.header("Upload de Dados")
uploaded_file = st.file_uploader("Faça upload de um arquivo CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Pré-visualização dos Dados:")
    st.dataframe(df.head())

# Seção do formulário
st.header("Formulário para Inserir Dados")
with st.form("formulario"):
    nome = st.text_input("Nome:")
    idade = st.number_input("Idade:", min_value=0, max_value=120, step=1)
    email = st.text_input("Email:")
    submit = st.form_submit_button("Salvar")

    if submit:
        if nome and email:
            inserir_registro(nome, idade, email)
            st.success("Registro salvo com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos!")

# Exibir registros armazenados
st.header("Registros Armazenados")
dados = carregar_registros()
df_registros = pd.DataFrame(dados, columns=["ID", "Nome", "Idade", "Email"])
st.dataframe(df_registros)
