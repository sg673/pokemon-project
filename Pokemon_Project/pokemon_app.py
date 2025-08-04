import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests

df = pd.read_csv("pokemon.csv")

#TYPE CHART (GENERATED FROM CHATGPT)
type_chart = {
    "Normal":    {"Rock": 0.5, "Ghost": 0, "Steel": 0.5},
    "Fire":      {"Grass": 2, "Ice": 2, "Bug": 2, "Steel": 2, "Fire": 0.5, "Water": 0.5, "Rock": 0.5, "Dragon": 0.5},
    "Water":     {"Fire": 2, "Ground": 2, "Rock": 2, "Water": 0.5, "Grass": 0.5, "Dragon": 0.5},
    "Electric":  {"Water": 2, "Flying": 2, "Electric": 0.5, "Grass": 0.5, "Dragon": 0.5, "Ground": 0},
    "Grass":     {"Water": 2, "Ground": 2, "Rock": 2, "Fire": 0.5, "Grass": 0.5, "Poison": 0.5, "Flying": 0.5, "Bug": 0.5, "Dragon": 0.5, "Steel": 0.5},
    "Ice":       {"Grass": 2, "Ground": 2, "Flying": 2, "Dragon": 2, "Fire": 0.5, "Water": 0.5, "Ice": 0.5, "Steel": 0.5},
    "Fighting":  {"Normal": 2, "Rock": 2, "Steel": 2, "Ice": 2, "Dark": 2, "Ghost": 0, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Fairy": 0.5},
    "Poison":    {"Grass": 2, "Fairy": 2, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0},
    "Ground":    {"Fire": 2, "Electric": 2, "Poison": 2, "Rock": 2, "Steel": 2, "Grass": 0.5, "Bug": 0.5, "Flying": 0},
    "Flying":    {"Grass": 2, "Fighting": 2, "Bug": 2, "Electric": 0.5, "Rock": 0.5, "Steel": 0.5},
    "Psychic":   {"Fighting": 2, "Poison": 2, "Psychic": 0.5, "Steel": 0.5, "Dark": 0},
    "Bug":       {"Grass": 2, "Psychic": 2, "Dark": 2, "Fire": 0.5, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Ghost": 0.5, "Steel": 0.5, "Fairy": 0.5},
    "Rock":      {"Fire": 2, "Ice": 2, "Flying": 2, "Bug": 2, "Fighting": 0.5, "Ground": 0.5, "Steel": 0.5},
    "Ghost":     {"Ghost": 2, "Psychic": 2, "Dark": 0.5, "Normal": 0},
    "Dragon":    {"Dragon": 2, "Steel": 0.5, "Fairy": 0},
    "Dark":      {"Ghost": 2, "Psychic": 2, "Fighting": 0.5, "Dark": 0.5, "Fairy": 0.5},
    "Steel":     {"Rock": 2, "Ice": 2, "Fairy": 2, "Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Steel": 0.5},
    "Fairy":     {"Fighting": 2, "Dragon": 2, "Dark": 2, "Fire": 0.5, "Poison": 0.5, "Steel": 0.5},
}

def get_pokedex_entry(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}/"
    response = requests.get(url)
    if response.status_code != 200:
        return "Pokédex entry unavailable."

    data = response.json()
    for entry in data['flavor_text_entries']:
        if entry['language']['name'] == 'en' and entry['version']['name'] in ['sword', 'shield', 'scarlet', 'violet']:
            return entry['flavor_text'].replace('\n', ' ').replace('\f', ' ').strip()
    for entry in data['flavor_text_entries']:
        if entry['language']['name'] == 'en':
            return entry['flavor_text'].replace('\n', ' ').replace('\f', ' ').strip()
    return "No English Pokédex entry found."

def get_matchup_score(attacker_types, defender_types):
    if not attacker_types or not defender_types:
        return 1.0
    multiplier = 1.0
    for atk in attacker_types:
        if atk in type_chart:
            for dfn in defender_types:
                effectiveness = type_chart.get(atk, {}).get(dfn, 1.0)
                multiplier *= effectiveness
    return round(multiplier, 2)

def display_type_vs_type(p1, p2):
    st.subheader("Matchup Between the Two Pokémon")

    p1_types = [p1['type_1']]
    if pd.notna(p1['type_2']):
        p1_types.append(p1['type_2'])

    p2_types = [p2['type_1']]
    if pd.notna(p2['type_2']):
        p2_types.append(p2['type_2'])

    a_vs_b = get_matchup_score(p1_types, p2_types)
    b_vs_a = get_matchup_score(p2_types, p1_types)

    st.markdown(f"🔺 **{p1['name']} attacking {p2['name']}**: `{a_vs_b}×` effectiveness")
    st.markdown(f"🔻 **{p2['name']} attacking {p1['name']}**: `{b_vs_a}×` effectiveness")

#SIDEBAR BIT
st.sidebar.title("Options")
compare_mode = st.sidebar.checkbox("Compare two Pokémon?", value=False)
search_mode = st.sidebar.radio("Search mode", ["Name", "Pokédex Number"], horizontal=True)

if search_mode == "Name":
    pokemon_list = sorted(df['name'].unique().tolist())
    display_map = {name: name for name in pokemon_list}
else:
    df_sorted = df.sort_values(by="pokedex_number")
    pokemon_list = df_sorted.apply(lambda row: f"#{int(row['pokedex_number']):03d} {row['name']}", axis=1).tolist()
    display_map = {f"#{int(row['pokedex_number']):03d} {row['name']}": row['name'] for _, row in df_sorted.iterrows()}

poke1_display = st.sidebar.selectbox("Select First Pokémon", pokemon_list)
poke2_display = st.sidebar.selectbox("Select Second Pokémon", pokemon_list) if compare_mode else None

poke1_name = display_map[poke1_display]
poke2_name = display_map[poke2_display] if compare_mode else None

poke1 = df[df['name'] == poke1_name].iloc[0]
poke2 = df[df['name'] == poke2_name].iloc[0] if compare_mode else None

def display_pokemon_info(p, large_image=False):
    size = 240 if large_image else 96
    st.image(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{int(p['pokedex_number'])}.png", width=size)
    st.markdown(f"**Name:** {p['name']}")
    st.markdown(f"**Height:** {p['height_m']} m")
    st.markdown(f"**Weight:** {p['weight_kg']} kg")
    st.markdown(f"**Type(s):** {p['type_1']}" + (f", {p['type_2']}" if pd.notna(p['type_2']) else ""))
    st.markdown(f"**Species:** {p['species']}")
    st.markdown(f"**Generation:** {p['generation']}")
    st.markdown(f"**Total Base Stats:** {p['total_points']}")
    st.markdown(f"**Pokédex Entry:** {get_pokedex_entry(int(p['pokedex_number']))}")

def display_type_matchups(pokemon_row):
    st.subheader("Type Matchups")
    matchup_cols = [col for col in pokemon_row.index if col.startswith("against_")]
    matchup_data = pd.DataFrame({
        "Type": [col.replace("against_", "").capitalize() for col in matchup_cols],
        "Effectiveness": [pokemon_row[col] for col in matchup_cols]
    })
    matchup_data = matchup_data.sort_values(by="Effectiveness", ascending=False).reset_index(drop=True)

    def color_scale(val):
        if val >= 2.0:
            return "background-color: #ffcccc"
        elif val == 1.0:
            return "background-color: #ffffcc"
        elif val < 1.0:
            return "background-color: #ccffcc"
        return ""

    styled = matchup_data.style.applymap(color_scale, subset=["Effectiveness"])
    st.dataframe(styled, use_container_width=True)

def radar_chart(p1, p2):
    stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
    p1_stats = p1[stats].values.flatten().tolist()
    p2_stats = p2[stats].values.flatten().tolist()

    labels = stats
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    p1_stats += p1_stats[:1]
    p2_stats += p2_stats[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, p1_stats, label=p1['name'])
    ax.fill(angles, p1_stats, alpha=0.25)
    ax.plot(angles, p2_stats, label=p2['name'])
    ax.fill(angles, p2_stats, alpha=0.25)

    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_title("Stat Comparison")
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
    st.pyplot(fig)

#MAIN USER INETRFACE
st.title("Pokémon Info & Comparison")

if compare_mode:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"{poke1['name']}")
        display_pokemon_info(poke1)
        display_type_matchups(poke1)
    with col2:
        st.subheader(f"{poke2['name']}")
        display_pokemon_info(poke2)
        display_type_matchups(poke2)
    display_type_vs_type(poke1, poke2)
    radar_chart(poke1, poke2)
else:
    center_col = st.columns([1, 2, 1])[1]
    with center_col:
        st.subheader(f"{poke1['name']}")
        display_pokemon_info(poke1, large_image=True)
        display_type_matchups(poke1)

    #HeightVsWeightGraph
    st.subheader("Height vs Weight Comparison")
    sample_df = df.sample(30, random_state=1)
    sample_df = pd.concat([sample_df, pd.DataFrame([poke1])], ignore_index=True)

    fig, ax = plt.subplots()
    ax.scatter(sample_df['height_m'], sample_df['weight_kg'], alpha=0.6, label="Other Pokémon")
    ax.scatter(poke1['height_m'], poke1['weight_kg'], color='red', label=poke1['name'], s=100)
    ax.set_xlabel("Height (m)")
    ax.set_ylabel("Weight (kg)")
    ax.set_title(f"{poke1['name']}: Compared to Random Pokémon")
    ax.legend()
    st.pyplot(fig)



