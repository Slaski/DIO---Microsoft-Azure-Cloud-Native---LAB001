import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import pymssql
import uuid
import json
from dotenv import load_dotenv

load_dotenv()

BLOB_CONNECTION_STRING = os.getenv('BLOB_CONNECTION_STRING')
BLOB_CONTAINER_NAME = os.getenv('BLOB_CONTAINER_NAME')
BLOB_ACCOUNT_NAME = os.getenv('BLOB_ACCOUNT_NAME')

SQL_SERVER = os.getenv('SQL_SERVER')
SQL_DATABASE = os.getenv('SQL_DATABASE')
SQL_USER = os.getenv('SQL_USER')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')

st.title('Cadastro de Produtos')

# Formulário de cadastros de produtos
nome_produto = st.text_input('Nome do Produto')
preco_produto = st.number_input('Preço do Produto', min_value=0.0, format='%.2f')
descricao_produto = st.text_input('Descrição do Produto')
imagem_produto = st.file_uploader('Imagem do Produto', type=['jpg', 'png', 'jpeg'])

# Salvar imagem no blob storage
def carrega_imagem(file):
    service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
    container_client = service_client.get_container_client(BLOB_CONTAINER_NAME)
    blob_name = str(uuid.uuid4()) + file.name
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(file.read(), overwrite=True)
    image_url = f"https://{BLOB_ACCOUNT_NAME}.blob.core.windows.net/{BLOB_CONTAINER_NAME}/{blob_name}"
    return image_url

def insere_produto(nome, preco, descricao, imagem):
    try:
        imagem_url = carrega_imagem(imagem)
        conn = pymssql.connect(server=SQL_SERVER, database=SQL_DATABASE, user=SQL_USER, password=SQL_PASSWORD)
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO Produtos (nome, preco, descricao, imagem_url) VALUES ('{nome}', {preco}, '{descricao}', '{imagem_url}')")
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f'Erro ao inserir produto: {e}')
        return False
    
def lista_produtos():
    try:
        conn = pymssql.connect(server=SQL_SERVER, database=SQL_DATABASE, user=SQL_USER, password=SQL_PASSWORD)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Produtos")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        st.error(f'Erro ao listar produtos: {e}')
        return []
    
def printa_produtos_tela():
    produtos = lista_produtos()
    if produtos:
        cards_por_linha = 3
        cols = st.columns(cards_por_linha)
        for i, produto in enumerate(produtos):
            col = cols[i % cards_por_linha]
            with col:
                st.markdown(f'### {produto[1]}')
                st.write(f'**Preço:** {produto[3]:.2f}')
                st.write(f'**Descrição:** {produto[2]}')
                if produto[4]:
                    html_img = f'<img src="{produto[4]}" width="200" height="200" alt="Imagem do Produto" />'
                    st.markdown(html_img, unsafe_allow_html=True)
            if (i + 1) % cards_por_linha == 0 and (i + 1) < len(produtos):
                cols = st.columns(cards_por_linha)
    else:
        st.info("Nenhum produto encontrado")

if st.button('Salvar Produto'):
    insere_produto(nome_produto, preco_produto, descricao_produto, imagem_produto)
    return_mesage = 'Produto salvo com sucesso'
    printa_produtos_tela()

st.header('Produtos Cadastrados')

if st.button('Listar Produtos'):
    printa_produtos_tela()
    return_message = 'Produtos listados com sucesso'