# Setup imports to work from root
# Prevents module not found errors when running from app.py by setting all
# file relationships to be relative to root
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import core.load_data as load_data
import core.transform_data as transform_data
import pandas as pd
import plotly.express as px
import core.random_df as rd
import numpy as np



def format_type(types: list) -> str:
    """
    Converts the types into html with colours.
    """
    # A dictionary to map types to their colours
    type_dict = {
        "Normal": "#A8A77A",
        "Fire": "#EE8130",
        "Water": "#6390F0",
        "Electric": "#F7D02C",
        "Grass": "#7AC74C",
        "Ice": "#96D9D6",
        "Fighting": "#C22E28",
        "Poison": "#A33EA1",
        "Ground": "#E2BF65",
        "Flying": "#A98FF3",
        "Psychic": "#F95587",
        "Bug": "#A6B91A",
        "Rock": "#B6A136",
        "Ghost": "#735797",
        "Dragon": "#6F35FC",
        "Dark": "#705746",
        "Steel": "#B7B7CE",
        "Fairy": "#D685AD"
    }
    output = "<div style='display: flex; gap: 5px;'>"
    for t in types:
        output += (
            f"<span style='background-color: {type_dict[t]}; "
            f"padding: 5px; border-radius: 5px;'>{t}</span>"
        )
    output += "</div>"
    return output


def main_page():
    st.title("Pokémon Dataset Explorer")
    # Load the Pokémon data
    df = transform_data.clean_data()

    search_type = st.radio("Search by:", ["Pokédex Number", "Name"])
    # Based on the search type, show the appropriate input
    if search_type == "Pokédex Number":
        pokedex_num = st.number_input(
            "Enter Pokédex Number",
            min_value=1,
            max_value=898,
            value=1
        )
        all_pokemon_with_number = df[df["pokedex_number"] == pokedex_num]
    else:
        name = st.selectbox("Select Pokémon Name", df["name"].values)
        selected_pokemon = df[df["name"] == name]
        pokedex_num = selected_pokemon.iloc[0]["pokedex_number"]
        all_pokemon_with_number = df[df["pokedex_number"] == pokedex_num]
    variants = False
    if (len(all_pokemon_with_number) > 1):
        variants = True

    poke_info = all_pokemon_with_number.iloc[0]

    disp1, disp2 = st.columns(2)

    with disp1:
        st.header(poke_info["name"])
    with disp2:
        if variants:
            out = ""
            for index, row in all_pokemon_with_number.iterrows():
                out += f"<li>{row['name']}</li>"
            with st.expander("Variants available:"):
                st.markdown(f"<ul>{out}</ul>", unsafe_allow_html=True)

    # Center the image
    img1, img2, img3 = st.columns(3)
    img2.image(
        (
            f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"
            f"{int(pokedex_num)}.png"
        ),
        width=300
    )

    st.write("### Type")
    types = [
        poke_info[f"type_{i + 1}"]
        for i in range(poke_info["type_number"])
    ]
    stat1,stat2 = st.columns(2)
    
    stat1.markdown(format_type(types), unsafe_allow_html=True)
    stat2.write(f"**Height:** {poke_info['height_m']} m | **Weight:** {poke_info['weight_kg']} kg")

    st.write(" ### Stats")
    st.table(poke_info[[
        "hp",
        "attack",
        "defense",
        "speed",
        "sp_attack",
        "sp_defense"
    ]].to_frame().T)
    
    weight_df = rd.generate_random_rows(df, poke_info["pokedex_number"], 5)
    poke_info_df = poke_info.to_frame().T
    fig_df = pd.concat([weight_df, poke_info_df], ignore_index=True)
    # Add a column to indicate if the row is the selected Pokémon
    fig_df["highlight"] = fig_df["pokedex_number"].apply(lambda x: "Selected" if x == poke_info["pokedex_number"] else "Other")
    fig = px.bar(
        fig_df,
        x = "name",
        y = "weight_kg",
        labels = {"name": "Name", "weight_kg": "Weight (kg)"},
        text = "weight_kg",
        color = "highlight",
        color_discrete_map={"Selected": "Green", "Other": "Blue"},
    )
    fig.update_layout(xaxis_title="Name", yaxis_title="Weight (kg)", xaxis={'categoryorder': 'total ascending'})

    st.plotly_chart(fig)

    radar_chart(poke_info)


def radar_chart(p1):
    stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']

    fig = px.line_polar(p1, r=p1[stats].values, theta=stats, line_close=True)
    fig.update_traces(fill='toself', line_color='#FF6B6B')

    st.plotly_chart(fig)


if __name__ == "__main__":
    main_page()