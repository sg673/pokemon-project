# Setup imports to work from root
# Prevents module not found errors when running from app.py by setting all
# file relationships to be relative to root
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import core
from core import load_data as ld
import pandas as pd

# Join evolution data onto initial dataset
def join_evo_data(data):
    # Read additional dataset to obtain evolution data
    pre_evolution_df = pd.read_csv('data/pokemon_dex.csv', delimiter='\t', encoding="utf-16")
    # Set index of new dataframe to match existing dataset column
    pre_evolution_df.set_index('pokedex_number', inplace=True)
    # Set index of existing dataset to identical column and join wanted column on index
    # Join left to match incoming data to existing records
    t_data = pd.DataFrame(data).set_index('pokedex_number').join(pre_evolution_df['description'], how='left')
    # Return joined dataset
    return t_data

# Clean joined dataset, drop unwanted columns and remove duplicates
def clean_data():
    # Call function to create joined dataset
    data_df = join_evo_data(ld.load_data())
    # create new dataset only containing wanted columns
    clean_df = data_df[[
        'name', 
        'description',  
        'generation', 
        'status',
        'type_number',
        'type_1',
        'type_2',
        'height_m',
        'weight_kg',
        'total_points',
        'hp',
        'attack',
        'defense',
        'sp_attack',
        'sp_defense',
        'speed',
        'percentage_male',
        'against_normal',
        'against_fire',
        'against_water',
        'against_electric',
        'against_grass',
        'against_ice',
        'against_fight',
        'against_poison',
        'against_ground',
        'against_flying',
        'against_psychic',
        'against_bug',
        'against_rock',
        'against_ghost',
        'against_dragon',
        'against_dark',
        'against_steel',
        'against_fairy']]
    # Drop duplicates created from joining datasets
    clean_df.drop_duplicates(inplace=True)
    # Return clean dataframe
    return clean_df.reset_index()
    

if __name__ == "__main__":
    # Auto run for debugging
    print(clean_data())
