import streamlit as st
import pandas as pd
import plotly.express as px

# URL do arquivo CSV no GitHub
url = 'https://raw.githubusercontent.com/mariopenna/CRAQUE/main/CRAQUE.csv'

# Carregar o CSV diretamente do GitHub
data = pd.read_csv(url)

# Renomear as colunas conforme solicitado
data = data.rename(columns={
    'Player': 'Jogador',
    'Nation': 'Nacionalidade',
    'Idade': 'Idade',
    'Born': 'Nascimento',
    'Squad': 'Time',
    'Pos': 'Posição',
    'Campeonato': 'Campeonato',
    'Ano': 'Temporada',
    'MP': 'Partidas',
    'Min': 'Minutos',
    'Gls': 'Gols',
    'Ast': 'Assistencias',
    'GCA': 'GCA (Ações que geraram Gols)',
    'Cmp%_total': '%Passes Completados',
    'TklW_tackles': 'Tackles Vencidos',
    'Int_blocks': 'Interceptações',
    'CrdY_performance': 'Cartões Amarelos',
    'Won%_aereal-duels': '% Bolas Aéreas Vencidas',
    'RAPTOR_final_Off': 'CRAQUE Ofensivo',
    'RAPTOR_final_Def': 'CRAQUE Defensivo',
    'RAPTOR_final_Total': 'CRAQUE Total',
    'WAR': 'WAR'
})

# Criar as páginas
page = st.sidebar.radio("Navegação", ["Sobre", "Análise Geral", "Tabela", "Comparação de Jogadores"])

if page == "Sobre":
    st.title("Projeto CRAQUE: Cálculo de Rendimentos de Atletas")
    st.write("""
    Bem-vindo ao projeto CRAQUE! Este projeto visa analisar o desempenho de jogadores de futebol utilizando um modelo 
    inovador chamado CRAQUE (Cálculo de Rendimentos de Atletas em Qualidade e Estatísticas).
    
    Use a navegação à esquerda para explorar a análise gráfica dos dados, visualizar a tabela geral com todos os jogadores, 
    ou comparar dois jogadores específicos.
    """)

elif page == "Análise Geral":
    st.title("Análise Geral")

    # Filtro por Campeonato
    campeonato = st.selectbox('Selecione um Campeonato', options=['Todos'] + list(data['Campeonato'].unique()))
    if campeonato != 'Todos':
        clubes_disponiveis = data[data['Campeonato'] == campeonato]['Time'].unique()
    else:
        clubes_disponiveis = data['Time'].unique()

    # Filtro por Clube (exibe apenas clubes do campeonato selecionado)
    squad = st.selectbox('Selecione um Clube', options=['Todos'] + list(clubes_disponiveis))

    # Filtro por Idade
    idade_min, idade_max = st.slider('Selecione o intervalo de Idade', int(data['Idade'].min()), int(data['Idade'].max()), (int(data['Idade'].min()), int(data['Idade'].max())))
    data_filtered = data[(data['Idade'] >= idade_min) & (data['Idade'] <= idade_max)]

    # Aplicar filtros adicionais em data_filtered
    if campeonato != 'Todos':
        data_filtered = data_filtered[data_filtered['Campeonato'] == campeonato]
    if squad != 'Todos':
        data_filtered = data_filtered[data_filtered['Time'] == squad]

    # Gráfico de dispersão com cores para diferentes times
    fig = px.scatter(
        data_filtered,
        x='CRAQUE Ofensivo',
        y='CRAQUE Defensivo',
        color='Time',  # Times representados por cores diferentes
        size_max=5,
        opacity=0.8,
        hover_name='Jogador',
        hover_data=['Temporada', 'Idade', 'Campeonato'],
        title='Relação entre CRAQUE Ofensivo vs CRAQUE Defensivo por Time',
        labels={
            'CRAQUE Ofensivo': 'CRAQUE Ofensivo',
            'CRAQUE Defensivo': 'CRAQUE Defensivo'
        }
    )

    # Adicionar linhas de referência nos eixos X e Y para a coordenada (0,0)
    fig.add_shape(
        type="line",
        x0=0, y0=data_filtered['CRAQUE Defensivo'].min(),
        x1=0, y1=data_filtered['CRAQUE Defensivo'].max(),
        line=dict(color="Black", width=2)
    )

    fig.add_shape(
        type="line",
        x0=data_filtered['CRAQUE Ofensivo'].min(), y0=0,
        x1=data_filtered['CRAQUE Ofensivo'].max(), y1=0,
        line=dict(color="Black", width=2)
    )

    # Exibir o gráfico na página do Streamlit
    st.plotly_chart(fig, use_container_width=True)

elif page == "Tabela":
    st.title("Tabela")

    # Filtros na Tabela Geral
    campeonato = st.selectbox('Filtrar por Campeonato', options=['Todos'] + list(data['Campeonato'].unique()))
    if campeonato != 'Todos':
        data = data[data['Campeonato'] == campeonato]

    squad = st.selectbox('Filtrar por Clube', options=['Todos'] + list(data['Time'].unique()))
    if squad != 'Todos':
        data = data[data['Time'] == squad]

    jogador = st.selectbox('Filtrar por Jogador', options=['Todos'] + list(data['Jogador'].unique()))
    if jogador != 'Todos':
        data = data[data['Jogador'] == jogador]

    idade_min, idade_max = st.slider('Filtrar por Idade', int(data['Idade'].min()), int(data['Idade'].max()), (int(data['Idade'].min()), int(data['Idade'].max())))
    data = data[(data['Idade'] >= idade_min) & (data['Idade'] <= idade_max)]

    # Exibir a tabela geral com todos os filtros aplicados
    st.dataframe(data, height=500, use_container_width=True)

elif page == "Comparação de Jogadores":
    st.title("Comparação de Jogadores")

    # Seleção de dois jogadores para comparação
    jogador1 = st.selectbox('Selecione o Primeiro Jogador', options=data['Jogador'].unique())
    jogador2 = st.selectbox('Selecione o Segundo Jogador', options=data['Jogador'].unique())

    # Filtrar os dados dos jogadores selecionados
    comparacao = data[(data['Jogador'] == jogador1) | (data['Jogador'] == jogador2)]
    comparacao = comparacao[['Jogador', 'Time', 'Temporada', 'CRAQUE Ofensivo', 'CRAQUE Defensivo', 'WAR']]

    # Exibir a tabela comparativa
    st.write(f"Comparando {jogador1} e {jogador2}:")
    st.dataframe(comparacao.reset_index(drop=True))



