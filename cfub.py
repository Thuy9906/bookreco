"""
Collabotative filtering model-based (Matrix Factorization based algorithm)

objectif : 
Proposer un livre qui est susceptible d'être bien noté par l'utilisateur (au delà de 4.0 par exemple)

Etapes
1 Construire le modèle

2 Utiliser le modèle pour estimer la note donnée à un livre par un utilisateur (conditions : livre et utilisateur dans les 5% retenus pour le dataframe d'entraînement)

3 Boucler sur toute la liste des livres et proposer les livres avec les meilleures estimations de note
"""

import pandas as pd
from collaborativefiltering import rp, fr, map_id_title
from surprise import Reader, Dataset, SVD

# step 1 CF UB
def build_svd():
    svd=SVD()    
    reader = Reader()
    data = Dataset.load_from_df(fr[['user_id', 'book_id', 'rating']], reader)
    trainset = data.build_full_trainset()
    svd.fit(trainset)
    return svd

svd = build_svd()

# step 2 CF UB
def estimate_rating(uid, iid):
    return svd.predict(uid, iid).est

# step 3 CF UB
def recommend_best_est_books(userid, threeshold = 4): 
    # liste des livres que l'utilisateur n'a pas notés (= à noter)
    books_to_rate = rp[rp.loc[:, userid]==0].loc[:, userid]   
    # un dictionnaire pour stocker la note à estimer pour chaque livre
    rating_est={}
    # liste des recommandations
    books_to_recommend = []
    # pour chaque livre à noter
    for key, value in books_to_rate.items():
        # ajouter la note estimée au dictionnaire
        rating_est[key]=estimate_rating(userid, key)
        # si l'estimation est supérieure au seuil
        if rating_est[key] >= threeshold :
            # ajouter le livre à la liste des recommandations
            books_to_recommend.append(map_id_title(key))
    print ("basé sur les notes que vous avez données, voici les livres que vous pourriez aimer", books_to_recommend)
    #print ("nombre de livres à recommander : ", len(books_to_recommend))
    #print ("nombre de livres non notés : ", len(rating_est))
    
# fonction appelée seulement pour les uid dans les 5% les plus collaboratifs
def cfub(uid=75):
    recommend_best_est_books(uid)

"""
def recommend_best_est_books(userid, threeshold = 4): 
    # liste des livres que l'utilisateur n'a pas notés
    books_to_rate = rp[rp[:,userid]==0]   
    # un dictionnaire pour stocker la note à estimer pour chaque livre
    rating_est={}
    # pour chaque livre à noter
    for book in books_to_rate:
        # ajouter la note estimée au dictionnaire
        rating_est[book]=estimate_rating(userid, book)
    df_re=pd.DataFrame.from_dict(rating_est, columns=['book_id', 'rating_est'])
    df_re.set_index('book_id')
    # afficher les livres avec une estimation supérieure au seuil donné
    df_re[df_re['rating_est'] >= threeshold]
"""
