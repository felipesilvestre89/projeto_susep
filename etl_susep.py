import datetime
import pandas as pd
from sqlalchemy import TableClause
import db


# Inicializa um dataframe vazio para armazenar os resultados
# Hora início do script
inicio = datetime.datetime.now()
inicio_formatado = inicio.strftime('%H:%M:%S')

df_final_total = pd.DataFrame()

periodo = '200301'

while periodo != '202402':


    # ETL de todos os arquivos da pasta
    diretorio_excel = r'C:\portfolio\projeto_susep\susep\\'
    df = pd.read_html(f'{diretorio_excel}{periodo}.xls')

    # Escolha a tabela desejada (pode ser necessário ajustar o índice)
    indice_tabela_desejada = 0
    df_final = df[indice_tabela_desejada]

    # ETL para tratar os dados como float
    df_final.fillna(0)
    df_final.iloc[:, 2:29] = df_final.iloc[:, 2:29].replace({'\.': ''}, regex=True).astype(float)
    
    # Adiciona a coluna periodo
    df_final['periodo'] = [f'{periodo}']* len(df_final)
    
    # Concatena o dataframe atual ao dataframe total
    df_final_total = pd.concat([df_final_total, df_final], ignore_index=True)

    print(f'Executando agora o arquivo {periodo}')
 
    # Incrementar a variável periodo para o próximo ciclo
    # Converte os últimos dois dígitos para um número inteiro
    ano_mes = int(periodo[4:])
    # Incrementa um até 12
    ano_mes += 1
    # Se o mês ultrapassar 12, incrementa o ano e redefine o mês para 1
    if ano_mes > 12:
        ano_mes = 1
        ano = int(periodo[:4]) + 1
        periodo = f"{ano}{ano_mes:02d}"
    else:
        # Atualiza o período
        periodo = periodo[:4] + f"{ano_mes:02d}"

# Selecionando as colunas necessárias
df_final_total = df_final_total.iloc[:, 0:30]

# Etl das colunas para Modelagem no Banco
df_final_total.dropna(subset=['Empresa'])
df_final_total.columns = df_final_total.columns.str.lower()
df_final_total.columns = df_final_total.columns.str.replace('(r$)', '')
df_final_total.columns = df_final_total.columns.str.replace(' ', '')
df_final_total.columns = df_final_total.columns.str.replace('ó', 'o')

#Extraindo o arquivo para o csv
df_final_total = pd.melt(df_final_total, id_vars=['codigosusep', 'empresa', 'periodo'], var_name='estado', value_name='valor')
# df_final_total.to_excel('teste.xlsx')
# df_final_total.to_csv('arquivo_teste_final.csv', encoding='utf-8', index=False)

#Deletando a tabela
schema= 'public'
tabela= 'premios_susep2'

try:
    db.cursor.execute(f'TRUNCATE TABLE {schema}.{tabela}')
    db.conn.commit()
    print('Dados deletetados da tabela premios_susep')
except Exception as e:
    print(f'Erro ao executar truncate table na {schema}.{tabela}', e)

# Salvando os Dataframes no Banco
print('Inserindo Dataframe no banco de dados...')
try:
    df_final_total.to_sql(con=db.engine, name=f'{tabela}', schema=f'{schema}', if_exists='append',
                                index=False)
    print('Tabela de Premios Susep Inserida com Sucesso!')
except Exception as e:
    print('Erro', e)


# Hora fim do script
fim = datetime.datetime.now()
fim_formatado = fim.strftime('%H:%M:%S')
tempo_execucao = fim - inicio

print(f'Os dados da SUSEP foram inseridos no banco de dados:\n Início: {inicio_formatado} Fim: {fim_formatado}. Tempo de execução: {tempo_execucao}')