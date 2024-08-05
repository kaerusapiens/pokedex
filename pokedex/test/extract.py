import pokebase as pb
import pandas as pd


# Pokemon dataframe
df = pd.DataFrame(columns=["generation","id","name_ja","name_ko","capture_rate","base_happiness","is_baby","is_legendary","is_mythical","evoles_name_ja","evoles_name_ko"])


# Append Pokemons to dataframe
def create_new_row(gen, pokemon_id, names, capture_rate, base_happiness, is_baby, is_legendary,is_mythical,evoles_name):
    return pd.DataFrame([{
        "generation": gen,
        "id": pokemon_id,
        "name_ja": names.get('ja', 'N/A'),
        "name_ko": names.get('ko', 'N/A'),
        "capture_rate": capture_rate,
        "base_happiness": base_happiness,
        "is_baby": is_baby,
        "is_legendary": is_legendary,
        "is_mythical": is_mythical,
        "evoles_name_ja": evoles_name.get('ja','N/A'),
        "evoles_name_ko": evoles_name.get('ko','N/A'),
    }])


# Generation Number (Gold/Silver)
GENERATION_NUM = [2]

# GET language options for pokemon
def get_names_in_languages(species, languages):
    names = dict()
    for name_entry in species.names:
        if name_entry.language.name in languages:
            names[name_entry.language.name] = name_entry.name
    return names


# Loop Gen
for gen in GENERATION_NUM:
    gen_resource = pb.generation(gen)
    # Append Data
    for index, pokemon in enumerate(gen_resource.pokemon_species):
        species = pb.pokemon_species(pokemon.name)
        capture_rate = species.capture_rate
        base_happiness = species.base_happiness
        is_baby = species.is_baby
        is_legendary = species.is_legendary
        is_mythical = species.is_mythical
        evolves_from_species = species.evolves_from_species

        names = get_names_in_languages(species, ['ko', 'ja'])
        evoles_name = get_names_in_languages(species, ['ko', 'ja'])

        new_row = create_new_row( gen, pokemon.id, names, capture_rate, base_happiness, is_baby, is_legendary,is_mythical, evoles_name)
        df = pd.concat([df, new_row], ignore_index=True)

