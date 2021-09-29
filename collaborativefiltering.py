"""
Colaborative filtering
Données utilisées : ratings

Préprocessing : 5%

. des livres les plus notés

. des utilisateurs les plus collaboratifs (qui ont donné le plus de notes)

Construire la table pivot qui va servir au modèle :

. CF memory-based (proposer des livres similaires à un livre lu/consulté récemment)

. CF model-based (proposer des livres qui pourraient être bien notés par l'utilisateur)

Mapping book_id - titre

"""

import pandas as pd
r = pd.read_csv( 'data/ratings.csv' )
b = pd.read_csv( 'data/books.csv' )

# filtrer les livres les  plus notés
def filter_top_5quantile_books():
    reviews_per_book = r.groupby( 'book_id' ).book_id.apply( lambda x: len( x ))
    xb = r['book_id'].value_counts() > reviews_per_book.quantile(0.95)
    yb = xb[xb].index
    bratings = r[r['book_id'].isin(yb)]    
    return bratings

# filtrer les utilisateurs les plus collaboratifs
def filter_top_5quantile_users():
    reviews_per_user = r.groupby( 'user_id' ).user_id.apply( lambda x: len( x ))
    xu = r['user_id'].value_counts() > reviews_per_user.quantile(0.95)
    yu = xu[xu].index  #user_ids
    print(yu.shape)
    uratings = r[r['user_id'].isin(yu)]
    return uratings

# garder uniquement les notations données aux top livres par les top utilisateurs
def merge_books_users_filter():
    uratings = filter_top_5quantile_users()
    bratings = filter_top_5quantile_books()
    return pd.merge(uratings, bratings, on=['user_id', 'book_id', 'rating'])

# afficher les notations données par un utilisateurs pour un livre sous forme de matrice
def pivot_ratings():
    ratings_pivot = fr.pivot_table(columns='user_id', index='book_id', values="rating")
    ratings_pivot.fillna(0, inplace=True)
    return ratings_pivot


def map_id_title(iid):
    return b[b['book_id']==iid].iloc[0]['title']


fr = merge_books_users_filter()
rp = pivot_ratings() 
top_users = fr['user_id'].unique()
top_books = fr['book_id'].unique()
b2 = b[b['book_id'].isin(top_books)][['book_id', 'title']]

"""

rp_knn=pr_knn()
def pr_knn():
    rp_knn=fr.merge(b2, on='book_id').pivot_table(columns='user_id', index='title', values="rating")
    rp_knn.fillna(0, inplace=True)
    return rp_knn

"""