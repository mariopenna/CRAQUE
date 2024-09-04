import streamlit as st
import pandas as pd
import plotly.express as px

# URL of the CSV file on GitHub
url = 'https://raw.githubusercontent.com/mariopenna/CRAQUE/main/CRAQUE.csv'

# Load the CSV directly from GitHub
data = pd.read_csv(url)

# Rename columns to English
data = data.rename(columns={
    'Player': 'Player',
    'Nation': 'Nationality',
    'Idade': 'Age',
    'Born': 'Birth Date',
    'Squad': 'Team',
    'Pos': 'Position',
    'Campeonato': 'League',
    'Ano': 'Season',
    'MP': 'Matches Played',
    'Min': 'Minutes Played',
    'Gls': 'Goals',
    'Ast': 'Assists',
    'GCA': 'Goal-Creating Actions',
    'Cmp%_total': 'Pass Completion %',
    'TklW_tackles': 'Tackles Won',
    'Int_blocks': 'Interceptions',
    'CrdY_performance': 'Yellow Cards',
    'Won%_aereal-duels': 'Aerial Duels Won %',
    'RAPTOR_final_Off': 'CRAQUE Offensive',
    'RAPTOR_final_Def': 'CRAQUE Defensive',
    'RAPTOR_final_Total': 'CRAQUE Total',
    'WAR': 'WAR'
})

# Set up the sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["About", "General Analysis", "Table", "Player Comparison"])

if page == "About":
    st.title("CRAQUE Project: Calculating Athlete Performance")
    st.write("""
    Welcome to the **CRAQUE (Calculating Athlete Performance in Quality and Statistics)** project!

    Inspired by FiveThirtyEight's RAPTOR model, the CRAQUE model leverages detailed statistics and algorithms to evaluate each player's unique contribution on the field and quantify wins above a replacement player, adjusted for playing time.

    For more information, check out my presentation on LinkedIn: [LinkedIn Presentation](https://www.linkedin.com/feed/update/urn:li:activity:7226935140541710336/)

    Use the navigation menu on the left to explore graphical data analysis, view the general table with all players, or compare specific players.
    """)

elif page == "General Analysis":
    st.title("General Analysis")

    # League Filter
    league = st.selectbox('Select a League', options=['All'] + sorted(data['League'].unique()))
    if league != 'All':
        data = data[data['League'] == league]
        teams_available = data['Team'].unique()
    else:
        teams_available = data['Team'].unique()

    # Season Filter
    season = st.selectbox('Select a Season', options=['All'] + sorted(data['Season'].unique()))
    if season != 'All':
        data = data[data['Season'] == season]

    # Team Filter
    team = st.selectbox('Select a Team', options=['All'] + sorted(teams_available))
    if team != 'All':
        data = data[data['Team'] == team]

    # Age Filter
    age_min, age_max = st.slider('Select Age Range', int(data['Age'].min()), int(data['Age'].max()), (int(data['Age'].min()), int(data['Age'].max())))
    data_filtered = data[(data['Age'] >= age_min) & (data['Age'] <= age_max)]

    # Scatter Plot
    fig = px.scatter(
        data_filtered,
        x='CRAQUE Offensive',
        y='CRAQUE Defensive',
        color='Team',
        size_max=10,
        opacity=0.8,
        hover_name='Player',
        hover_data=['Season', 'Age', 'League'],
        title='CRAQUE Offensive vs. CRAQUE Defensive by Team',
        labels={
            'CRAQUE Offensive': 'CRAQUE Offensive',
            'CRAQUE Defensive': 'CRAQUE Defensive'
        }
    )

    # Add reference lines at (0,0)
    fig.add_hline(y=0, line_dash="dash", line_color="black")
    fig.add_vline(x=0, line_dash="dash", line_color="black")

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)

    # Explanation of Metrics
    st.write("""
    **Metrics Explanation:**
    
    - **CRAQUE Offensive**: Measures the player's offensive contribution to the team.
    - **CRAQUE Defensive**: Measures the player's defensive contribution to the team.
    - **CRAQUE Total**: The sum of offensive and defensive contributions.
    """)

elif page == "Table":
    st.title("Player Statistics Table")

    # League Filter
    league = st.selectbox('Filter by League', options=['All'] + sorted(data['League'].unique()))
    if league != 'All':
        data = data[data['League'] == league]
        teams_available = data['Team'].unique()
    else:
        teams_available = data['Team'].unique()

    # Season Filter
    season = st.selectbox('Filter by Season', options=['All'] + sorted(data['Season'].unique()))
    if season != 'All':
        data = data[data['Season'] == season]

    # Team Filter
    team = st.selectbox('Filter by Team', options=['All'] + sorted(teams_available))
    if team != 'All':
        data = data[data['Team'] == team]

    # Player Filter
    player = st.selectbox('Filter by Player', options=['All'] + sorted(data['Player'].unique()))
    if player != 'All':
        data = data[data['Player'] == player]

    # Age Filter
    age_min, age_max = st.slider('Filter by Age', int(data['Age'].min()), int(data['Age'].max()), (int(data['Age'].min()), int(data['Age'].max())))
    data = data[(data['Age'] >= age_min) & (data['Age'] <= age_max)]

    # Display the data table
    st.dataframe(data.reset_index(drop=True), height=500, use_container_width=True)

    # Explanation of WAR
    st.write("""
    **Metric Explanation:**
    
    - **WAR (Wins Above Replacement)**: Quantifies the number of additional wins a player contributes to their team compared to a replacement-level player, adjusted for playing time.
    """)

elif page == "Player Comparison":
    st.title("Player Comparison")

    # League Filter
    league = st.selectbox('Filter by League', options=['All'] + sorted(data['League'].unique()))
    if league != 'All':
        data = data[data['League'] == league]
        players_available = data['Player'].unique()
    else:
        players_available = data['Player'].unique()

    # Season Filter
    season = st.selectbox('Filter by Season', options=['All'] + sorted(data['Season'].unique()))
    if season != 'All':
        data = data[data['Season'] == season]

    # Select Players for Comparison
    player1 = st.selectbox('Select First Player', options=sorted(players_available))
    player2 = st.selectbox('Select Second Player', options=sorted(players_available))

    # Filter data for selected players
    comparison = data[data['Player'].isin([player1, player2])]

    # Select metrics to display
    metrics = st.multiselect(
        'Select Metrics to Compare',
        options=['Matches Played', 'Minutes Played', 'Goals', 'Assists', 'Goal-Creating Actions',
                 'Pass Completion %', 'Tackles Won', 'Interceptions', 'Yellow Cards',
                 'Aerial Duels Won %', 'CRAQUE Offensive', 'CRAQUE Defensive', 'CRAQUE Total', 'WAR'],
        default=['CRAQUE Offensive', 'CRAQUE Defensive', 'CRAQUE Total', 'WAR']
    )

    # Display comparison table
    st.write(f"**Comparing {player1} and {player2}:**")
    st.table(comparison[['Player', 'Team', 'Season'] + metrics].reset_index(drop=True))

    # Explanation of Metrics
    st.write("""
    **Metrics Explanation:**
    
    - **CRAQUE Offensive**: Measures the player's offensive contribution to the team.
    - **CRAQUE Defensive**: Measures the player's defensive contribution to the team.
    - **CRAQUE Total**: The sum of offensive and defensive contributions.
    - **WAR (Wins Above Replacement)**: Quantifies the number of additional wins a player contributes to their team compared to a replacement-level player, adjusted for playing time.
    """)

