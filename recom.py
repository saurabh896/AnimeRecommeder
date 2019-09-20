import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
df=pd.read_csv('rating.csv')
anime=pd.read_csv('anime.csv')
df=pd.merge(df,anime.drop('rating',axis=1),on='anime_id')
print(df.head())
print(df.groupby('name')['rating'].mean().sort_values(ascending=False).head(10))


ratings = pd.DataFrame(df.groupby('name')['rating'].mean())
ratings['num of ratings'] = pd.DataFrame(df.groupby('name')['rating'].count())

genre_dict = pd.DataFrame(data=anime[['name','genre']])
genre_dict.set_index('name',inplace=True)


def check_genre(genre_list,string):
    if any(x in string for x in genre_list):
        return True
    else:
        return False




def get_recommendation(name):
    anime_genre=genre_dict.loc[name].values[0].split(',')
    cols=anime[anime['genre'].apply(lambda x:check_genre(anime_genre,str(x)))]['name'].tolist()
    animemat=df[df['name'].isin(cols)].pivot_table(index='user_id',columns='name',values='rating')
    anime_user_rating=animemat[name]
    similar_anime=animemat.corrwith(anime_user_rating)
    corr_anime=pd.DataFrame(similar_anime,columns=['correlation'])
    corr_anime=corr_anime.join(ratings['num of rating'])
    corr_anime.dropna(inplace=True)
    corr_anime = corr_anime[corr_anime['num of ratings']>5000].sort_values(
        'correlation',ascending=False)
    return corr_anime.head(10)
    
get_recommendation('Kimi no Na wa.')