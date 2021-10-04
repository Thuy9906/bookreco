
import pandas as pd
# Chargements des data

plus_vote_books = pd.read_csv('plus_vote_books1.csv')
book_tags = pd.read_csv("book_tags_modif.csv")


"""
utilisateur devra rentrer soit un id si il est déja présent dans la BDD
sinon il rentrera 'new' si c'est un nouveau utilisateur puis aura le choix de
renseigner ses genres de livres préférer parmis une liste proposée


Pour utilisateur Nouveau :

lui proposer 5 livres des genres qu'il a renseigner ayant
 le meilleur score avec la formule IMDB
ainsi que 5 livres (genres qu'il a renseigner)
 avec un score juste au dessus de la médiane des score IMDB
 
Pour l'utilisateur Connu :


"""



#liste des genres 
L_genre = ['fiction','fantasy','young-adult','classics','romance','ya','mystery','non-fiction','historical-fiction','series','science-fiction','sci-fi','paranormal',
'contemporary','horror','urban-fantasy','nonfiction','adult','classic','childrens','graphic-novels','thriller','vampires','adventure','history','dystopian','historical',
'humor','novels','chick-lit','literature','dystopia','paranormal-romance','children','magic','crime','comics','memoir','adult-fiction','children-s','sci-fi-fantasy',
'biography','children-s-books','supernatural','manga','philosophy','teen','graphic-novel','science','new-adult','suspense','novel','poetry','picture-books','school',
'contemporary-romance','childhood','plays','scifi','realistic-fiction','kids','short-stories','drama','vampire','middle-grade','contemporary-fiction','mystery-thriller',
'fantasy-sci-fi','literary-fiction','psychology','general-fiction','ya-fiction','historical-romance','childrens-books','mythology','mysteries','funny','ya-fantasy',
'business','action','memoirs','war','high-fantasy','scifi-fantasy','religion','humour','epic-fantasy','kids-books','young-adult-fiction','comedy','erotica',
'shelfari-favorites']
score_top = plus_vote_books['score'].iloc[4]


# Recommandation pour un nouvel utilisateur
def new_user():
    genre_liked_user1 = genre_liked_user()
    liste_book_user1 = list(book_tags['goodreads_book_id'][book_tags['tag_name'].isin(genre_liked_user1)].unique())

    score_top_user1 = plus_vote_books['score'][plus_vote_books['goodreads_book_id'].isin(liste_book_user1)].quantile(0.9995)

    top_books = plus_vote_books[plus_vote_books['goodreads_book_id'].isin(liste_book_user1)].copy().loc[plus_vote_books['score'] >= score_top]

    before = plus_vote_books[plus_vote_books['goodreads_book_id'].isin(liste_book_user1)].shape[0]//2
    after = before + top_books.shape[0]
    reco_audacieuse = plus_vote_books[plus_vote_books['goodreads_book_id'].isin(liste_book_user1)].truncate(before=before,after=after)

    reco_u1 = pd.concat([top_books,reco_audacieuse])

    reco_u1.reset_index(inplace=True,drop=True)
    return reco_u1

# Récupération des genres aimés par l'utilisateur
def genre_liked_user():
    genre_liked_user1 = list()
    print(L_genre)
    accord = str(input())
    genre_liked_user1.append(accord)
    while accord != 'non' :
        accord = input("entrer s'en de nouveu sinon taper non\n")
        if accord.lower() != 'non':
            genre_liked_user1.append(accord)
    return genre_liked_user1


