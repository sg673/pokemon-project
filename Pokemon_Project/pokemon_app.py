import streamlit as st
import pandas as pd

df = pd.read_csv("pokemon.csv")

def display_pokemon_info(p):
    st.image(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{int(p['pokedex_number'])}.png")
    st.markdown(f"**Name:** {p['name']}")
    st.markdown(f"**Height:** {p['height_m']} m")
    st.markdown(f"**Weight:** {p['weight_kg']} kg")
    st.markdown(f"**Type(s):** {p['type_1']}" + (f", {p['type_2']}" if pd.notna(p['type_2']) else ""))
    st.markdown(f"**Species:** {p['species']}")
    st.markdown(f"**Generation:** {p['generation']}")
    st.markdown(f"**Total Base Stats:** {p['total_points']}")

#sidebar bit
st.sidebar.title("Select Pokémon")
poke1_num = st.sidebar.number_input("First Pokémon Number", min_value=1, max_value=898, step=1, value=1)
poke2_num = st.sidebar.number_input("Second Pokémon Number", min_value=1, max_value=898, step=1, value=4)

#getting bith pkmn
poke1 = df[df['pokedex_number'] == poke1_num]
poke2 = df[df['pokedex_number'] == poke2_num]

if poke1.empty or poke2.empty:
    st.warning("One or both Pokémon not found.")
else:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"{poke1.iloc[0]['name']} (#{poke1_num})")
        display_pokemon_info(poke1.iloc[0])
        
    with col2:
        st.subheader(f"{poke2.iloc[0]['name']} (#{poke2_num})")
        display_pokemon_info(poke2.iloc[0])
        
    
