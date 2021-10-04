"""
Collabotative filtering model-based (Clustering algorithm)

Objectif : 
Proposer un livre similaire à un livre qui a été consulté basé sur la notation des utilisateurs

Etapes :
1 Créer une CSR (matrice creuse compressée) pour entraîner un modèle knn

2 Proposer les k livres les plus proches à un livre récemment consulté/lu
"""

from collaborativefiltering import rp, map_id_title, top_books
from joblib import load
import pandas as pd
import numpy as np

def recommend_similar_books(book_id=26):
    model = load("knn.joblib")
    distances, suggestions = model.kneighbors(rp.loc[book_id, :].values.reshape(1, -1)) # rp.iloc[0, :].values.reshape(1, -1)
    sim_books = []
    for i in range(suggestions.shape[1]):
        csr_id = suggestions[0,i]
        book_id = dict_csr_rp.get(csr_id)
        book = map_id_title(book_id)
        sim_books.append(book) 
    print('(réponse de requête API) recommandation avec le clustering : \n', sim_books)   
    

def map_csr_rp():
    userId_map = {new_id: old_id for new_id, old_id in enumerate(top_books)}
    inverse_userId_map = {old_id: new_id for new_id, old_id in enumerate(top_books)}
    dict_csr_rp = dict(zip(np.vectorize(inverse_userId_map.get)(top_books), top_books))
    return dict_csr_rp

dict_csr_rp = map_csr_rp()