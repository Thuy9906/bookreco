from surprise import Reader, Dataset, SVD
from joblib import dump
from collaborativefiltering import fr
def build_svd():
    svd=SVD()    
    reader = Reader()
    data = Dataset.load_from_df(fr[['user_id', 'book_id', 'rating']], reader)
    trainset = data.build_full_trainset()
    svd.fit(trainset)
    dump(svd, "svd.joblib")
build_svd()