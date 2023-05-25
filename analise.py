import streamlit as st
import pandas as pd 
import numpy as np
import openpyxl
import matplotlib.pyplot as plt
import plotly.express as px 
from io import BytesIO
import requests
import pytz
from datetime import datetime
from PIL import Image

# Configuração básica da página
st.set_page_config(
    page_title="Sistema Controle de Estoque",
    page_icon="U+1F527",
    #layout="Dark",
    initial_sidebar_state="expanded"
)
st.title('Sistema Controle de Qualidade')

# criar lista de opções 

menu=['Inicio','Prazo de Validade','Analise de Estoque']

# Adicionar um componente de rádio na barra lateral
escolha = st.sidebar.selectbox('Selecione uma opção', menu)


# exibir pagina inicial

if escolha == 'Inicio':

    # Cria duas colunas
    col1, col2, = st.columns([1,2])
    

    # Renderiza a tabela na primeira coluna
    with col1:
        
        # Carrega os dados do arquivo Excel
        df = pd.read_excel("C:/Users/ezequiaslima/Desktop/Streamlit/dados.xlsx")
        
        st.markdown("Bem-vindo ao Painel Geral")
        
        Filtra_dados = df['Tratativa'].unique().tolist()        
        selecionar_dados = st.selectbox('Selecione a Tratativa realizada:', Filtra_dados)      
        filtragem = df[df['Tratativa'] == selecionar_dados] 
        st.write(filtragem)

        
        # Exemplo de st.metric
        valor_metrica = len(filtragem)  # Valor numérico para exibir na métrica
        rotulo_metrica = "Registros"  # Rótulo para descrever a métrica

        st.metric(label=rotulo_metrica, value=valor_metrica)
        
      #################################### analise de dados vencidos 35 ###########################

        #################### configuração api 156 #############################
        url = "https://api-dw.bseller.com.br/webquery/execute-excel/QRY0156"
        
        headers = {
            "Content-Type": "application/json",
            "X-Auth-Token": "746E4AA1FE7A85BCE053A7F3A8C0AAED"
        }
        body = {
            "parametros": {
                "FORNEC": 0,
                "GRCL": "%",
                "P_ID_PLANTA": "MECAJ",
                "RESTR": "35",
                "X1": "%",
                "X2": "%",
                "X3": "%",
                "X4": "%"
            }
        }
        
        response = requests.post(url, headers=headers, json=body)
        excel_data = response.content
        
        # Ler o arquivo Excel diretamente a partir dos dados retornados pela API
        df_venc = pd.read_excel(BytesIO(excel_data))
        
        #################### configuração api 156 #############################
        
        # Calcular a soma da coluna "Valor"
        soma_valor = df_venc['Valor'].sum()

        # Arredondar o valor para duas casas decimais
        soma_valor_arredondada = round(soma_valor, 2)

        # Exibir a métrica no Streamlit
        st.metric("Valor Total Estoque a vencer", soma_valor_arredondada)
            
        ############################### soma de quantidade ####################
        # Calcular a soma da coluna "Quantidade"
        soma_quanti = df_venc['Quantidade'].sum()

        # Exibir a métrica no Streamlit
        st.metric("Quantidade de Itens em Estoque a vencer", soma_quanti)
            
    ################################ analise de dados vencidos 35 ###########################


        #################### configuração api 156 15 SECO #############################
    
        url = "https://api-dw.bseller.com.br/webquery/execute-excel/QRY0156"
        
        headers = {
            "Content-Type": "application/json",
            "X-Auth-Token": "746E4AA1FE7A85BCE053A7F3A8C0AAED"
        }
        body = {
            "parametros": {
                "FORNEC": 0,
                "GRCL": "%",
                "P_ID_PLANTA": "MECAJ",
                "RESTR": "15",
                "X1": "QBR",
                "X2": "DES",
                "X3": "001",
                "X4": "C.E"
            }
        }
        
        response = requests.post(url, headers=headers, json=body)
        excel_data = response.content
        
        df_avaria = pd.read_excel(BytesIO(excel_data))

        #################### configuração api 156 15 SECO #############################
   
        # Calcular a soma da coluna "Valor"
        #soma_valor = df_avaria['Valor'].sum()

        # Arredondar o valor para duas casas decimais
        #soma_valor_arredondada = round(soma_valor, 2)

        # Exibir a métrica no Streamlit
        #st.metric("Valor itens secos", soma_valor_arredondada)
            
        ############################### soma de quantidade ####################
        # Calcular a soma da coluna "Quantidade"
        #soma_quanti = df_avaria['Quantidade'].sum()

        # Exibir a métrica no Streamlit
        #st.metric("Quantide de Itens secos", soma_quanti)
         
    
    # Cria o gráfico de rosca na segunda coluna
    with col2:
    
    ################# grafico de processo de vencidos #####################
        fornecedor_grafico = px.pie(filtragem,
                                    title='Analise por Fornecedor',
                                    
                                    values='Valor Total',
                                    
                                    names='Digite o nome do Fornecedor'
                                    
        )
        
        st.plotly_chart(fornecedor_grafico)
    ################# grafico de processo de vencidos #####################
    
    
    
    
    ################ grafico de processo de estoqe a vencer ################
        # Ler o arquivo Excel diretamente a partir dos dados retornados pela API
                                ## api abaixo##
        url = "https://api-dw.bseller.com.br/webquery/execute-excel/QRY0156"
        
        headers = {
            "Content-Type": "application/json",
            "X-Auth-Token": "746E4AA1FE7A85BCE053A7F3A8C0AAED"
        }
        body = {
            "parametros": {
                "FORNEC": 0,
                "GRCL": "%",
                "P_ID_PLANTA": "MECAJ",
                "RESTR": "35",
                "X1": "%",
                "X2": "%",
                "X3": "%",
                "X4": "%"
            }
        }
        
        response = requests.post(url, headers=headers, json=body)
        excel_data = response.content
        
        # Ler o arquivo Excel diretamente a partir dos dados retornados pela API
        df_venc = pd.read_excel(BytesIO(excel_data))
                   ## api acima ##
        # Criar o gráfico de barras usando o Plotly Express
        fig_ve = px.bar(df_venc,
                     
                     title='Itens A vencer no estoque',
                     
                     x='Fornecedor',
                     
                     y='Valor')

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig_ve)
    ################ grafico de processo de estoqe a vencer ################
    
    
    
    ############### grafico de analise seco avaria interna  ################
                                ## api abaixo##
        url = "https://api-dw.bseller.com.br/webquery/execute-excel/QRY0156"
        
        headers = {
            "Content-Type": "application/json",
            "X-Auth-Token": "746E4AA1FE7A85BCE053A7F3A8C0AAED"
        }
        body = {
            "parametros": {
                "FORNEC": 0,
                "GRCL": "%",
                "P_ID_PLANTA": "MECAJ",
                "RESTR": "15",
                "X1": "QBR",
                "X2": "DES",
                "X3": "001",
                "X4": "C.E"
            }
        }
        
        response = requests.post(url, headers=headers, json=body)
        excel_data = response.content
        
        df_avaria = pd.read_excel(BytesIO(excel_data))

                   ## api acima ##
        # Ler o arquivo Excel diretamente a partir dos dados retornados pela API
        df_avaria = pd.read_excel(BytesIO(excel_data))

        # Criar o gráfico de barras usando o Plotly Express
        fig = px.bar(df_avaria, 
                     
                     title='Avaria Interna (SECO)', 
                     
                     x='Fornecedor', 
                     
                     y='Valor')

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)
    ############### grafico de analise seco avaria interna  ################
    
    
    ############################# metrica de avaria seca ####################

        # Calcular a soma da coluna "Valor"
        soma_valor = df_avaria['Valor'].sum()

        # Arredondar o valor para duas casas decimais
        soma_valor_arredondada = round(soma_valor, 2)

        # Exibir a métrica no Streamlit
        st.metric("Valor itens secos", soma_valor_arredondada)
            
        ############################### soma de quantidade ####################
        # Calcular a soma da coluna "Quantidade"
        soma_quanti = df_avaria['Quantidade'].sum()

        # Exibir a métrica no Streamlit
        st.metric("Quantidade de Itens secos", soma_quanti)
        ############################# metrica de avaria seca ####################
        #################### configuração api 156 15 SECO #############################



        ############### grafico de analise liquido avaria interna  ################
                                ## api abaixo##
        url = "https://api-dw.bseller.com.br/webquery/execute-excel/QRY0156"
        
        headers = {
            "Content-Type": "application/json",
            "X-Auth-Token": "746E4AA1FE7A85BCE053A7F3A8C0AAED"
        }
        body = {
            "parametros": {
                "FORNEC": 0,
                "GRCL": "%",
                "P_ID_PLANTA": "MECAJ",
                "RESTR": "15",
                "X1": "QBR",
                "X2": "LIQ",
                "X3": "001",
                "X4": "C.E"
            }
        }
        
        response = requests.post(url, headers=headers, json=body)
        excel_data = response.content
        
        df_avaria_liquido = pd.read_excel(BytesIO(excel_data))

        
        # Criar o gráfico de barras usando o Plotly Express
        fig_liquido = px.bar(df_avaria_liquido, 
                     
                     title='Avaria Interna (Liquido)', 
                     
                     x='Fornecedor', 
                     
                     y='Valor')

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig_liquido)
        
        
        # Calcular a soma da coluna "Valor"
        soma_valor = df_avaria_liquido['Valor'].sum()

        # Arredondar o valor para duas casas decimais
        soma_valor_arredondada = round(soma_valor, 2)

        # Exibir a métrica no Streamlit
        st.metric("Valor itens liquidos", soma_valor_arredondada)
            
        ############################### soma de quantidade ####################
        # Calcular a soma da coluna "Quantidade"
        soma_quanti = df_avaria_liquido['Quantidade'].sum()

        # Exibir a métrica no Streamlit
        st.metric("Quantidade de Itens Liquidos", soma_quanti)
        
        ############### grafico de analise liquido avaria interna  ################
    
        
        
    ########## Tela 2 ################
if escolha == 'Prazo de Validade':
    
    def main():
        st.markdown('Pagina para análise de itens vencidos!')
        
        col1, col2 = st.columns([1, 2])
        
        # Ler o arquivo Excel diretamente a partir dos dados retornados pela API
                                ## api abaixo##
        url = "https://api-dw.bseller.com.br/webquery/execute-excel/QRY0156"
        
        headers = {
            "Content-Type": "application/json",
            "X-Auth-Token": "746E4AA1FE7A85BCE053A7F3A8C0AAED"
        }
        body = {
            "parametros": {
                "FORNEC": 0,
                "GRCL": "%",
                "P_ID_PLANTA": "MECAJ",
                "RESTR": "65",
                "X1": "QBR",
                "X2": "VCT",
                "X3": "000",
                "X4": "NGC"
            }
        }
        
        response = requests.post(url, headers=headers, json=body)
        excel_data = response.content
        
        # Ler o arquivo Excel diretamente a partir dos dados retornados pela API
        df_venc_analise = pd.read_excel(BytesIO(excel_data))
        
        # Carregar a base geral para análise
        base_vencidos = pd.read_excel(r"C:\Users\ezequiaslima\Desktop\Streamlit\Base_dados_vencidos.xlsx")
        
        # Analisar por fornecedor
        fornecedores = df_venc_analise['Fornecedor'].unique().tolist()
        fornecedor_selecionado = st.selectbox('Selecione um fornecedor para filtrar:', fornecedores)
        base_filtrada = df_venc_analise[df_venc_analise['Fornecedor'] == fornecedor_selecionado]
        
        st.write(base_filtrada)
            
        # Opção para verificar o valor a vencer
        valor_de_vencido = st.checkbox("Verificar Valor do fornecedor?")
        
        if valor_de_vencido:
            # Verificar o valor
            verificar_valor_vencido = base_filtrada[['Valor']].sum()
            
            # Exibir dados somados
            st.write(verificar_valor_vencido)
                
        # Oferecer opção para salvar os dados filtrados em uma tabela Excel
        salvar_excel = st.checkbox("Salvar dados filtrados em Excel?")

        if salvar_excel:
            dinamica = pd.pivot_table(base_filtrada, index=['Item WMS', 'Lote', 'Ean', 'Data de Validade', 'Descrição', 'Fornecedor'], values=['Quantidade', 'Valor'], aggfunc=np.sum)
            
            # Salvar os dados filtrados em uma tabela Excel
            dinamica.to_excel("Relatorio.xlsx", index=True)
        
            # Exibir uma mensagem de sucesso para o usuário
            st.success("Dados filtrados salvos com sucesso em Relatorio.xlsx!")
            
        # Analisar estoque
        st.markdown('Análise de Estoque')
        
        # Configuração API 156
        url = "https://api-dw.bseller.com.br/webquery/execute-excel/QRY0156"
        headers = {
            "Content-Type": "application/json",
            "X-Auth-Token": "746E4AA1FE7A85BCE053A7F3A8C0AAED"
        }
        body = {
            "parametros": {
                "FORNEC": 0,
                "GRCL": "%",
                "P_ID_PLANTA": "MECAJ",
                "RESTR": "35",
                "X1": "%",
                "X2": "%",
                "X3": "%",
                "X4": "%"
            }
        }
        
        response = requests.post(url, headers=headers, json=body)
        excel_data = response.content
        
        # Ler o arquivo Excel diretamente a partir dos dados retornados pela API
        df_venc = pd.read_excel(BytesIO(excel_data))

        st.write(df_venc)
        
        # Opção para verificar o valor a vencer
        valor_a_vencer = st.checkbox("Verificar Valor?")
        
        if valor_a_vencer:
            # Verificar o valor
            verificar_valor = df_venc[['Valor']].sum()
            
            # Exibir dados somados
            st.write(verificar_valor)
            
        # Oferecer opção para salvar os dados em uma tabela Excel
        auditoria = st.checkbox("Auditar locais?")
        
        if auditoria:
            # Criar dinâmica
            di_au = pd.pivot_table(df_venc, index=['Item WMS', 'Lote', 'Ean', 'Data de Validade', 'Descrição', 'Fornecedor', 'Id Local', 'Local'], values=['Quantidade'], aggfunc=np.sum)
            
            # Ordenar as linhas em ordem decrescente com base na coluna "Local"
            dinamica_x = di_au.sort_values(by="Local", ascending=False)
            
            # Ordenar as linhas em ordem decrescente com base na coluna "Local"
            dinamica_v = dinamica_x.sort_values(by="Local", ascending=False)
            
            # Salvar em Excel
            dinamica_v.to_excel("Auditoria_estoque.xlsx", index=True)
            
            # Exibir uma mensagem de sucesso para o usuário
            st.success("Auditoria salva com sucesso em Auditoria_estoque.xlsx!")
            
        ############# Formulário para armazenar os fornecedores negociados ##############
        st.title("Acompanhamento de Negociação")
        
        # Criar campos de entrada para o formulário
        Fornecedor = st.text_input("Digite o nome do Fornecedor")
        Representante_Comercial = st.text_input("Digite o nome do Representante")
        Quantidade = st.text_input("Quantidade")
        Valor = st.text_input("Valor Total")
        Data = st.text_input("Data")
        Status = st.text_input("Status da Negociação")
        Tratativa = st.text_area("Tratativa")
            
        data = {}
            
        # Criar botão para enviar os dados do formulário
        if st.button("Enviar"): 
            # Criar dicionário com os dados do formulário
            data = {
                "Digite o nome do Fornecedor": Fornecedor,
                "Digite o nome do Representante": Representante_Comercial,
                "Quantidade": Quantidade,
                "Valor Total": Valor,
                "Data": Data,
                "Status da Negociação": Status,
                "Tratativa": Tratativa   
            }
            
            # Adicionar os dados do formulário a um DataFrame do Pandas
            df = pd.DataFrame([data])

            # Salvar o DataFrame em um arquivo Excel
            try:
                # Tenta abrir o arquivo Excel
                book = pd.read_excel("dados.xlsx")
                # Adiciona o novo DataFrame no final da planilha
                book = pd.concat([book, df], ignore_index=True)
            except FileNotFoundError:
                # Se o arquivo Excel não existir, cria um novo com o DataFrame
                book = df
                        
            # Salvar o DataFrame em um arquivo Excel
            book.to_excel("dados.xlsx", index=False)

            st.success("Dados enviados com sucesso!")
                
            #form = pd.read_excel(r"C:\Users\ezequiaslima\Desktop\Streamlit\dados.xlsx")
        
            #fornecedores_form = form['Status da Negociação'].unique().tolist()
            #form_select = st.selectbox('Selecione o status para filtrar:', fornecedores_form)
            #base_filtrada_form = form[form['Status da Negociação'] == form_select]
            
            #st.write(base_filtrada_form)
            
            #### Verificar valor #####
            #Pendente = st.checkbox("Verificar o valor?")
            
            #if Pendente:
                #validar_valor = base_filtrada_form[['Valor Total']].sum()
                
                #st.write(validar_valor)
                
            
                    
        ######## FILTRAR POR TRATATIVA ############
        form = pd.read_excel(r"C:\Users\ezequiaslima\Desktop\Streamlit\dados.xlsx")
                
        fornecedores_form = form['Tratativa'].unique().tolist()
                        
        form_selct = st.selectbox('Selecione a Tratativa:', fornecedores_form)
                        
        base_filtrada_form = form[form['Tratativa'] == form_selct]
                    
        st.write(base_filtrada_form)
                    
                
        ######### verificar valor de fornecedores finalizados #############
        Tratativa = st.checkbox("Verificação de valor?")
                    
        if Tratativa:
            
            valor_tratativa = base_filtrada_form[['Valor Total']].sum()
                        
            st.write(valor_tratativa)            

    if __name__ == "__main__":
        main()
        
######################################## PAGINA DE SEPARAÇÃO ##################################################


    ########## Tela 3 ###############
if escolha == 'Analise de Estoque':
    
    # Ler o arquivo Excel com as informações de login e senha
    acesso = pd.read_excel(r"C:\Users\ezequiaslima\Desktop\Streamlit\acesso.xlsx")

    # Barra lateral para o login
    st.sidebar.title("Apliação de Estoque")
    st.sidebar.markdown('Realazi o Login abaixo para Proseguir')

    # Campos de entrada para login e senha na barra lateral
    login = st.sidebar.text_input("Login")
    senha = st.sidebar.text_input("Senha", type="password")

    # Botão de login na barra lateral
    if st.sidebar.button("Entrar"):
        # Verificar se o login e a senha correspondem aos valores no DataFrame
        if any((acesso["Login"] == login) & (acesso["Senha"] == senha)):
            #st.success("Login realizado com sucesso!")
            login_realizado = True
        else:
            st.error("Login ou senha incorretos!")
            login_realizado = False
    else:
        login_realizado = False
       
    # Verificar se o login foi realizado com sucesso
    if login_realizado:
        # Ocultar a tela de login
        st.empty()

        # Restante do seu código aqui
        
        #################### configuração api 156 #############################
        url = "https://api-dw.bseller.com.br/webquery/execute-excel/QRY0156"
        
        headers = {
            "Content-Type": "application/json",
            "X-Auth-Token": "746E4AA1FE7A85BCE053A7F3A8C0AAED"
        }
        body = {
            "parametros": {
                "FORNEC": 0,
                "GRCL": "%",
                "P_ID_PLANTA": "MECAJ",
                "RESTR": "40",
                "X1": "ANE",
                "X2": "001",
                "X3": "001",
                "X4": "00"
            }
        }
        
        response = requests.post(url, headers=headers, json=body)
        excel_data = response.content
        
        # Ler o arquivo Excel diretamente a partir dos dados retornados pela API
        df_e = pd.read_excel(BytesIO(excel_data))

        #################### configuração api 156 #############################
    
        
        #################### configuração api 870 #############################

        # Configuração API QRY0870
        #url_qry0870 = "https://api-dw.bseller.com.br/webquery/execute-excel/QRY0870"

        #headers = {
           # "Content-Type": "application/json",
           # "X-Auth-Token": "746E4AA1FE7A85BCE053A7F3A8C0AAED"
        #}

        #today = datetime.today().strftime('%Y-%m-%d')  # Obtém a data atual no formato 'YYYY-MM-DD'

        #body = {
            #"parametros": {    
               #"P_COD_ITEM": None,
                #"P_DATA_FIM": """today""",
                #"P_DATA_INI": """today""",
                #"P_HORA_FIM": None,
                #"P_HORA_INI": None,
                #"P_ID_CLALOC_FIM": "%",
                #"P_ID_CLALOC_INI": "%",
                #"P_ID_PLANTA": "MECAJ",
                #"P_ID_TRANS": None
            #}
        #}

        #response_qry0870 = requests.post(url_qry0870, headers=headers, json=body)
        #excel_data_qry0870 = response_qry0870.content

        # Ler o arquivo Excel diretamente a partir dos dados retornados pela API QRY0870
        #df_qry0870 = pd.read_excel(BytesIO(excel_data_qry0870), engine='openpyxl')

        # Exibir o DataFrame
        #st.write(df_qry0870)

        #################### configuração api 870 #############################
        


    
        ############ colunas #################
        
        col1, col2 = st.columns([1,2])
        
        with col1:
            
            # Ler o arquivo Excel diretamente a partir dos dados retornados pela API
            df_e = pd.read_excel(BytesIO(excel_data))
            
            dinamica_estoque_negativo = pd.pivot_table(df_e, index=['Item WMS','Ean','Fornecedor','Descrição'], values=['Quantidade','Valor'])
            
            # Exibir o DataFrame
            st.write(dinamica_estoque_negativo)
            
            
            # Calcular a soma da coluna "Valor"
            soma_valor = df_e['Valor'].sum()

            # Arredondar o valor para duas casas decimais
            soma_valor_arredondada = round(soma_valor, 2)

            # Exibir a métrica no Streamlit
            st.metric("Valor Total Estoque Negativo", soma_valor_arredondada)
            
            ############################### soma de quantidade ####################
            # Calcular a soma da coluna "Quantidade"
            soma_quanti = df_e['Quantidade'].sum()

            # Exibir a métrica no Streamlit
            st.metric("Quantide de Itens Estoque Negativo", soma_quanti)
            ############################### soma de quantidade ####################
            
            
            
    
            ################################ analise anterior ##########################
            
            # Criar colunas "Valor Anterior" e "Quantidade Anterior" com os valores e quantidades da linha anterior
            df_e["Valor Anterior"] = df_e["Valor"].shift(1)
            df_e["Quantidade Anterior"] = df_e["Quantidade"].shift(1)

            # Exibir o DataFrame com as colunas adicionadas
            #st.write(df_e)

            # Calcular a soma dos valores anteriores
            soma_valor_anterior = df_e["Valor Anterior"].sum()

            # Arredondar o valor para duas casas decimais
            soma_valor_anterior_arredondada = round(soma_valor_anterior, 2)

            # Exibir a métrica no Streamlit
            st.metric("Valor Total Estoque Anterior", soma_valor_anterior_arredondada)

            # Calcular a soma das quantidades anteriores
            soma_quantidade_anterior = df_e["Quantidade Anterior"].sum()

            # Exibir a métrica no Streamlit
            st.metric("Quantidade de Itens Estoque Anterior", soma_quantidade_anterior)

            ################################ analise anterior ##########################
            
            
            ############################ analise multipla ############################
            mult = df_e.dropna(subset=['Item Multiplo'])

            mult[['Item Multiplo']].count()

            dinamica_multiplo = pd.pivot_table(df_e, index=['Item Multiplo','Item WMS','Descrição'], values=['Quantidade','Preço'], aggfunc=np.sum)

            st.write(dinamica_multiplo)
            
            
            ############################ analise multipla ############################

            
            ########################### analise de resumo geral 151 ######################
      
            
            ########################### analise de resumo geral 151 ######################
            
      
        with col2:
            
            # Criar o gráfico de barras usando o Plotly Express
            fig = px.bar(df_e, x='Fornecedor', y='Valor')

            # Exibir o gráfico no Streamlit
            st.plotly_chart(fig)
            
            # Restante do seu código aqui

            # Obter a data atual
            #data_atual = pd.to_datetime('now').strftime('%Y-%m-%d %H:%M:%S')


            # Obter a data atual com fuso horário de Brasília
            timezone = pytz.timezone('America/Sao_Paulo')
            data_atual = datetime.now(timezone).strftime('%d/%m/%Y %H:%M:%S')

            # Exibir a data da última atualização da API no formato brasileiro
            st.text(f"Última atualização da API: {data_atual}")

            # Exibir a data da última atualização da API
            #st.text(f"Última atualização da API: {data_atual}")

            # Grafico de itens anteriormente
            # Criar o gráfico de barras usando o Plotly Express com as colunas "Fornecedor" e "Valor Anterior"
            fig = px.bar(df_e, x="Fornecedor", y="Valor Anterior")

            # Exibir o gráfico no Streamlit
            st.plotly_chart(fig)
            





    
    
    
    






        
        
    
    
    
    
    
