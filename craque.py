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

# Título da Página
st.title('CRAQUE: Cálculo de Rendimentos de Atletas em Qualidade e Estatísticas')

# Filtro por Campeonato
campeonato = st.selectbox('Selecione um Campeonato', options=['Todos'] + list(data['Campeonato'].unique()))
if campeonato != 'Todos':
    clubes_disponiveis = data[data['Campeonato'] == campeonato]['Time'].unique()
else:
    clubes_disponiveis = data['Time'].unique()

# Filtro por Clube (exibe apenas clubes do campeonato selecionado)
squad = st.selectbox('Selecione um Clube', options=['Todos'] + list(clubes_disponiveis))
if squad != 'Todos':
    jogadores_disponiveis = data[data['Time'] == squad]['Jogador'].unique()
else:
    jogadores_disponiveis = data['Jogador'].unique()

# Filtro por Jogador (exibe apenas jogadores do clube e campeonato selecionados)
player = st.selectbox('Selecione um Jogador', options=['Todos'] + list(jogadores_disponiveis))

# Filtro por Idade
idade_min, idade_max = st.slider('Selecione o intervalo de Idade', int(data['Idade'].min()), int(data['Idade'].max()), (int(data['Idade'].min()), int(data['Idade'].max())))
data_filtered = data[(data['Idade'] >= idade_min) & (data['Idade'] <= idade_max)]

# Aplicar filtros adicionais em data_filtered
if player != 'Todos':
    data_filtered = data_filtered[data_filtered['Jogador'] == player]
elif squad != 'Todos':
    data_filtered = data_filtered[data_filtered['Time'] == squad]
elif campeonato != 'Todos':
    data_filtered = data_filtered[data_filtered['Campeonato'] == campeonato]

# Destacar o jogador, clube ou campeonato selecionado
if player != 'Todos':
    data_filtered['Cor'] = 'Selecionado'
    color_discrete_map = {'Selecionado': 'red'}
elif squad != 'Todos':
    data_filtered['Cor'] = data_filtered['Time'].apply(lambda x: 'Selecionado' if x == squad else 'Outros')
    color_discrete_map = {'Selecionado': 'blue', 'Outros': 'lightgray'}
elif campeonato != 'Todos':
    data_filtered['Cor'] = data_filtered['Campeonato'].apply(lambda x: 'Selecionado' if x == campeonato else 'Outros')
    color_discrete_map = {'Selecionado': 'green', 'Outros': 'lightgray'}
else:
    data_filtered['Cor'] = 'Outros'
    color_discrete_map = None

# Gráfico de dispersão com Plotly
fig = px.scatter(
    data_filtered,
    x='CRAQUE Ofensivo',
    y='CRAQUE Defensivo',
    color='Cor',
    color_discrete_map=color_discrete_map,
    size_max=5,
    opacity=0.8,
    hover_name='Jogador',
    hover_data=['Temporada', 'Idade', 'Time', 'Campeonato'],
    title='Relação entre CRAQUE Ofensivo vs CRAQUE Defensivo',
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

# Exibir dados filtrados com largura ajustada
st.subheader("Dados Filtrados")
st.dataframe(data_filtered.drop(columns=['Cor']), height=300, use_container_width=True)


