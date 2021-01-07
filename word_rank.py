
import sys
import time
import numpy as np


def read_doc(filepath):

    with open(filepath, 'rt', encoding='utf-8') as fp:
        doc = [line for line in fp.read().splitlines() if line.strip() != '']

    return doc



def load_stopwords(filepath):
    """Loads stopwords from text file."""

    with open(filepath, 'rt') as fp:
        stopwords = set(fp.read().split())

    return stopwords



def get_sentences(doc):
    assert isinstance(doc, list)

    from re import split

    sentences = []
    for line in doc:
        sent = [s.strip() for s in split(r"[\?!.]", line)]
        sentences += (([s for s in sent if s != '']))

    return sentences


def clean(s):
    from re import finditer
    pattern = r"[a-z]+('[a-z])?[a-z]*"

    return [match.group(0) for match in finditer(pattern, s.lower())]


# Bag of Words
def gen_bag_of_words(sents):
    assert isinstance(sents, list)

    # load stopwords
    STOPWORDS = load_stopwords('data/english_stopwords.txt')

    ls = [None] * len(sents)
    for i, s in enumerate(sents):
        ls[i] = set([w for w in (set(clean(s))) if w not in STOPWORDS])

    return ls


def create_ids(bags):
    """
    Given a bag of words, creates a dictionary word index and a
    reverse lookup from ID to word.

    Returns:
        Tuple of two dictionaries
        `word_to_id` and `id_to_word`

    """
    # Generate Word IDs
    from random import choices

    all_words = set()
    for b in bags:
        all_words |= b

    word_to_id = {w: k for k, w in enumerate(all_words)}
    id_to_word = {k: w for k, w in enumerate(all_words)}

    # check ID creation
    for w in choices(list(all_words), k=5):
        assert id_to_word[word_to_id[w]] == w

    return word_to_id, id_to_word


# Sparse Matrix Coordinates and Values
def gen_coords(bags, word_to_id):
    # Some code to help you get started:
    m, n = len(word_to_id), len(bags)
    rows, cols, vals = [], [], []

    # Construct rows, cols, and vals:
    # rows = word ID
    # cols = sentence ID

    import numpy as np

    # essentially, this is the total count of each unique word in the entire document
    # num of sentence containing `i` word
    # iterate over each sentence/bag/document, then over each word
    ni = np.zeros(m)
    for sent in bags:
        for i in sent:
            # each word ID corresponds to the index of `ni`
            ni[word_to_id[i]] += 1

    for idx, sent in enumerate(bags):
        for w in sent:
            word_id = word_to_id[w]
            # word ID from dict
            rows.append(word_id)
            # sentence index
            cols.append(idx)
            # values
            a_ij = 1 / np.log((n + 1) / ni[word_id])
            vals.append(a_ij)

    # Returns your arrays:
    return rows, cols, vals


def get_svd_largest(A):
    from scipy.sparse.linalg import svds
    from numpy import abs
    u, s, v = svds(A, k=1, which='LM', return_singular_vectors=True)
    return s, abs(u.reshape(A.shape[0])), abs(v.reshape(A.shape[1]))


def rank_words(u0, v0):
    """
    Computes rank and returns the IDs of words in descending order
    of importance.
    """

    # NOTE:
    #    reshape Sigma and U to be a row vector (610,1)
    #    reshape V to be a column vector (1,110)

    # multiply Sigma and U, then DOT PROD with V.transpose
    rank = (sigma0 * u0).reshape(-1, 1).dot(v0.reshape(-1, 1).T)

    # sort rankings (largest to smallest)
    # `axis=0` sorts row-wise (rows are words)
    idx_rank = np.argsort(rank, axis=0)[::-1]

    # return ranked words
    return idx_rank[:, 0]


def rank_sentences(u0, v0):
    rank = (sigma0 * u0).reshape(-1, 1).dot(v0.reshape(-1, 1).T)

    # sort rankings (largest to smallest)
    # `axis=1` sorts column-wise (columns are sentence IDs)
    idx_rank = np.argsort(rank, axis=1)

    # return ranked words
    return idx_rank[0, :][::-1]


def get_matrix(bags, word_to_id):
    # create sparse matrix of words and sentences

    from scipy.sparse import csr_matrix

    rows, cols, vals = gen_coords(bags, word_to_id)

    return csr_matrix((vals, (rows, cols)), shape=(len(word_to_id), len(bags)))


def get_topn_words(u0, v0, n=10):
    # compute work rank
    word_ranking = rank_words(u0, v0)

    return [id_to_word[k] for k in word_ranking[:n]]


def get_topn_sentences(u0, v0, n=5):
    # compute sentence rank
    sentence_ranking = rank_sentences(u0, v0)
    raw_sents = get_sentences(raw_doc)
    return [raw_sents[k] for k in sentence_ranking[:n]]


if __name__ == '__main__':

    start_time = time.time()

    # provide filepath
    filepath = sys.argv[1]

    # read file
    raw_doc = read_doc(filepath)

    print('Document type:', type(raw_doc))
    print('Document length:', len(raw_doc))


    # get bag of words
    bags = gen_bag_of_words(get_sentences(raw_doc))

    # get word ids
    word_to_id, id_to_word = create_ids(bags)

    # compute SVD
    A = get_matrix(bags, word_to_id)
    sigma0, u0, v0 = get_svd_largest(A)

    print('-'*100)
    # compute work rank
    top_ten_words = get_topn_words(u0, v0, n=10)
    print("\nTop 10 words:\n", top_ten_words)
    print()

    # compute sentence rank
    top_five_sentences = get_topn_sentences(u0, v0, n=5)

    print("Top 5 sentences")
    print('-' * 100)
    for k, s in enumerate(top_five_sentences):
        print(f"\n{k}:", s)

    print('\n\nExecution time:', round(time.time() - start_time, 4), 'sec')
    print('-'*100)

