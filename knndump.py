from joblib import dump
from collaborativefiltering import rp

from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

def build_knn():
    book_sparse = csr_matrix(rp)
    model = NearestNeighbors(n_neighbors=10,algorithm='brute')
    model.fit(book_sparse)
    dump(model, "knn.joblib")
build_knn()