import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io

# Baixar o arquivo do Google Drive (link direto)
url = 'https://drive.google.com/uc?export=download&id=1H6w0iTV3XysicSkJRsRfbE62nRTkzLds'

@st.cache_data(hash_funcs={"requests.sessions.Session": id})
def load_data():
    try:
        r = requests.get(url)
        r.raise_for_status()  # Verificar se houve erro na requisição
        data = pd.read_csv(io.StringIO(r.text))
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro

data = load_data()

if data.empty:
    st.stop()  # Para a execução do app se os dados não forem carregados

# Filtros e ajustes na data_filtered
campeonato = st.selectbox('Selecione um Campeonato', options=['Todos'] + list(data['Campeonato'].unique()))
if campeonato != 'Todos':
    clubes_disponiveis = data[data['Campeonato'] == campeonato]['Squad'].unique()
else:
    clubes_disponiveis = data['Squad'].unique()

squad = st.selectbox('Selecione um Clube', options=['Todos'] + list(clubes_disponiveis))
if squad != 'Todos':
    jogadores_disponiveis = data[data['Squad'] == squad]['Player'].unique()
else:
    jogadores_disponiveis = data['Player'].unique()

player = st.selectbox('Selecione um Jogador', options=['Todos'] + list(jogadores_disponiveis))

idade_min, idade_max = st.slider('Selecione o intervalo de Idade', int(data['Idade'].min()), int(data['Idade'].max()), (int(data['Idade'].min()), int(data['Idade'].max())))
data_filtered = data[(data['Idade'] >= idade_min) & (data['Idade'] <= idade_max)]

# Destacar o jogador, clube ou campeonato selecionado
if player != 'Todos':
    data_filtered['Cor'] = data_filtered['Player'].apply(lambda x: 'Selecionado' se x == player else 'Outros')
    color_discrete_map = {'Selecionado': 'red', 'Outros': 'lightgray'}
elif squad != 'Todos':
    data_filtered['Cor'] = data_filtered['Squad'].apply(lambda x: 'Selecionado' se x == squad else 'Outros')
    color_discrete_map = {'Selecionado': 'blue', 'Outros': 'lightgray'}
elif campeonato != 'Todos':
    data_filtered['Cor'] = data_filtered['Campeonato'].apply(lambda x: 'Selecionado' se x == campeonato else 'Outros')
    color_discrete_map = {'Selecionado': 'green', 'Outros': 'lightgray'}
else:
    data_filtered['Cor'] = 'Outros'
    color_discrete_map = None

# Verificar se todas as colunas necessárias existem em data_filtered
if 'RAPTOR_final_Off' in data_filtered.columns and 'RAPTOR_final_Def' in data_filtered.columns:
    # Gráfico de dispersão com Plotly
    fig = px.scatter(
        data_filtered,
        x='RAPTOR_final_Off',
        y='RAPTOR_final_Def',
        color='Cor',
        color_discrete_map=color_discrete_map,
        size_max=5,
        opacity=0.8,
        hover_name='Player',
        hover_data=['Ano', 'Idade', 'Squad', 'Campeonato'],
        title='Relação entre RAPTOR_final_Off e RAPTOR_final_Def',
        labels={
            'RAPTOR_final_Off': 'RAPTOR Final Off',
            'RAPTOR_final_Def': 'RAPTOR Final Def'
        }
    )

    # Adicionar linhas de referência nos eixos X e Y para a coordenada (0,0)
    fig.add_shape(
        type="line",
        x0=0, y0=data_filtered['RAPTOR_final_Def'].min(),
        x1=0, y1=data_filtered['RAPTOR_final_Def'].max(),
        line=dict(color="Black", width=2)
    )

    fig.add_shape(
        type="line",
        x0=data_filtered['RAPTOR_final_Off'].min(), y0=0,
        x1=data_filtered['RAPTOR_final_Off'].max(), y1=0,
        line=dict(color="Black", width=2)
    )

    # Exibir o gráfico na página do Streamlit
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("As colunas 'RAPTOR_final_Off' ou 'RAPTOR_final_Def' não foram encontradas.")

# Exibir dados do jogador, clube ou campeonato selecionado
if player != 'Todos':
    st.subheader(f"Dados do Jogador Selecionado: {player}")
    player_data = data[data['Player'] == player]
    st.dataframe(player_data, height=300)
elif squad != 'Todos':
    st.subheader(f"Dados do Clube Selecionado: {squad}")
    squad_data = data[data['Squad'] == squad]
    st.dataframe(squad_data, height=300)
elif campeonato != 'Todos':
    st.subheader(f"Dados do Campeonato Selecionado: {campeonato}")
    campeonato_data = data[data['Campeonato'] == campeonato]
    st.dataframe(campeonato_data, height=300)
