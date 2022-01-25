import logging
import pandas as pd


def get_history_user(user_id: int, df, all_books):
    guide = pd.merge(df[df.id == user_id], all_books,
                     left_on='id_book', right_on='id_book',
                     how='inner').drop_duplicates()['id_book']

    history_ids = guide.unique().tolist()
    return history_ids


def get_name_book(book_id, all_books):
    name_books = all_books[(all_books.name_book != '') & (all_books.id_book == book_id)]['name_book']
    if name_books.shape[0] > 1:
        logging.info(f'More than one name for {book_id} book')
        return name_books.head(1).values[0]
    if name_books.shape[0] == 1:
        return name_books.values[0]
    return None


def get_similar_name_book(book_id, df, all_books):
    temp_series = pd.merge(df[df.id_book == book_id],
                       all_books,
                       left_on='id_book',
                       right_on='id_book',
                       how='inner')['name_book'].unique()
    if temp_series.shape[0] > 1:
        temp_series = temp_series[temp_series != '']
        return temp_series[0]

    elif temp_series.shape[0] == 1:
        return temp_series[0]
    return None
