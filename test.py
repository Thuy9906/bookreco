import numpy as np

from collaborativefiltering import top_users, b2
from cfub import cfub

from cfib import recommend_similar_books
from new import new_user

# Initialisation de l'utilisateur 
def run():
    print("(paramètre de requête API) : ID utilisateur, ou 'NEW' pour un nouvel utilisateur.")
    print("Liste d'ID utilisateur ayant servi à entraîner l'IA.",top_users, "\n")
    ID = input()
    print ('(paramètre de requête API) : au moins un genre de livre renseigné par l\'utilisateur parmis la liste \n')
    reco_u1 = new_user()
    print('(paramètre de requête API) : id du livre actuellement ou récemment consulté\n', b2)
    iid = int(input())    
    if ID.isnumeric():
        if int(ID) in top_users:
            cfub(int(ID))
        else :
            print('l\'id renseigné n\'est pas dans la liste proposée')
    print("(réponse de requête API) recommandation basée sur les genres favoris :\n", list(reco_u1['original_title']))    
    recommend_similar_books(iid)                 


run()