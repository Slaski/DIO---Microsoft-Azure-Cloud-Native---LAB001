# DIO - Microsoft Azure Cloud Native - LAB001
Laboratório do módulo "Armazenando dados de um E-commerce na Cloud" do bootcamp "Microsoft Azure Cloud Native".

## Descrição
Neste laboratório criamos uma página no streamlit para cadastro de produtos e listagem dos mesmos. Os dados dos produtos são armazenados banco de dados SQL no Azure e as imagens dos produtos são armazenados num contêiner em uma conta de armazenamento no Azure.

### Dependências
O projeto foi desenvolvido em python utilizando o vscode. As dependências do projeto estão listadas no arquivo requirements.txt. Para instalação delas, podemos utilizar o pip conforme abaixo:
```
python -m pip install -r requirements.txt
```

### Configuração
As configurações necessárias para execução devem estar no arquivo .env. Nela preenchemos os parâmetros para conexão ao contêiner e ao banco de dados de SQL. Segue os parâmetros necessários:
```
BLOB_CONNECTION_STRING = "..."
BLOB_CONTAINER_NAME = "..."
BLOB_ACCOUNT_NAME = "..."
SQL_SERVER = "..."
SQL_DATABASE = "..."
SQL_USER = "..."
SQL_PASSWORD = "..."
```

### Execução
Para execução devemos executar o streamlit com o arquivo main.py.
```
python -m streamlit run main.py
```