"""
Collabotative filtering memory-based (Item-Item filtering)

Objectif : 
Proposer un livre similaire à un livre qui a été consulté basé sur la notation des utilisateurs

Etapes :
1 Créer une CSR (matrice creuse compressée) pour entraîner un modèle knn

2 Proposer les k livres les plus proches à un livre récemment consulté/lu
"""

from collaborativefiltering import rp, map_id_title, top_books
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
def recommend_similary_books(book_id=26):
    book_sparse = csr_matrix(rp)
    print(book_sparse)

    model = NearestNeighbors(n_neighbors=10,algorithm='brute')
    model.fit(book_sparse)
    distances, suggestions = model.kneighbors(rp.loc[book_id, :].values.reshape(1, -1)) # rp.iloc[0, :].values.reshape(1, -1)
    sim_books = []
    for i in range(len(suggestions)):
        sim_books.append(suggestions[i])
    print('livres similaires au dernier livre consulté', sim_books)   

"""
def map_csr_rp():
    userId_map = {new_id: old_id for new_id, old_id in enumerate(top_books)}
    inverse_userId_map = {old_id: new_id for new_id, old_id in enumerate(top_books)}
    return userId_map, inverse_userId_map

"""

# recommend_similary_books(826)