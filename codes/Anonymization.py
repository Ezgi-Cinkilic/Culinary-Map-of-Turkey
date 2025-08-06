import pandas as pd

recipes = pd.read_csv('../datas/recipes_combined.csv')
profiles = pd.read_csv('../datas/profiles.csv')
cullinary = pd.read_csv('../datas/CullinaryMapDataset.csv')

all_profiles = pd.concat([
    recipes['profil_adi'],
    profiles['profil_adi'],
    cullinary['profil_adi']
]).unique()

start_id = 100000
user_ids = range(start_id, start_id + len(all_profiles))
mapping_df = pd.DataFrame({
    'profil_adi': all_profiles,
    'user_id': [f"{uid:06d}" for uid in user_ids]
})

def anonymize(df):
    df_new = df.merge(mapping_df, on='profil_adi').drop(columns=['profil_adi'])
    df_new = df_new.rename(columns={'user_id':'profil_id'})
    return df_new

recipes_anon = anonymize(recipes)
profiles_anon = anonymize(profiles)
cullinary_anon = anonymize(cullinary)

recipes_anon.to_csv('../datas/recipes_anon.csv', index=False)
profiles_anon.to_csv('../datas/profiles_anon.csv', index=False)
cullinary_anon.to_csv('../datas/CullinaryMapDataset_anon.csv', index=False)
mapping_df.to_csv('../datas/user_mapping.csv', index=False)

print("Anonim dosyalar (recipes_anon.csv, profiles_anon.csv, CullinaryMapDataset_anon.csv) ve mapping (user_mapping.csv) üretildi.")
