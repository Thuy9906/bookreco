import numpy as np
import pandas as pd

import re
import string

# Importation des Données
book_tags = pd.read_csv("/home/simplon/PYTHON_CODE/goodbooks-10k-master/book_tags.csv")
tags = pd.read_csv("/home/simplon/PYTHON_CODE/goodbooks-10k-master/tags.csv")
books = pd.read_csv("/home/simplon/PYTHON_CODE/goodbooks-10k-master/books.csv")

# Liste des tags que l'on garde.
L_genre = ['fiction','fantasy','young-adult','classics','romance','ya','mystery','non-fiction','historical-fiction','series','science-fiction','sci-fi','paranormal','contemporary','horror','urban-fantasy','nonfiction','adult','classic','childrens','graphic-novels','thriller','vampires','adventure','history','dystopian','historical','humor','novels','chick-lit','literature','dystopia','paranormal-romance','children','magic','crime','comics','memoir','adult-fiction','children-s','sci-fi-fantasy','biography','children-s-books','supernatural','manga','philosophy','teen','graphic-novel','science','new-adult','suspense','novel','poetry','picture-books','school','contemporary-romance','childhood','plays','scifi','realistic-fiction','kids','short-stories','drama','vampire','middle-grade','contemporary-fiction','mystery-thriller','fantasy-sci-fi','literary-fiction','psychology','general-fiction','ya-fiction','historical-romance','childrens-books','mythology','mysteries','funny','ya-fantasy','business','action','memoirs','war','high-fantasy','scifi-fantasy','religion','humour','epic-fantasy','kids-books','young-adult-fiction','comedy','erotica','shelfari-favorites']


# fonction de traitement qui retire la ponctuation qui est en dehors d'un mot puis le transforme en minuscule
def traitement(tag):
    tag=tag.replace('\n',' ')
    
    tag=' '.join(word.strip(string.punctuation) for word in tag.split())
    tag=tag.lower()
    return tag

tags['tag_name']= tags['tag_name'].astype(str)
tags_2 = tags['tag_name'].apply(lambda tag: traitement(tag))

# Création d'un nouveau dataframe pour garder les meme ID de livres
tags_3 = tags.merge(tags_2,on=['tag_name'])

# Rajout des noms des tags dans le dataframe book_tags 
book_tags = book_tags.merge(tags_3,on='tag_id')

# Rajout des information Title du livre dans le dataframe book_tags
book_tags = book_tags.merge(books[['goodreads_book_id','title']], on = 'goodreads_book_id')


book_tags.loc[book_tags['count'] < 0, 'count'] = 0
#book_tags[book_tags['tag_name']!='to-read'].sort_values('count',ascending=False).head(15)

# selection des tags présent dans la liste de tags pour en garder seulement les plus pertinents
book_tags=book_tags[book_tags['tag_name'].isin(L_genre)]

# Suppresion des lignes double.
book_tags = book_tags.drop_duplicates()

# Fonction permettant de créé le dataframe plus vote book
# Ce Dataframe classe les livres avec une formule utilisé par IMDB 
# Cette formule prend en compte le nombre de vote ainsi que la moyenne


# m est le nombre minimum de vote pour apparraitre dans les recommandation,
# on selectionne les 10% des livres qui ont obtenu le plus de vote.
m = books['ratings_count'].quantile(0.9)

# C est la moyenne de chaque note moyenne de livre présent dans le data Books
C = books['average_rating'].mean()


def formule_IMDB(x,m=m,C=C):
    # v est le nombre de vote pour le livre x
    v = x['ratings_count']

    # R est la note moyenne pour le livre x
    R = x['average_rating']

    return (v/(v+m)*R) + (m/(m+v)*C)

def book_score_IMDB():
    # Ici on selectionne les 10% des livres qui ont obtenu le plus de vote.
    plus_vote_books = books.copy()

    # on calcule le score IMDB pour chaque livre avec la méthode apply
    # en le plaçant dans une nouvelle colonne
    plus_vote_books['score'] = plus_vote_books.apply(formule_IMDB, axis=1)

    # on trie les score du plus élevé au plus faible
    plus_vote_books = plus_vote_books.sort_values('score', ascending=False)

    plus_vote_books.reset_index(drop=True,inplace=True)

    return plus_vote_books

book_tags.reset_index(inplace=True,drop=True)
# Enregistrement du Dataframe final
book_tags.to_csv('book_tags_modif.csv')

plus_vote_books1 = book_score_IMDB()
plus_vote_books1.to_csv('plus_vote_books1.csv')
