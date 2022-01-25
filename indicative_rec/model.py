import logging
import numpy as np

from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize

logging.basicConfig(filename='liba.log', filemode='w', format='%(asctime)s - %(message)s')


def create_csr_matrix(matrix, users, items):
    n_users = users.max() + 1
    n_items = items.max() + 1

    matrix_shape = (n_users, n_items)
    data = np.ones(items.shape)
    # разряженная матрица взаимодейсвий пользователей и книг
    user_item_matrix = csr_matrix((data, (users, items)), shape=matrix_shape)
    return user_item_matrix


def csr_row_set_nz_to_val(csr, row, value=0):
    if not isinstance(csr, csr_matrix):
        raise ValueError('Matrix given must be of CSR format.')
    csr.data[csr.indptr[row]:csr.indptr[row + 1]] = value


def normalization_matrix(user_item_matrix):
    reader_normalized_matrix = normalize(user_item_matrix, axis=1, norm='l1')
    book_normalized_matrix = normalize(user_item_matrix, axis=0, norm='l1')

    # readers with less than 2 books are useless for recommendation
    lazy_readers = np.array(user_item_matrix.sum(axis=1)).squeeze()
    lazy_readers = np.where(lazy_readers < 2)[0]

    # remove them from calculation of similar readers
    for rId in lazy_readers:
        csr_row_set_nz_to_val(reader_normalized_matrix, rId)

    return reader_normalized_matrix


def user_item_df(df):
    """
        add category to dataframe
    """
    df.id = df.id.astype('category')
    df.id_book = df.id_book.astype('category')
    return df


def add_category(user_item):
    user_item.id = user_item.id.astype('category')
    user_item.id_book = user_item.id_book.astype('category')
    # добавляем столбцы с номерами категорий книг и пользователей
    user_item['category_id'] = user_item.id.cat.codes
    user_item['category_book'] = user_item.id_book.cat.codes
    return user_item


def similar_lightfm(model, book_id, n: int = 5):
    book_embeddings = (model.item_embeddings.T
                      / np.linalg.norm(model.item_embeddings, axis=1)).T

    query_embedding = book_embeddings[book_id]
    similarity = np.dot(book_embeddings, query_embedding)
    most_similar = np.argsort(-similarity)[1:n+1]
    return most_similar


class Models:
    def __init__(self, model_file, df, model_type):
        self.model_file = model_file
        self.df = add_category(df)
        self.model_type = model_type
        self.items = None
        self.users = None

    def normalize_matrix(self, verbose=False):
        # получение датафреймов с пользователями и книгами
        user_item_matrix = user_item_df(self.df)

        # кодируем пользователей и книги
        self.users = user_item_matrix.id.cat.codes
        self.items = user_item_matrix.id_book.cat.codes

        csr_matrix = create_csr_matrix(user_item_matrix, self.users, self.items)
        normalization_df = normalization_matrix(csr_matrix)

        return normalization_df

    def predict(self, user_id, n: int = 5):
        logging.info(f'Create rec for user: {user_id}')

        user_id = self.df[self.df.id == user_id]['category_id'].values[0]

        normalization = self.normalize_matrix()

        logging.info('Normalize data')

        if self.model_type == 0:
            n_items = self.items.max() + 1
            indexs = self.model_file.predict(int(user), np.arange(n_items)).argsort()[::-1]
            already_read = self.df[(self.df.category_id == int(user)) & (
                self.df.category_book.isin(indexs))]['category_book'].tolist()
            for ar in already_read:
                indexs = indexs[indexs != ar]

            indexs = indexs[:n]
            recommend_books = self.df[self.df.category_book.isin(indexs)]['id_book'].unique().tolist()

            return recommend_books

        elif self.model_type == 1:
            indexs = [index for index, score_ in self.model_file.recommend(int(user_id), normalization)][:n]
            recommend_books = self.df[self.df.category_book.isin(indexs)]['id_book'].unique().tolist()
            return recommend_books
        elif self.model_type == 2:
            '''в разработке'''
            pass
        else:
            logging.info('Model isnt selected')

    def similar(self, book_id, n: int = 5):
        logging.info(f'Find similar for {book_id}')

        book_id = self.df[self.df.id_book == book_id]['category_book'].values[0]

        if self.model_type == 0:
            indexs = [int(ind) for ind in similar_lightfm(model=self.model_file, book_id=book_id)]
            similar_books = self.df[self.df.category_book.isin(indexs)]['id_book'].unique().tolist()
            return similar_books
        elif self.model_type == 1:
            indexs = [int(ind) for ind, _ in self.model_file.similar_items(book_id)[1:]]
            similar_books = self.df[self.df.category_book.isin(indexs)]['id_book'].unique().tolist()
            return similar_books
        else:
            logging.info("Model isnt selected")


if __name__ == '__main__':
    pass
