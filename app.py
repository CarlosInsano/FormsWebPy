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

# Função para atualizar registros
def atualizar_registro(id, nome, idade, email):
    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE registros SET nome = ?, idade = ?, email = ? WHERE id = ?", (nome, idade, email, id))
    conn.commit()
    conn.close()

# Função para excluir registros
def excluir_registro(id):
    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM registros WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# Inicializar o banco de dados
init_db()

# Título do aplicativo
st.title("Gerenciamento de Dados com Streamlit e SQLite - CRUD")

# Seção do formulário para adicionar novos registros
st.header("Adicionar Novo Registro")
with st.form("formulario_adicionar"):
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

# Seção para editar ou excluir registros
st.header("Editar ou Excluir Registro")
if dados:
    # Selecionar um registro para editar ou excluir
    ids = [registro[0] for registro in dados]
    id_selecionado = st.selectbox("Selecione o ID do registro:", ids)

    # Preencher os campos com os dados do registro selecionado
    registro_selecionado = next((r for r in dados if r[0] == id_selecionado), None)
    if registro_selecionado:
        novo_nome = st.text_input("Nome:", registro_selecionado[1])
        nova_idade = st.number_input("Idade:", min_value=0, max_value=120, value=registro_selecionado[2], step=1)
        novo_email = st.text_input("Email:", registro_selecionado[3])

        # Botões para atualizar ou excluir
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Atualizar"):
                atualizar_registro(id_selecionado, novo_nome, nova_idade, novo_email)
                st.success("Registro atualizado com sucesso!")
                st.rerun()

        with col2:
            if st.button("Excluir"):
                excluir_registro(id_selecionado)
                st.warning("Registro excluído com sucesso!")
                st.rerun()
else:
    st.info("Nenhum registro encontrado!")
