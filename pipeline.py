import pickle
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import time


def main():

    # Загружаем данные
    print("Loading data...")
    time.sleep(2)
    books = pd.read_csv(
        filepath_or_buffer='data/BX-Books.csv', sep=";", on_bad_lines='skip', encoding='latin-1',
        usecols=['ISBN', 'Book-Title', 'Image-URL-L']
    )
    ratings = pd.read_csv(
        filepath_or_buffer='data/BX-Book-Ratings.csv', sep=";", on_bad_lines='skip', encoding='latin-1'
    )
    # Переименовываем некоторые столбцы для удобства
    books.rename(columns={"Book-Title": 'title',
                          "Image-URL-L": "image_url"}, inplace=True)

    ratings.rename(columns={"User-ID": 'user_id',
                            'Book-Rating': 'rating'}, inplace=True)

    # Проводим необходимую трансформацию данных, а также выборку для дальнейшего обучения модели
    # Трансформация данных:
    print("Transforming data...")
    time.sleep(2)

    # Сначала отбираем пользователей, которые оценили более 200 книг
    users_200 = ratings['user_id'].value_counts() > 200
    users_200_index = users_200[users_200].index
    ratings = ratings[ratings['user_id'].isin(users_200_index)]
    # Смерджим получившийся датафрейм с датафреймом книг
    ratings_with_books = ratings.merge(books, on='ISBN')
    # Посчитаем сколько раз оценивалась каждая книга
    count_rating = ratings_with_books.groupby('title')['rating'].count().reset_index()
    # Переименуем колонку 'rating' для исключения ошибки при слиянии двух таблиц
    count_rating.rename(columns={'rating': 'num_of_ratings'}, inplace=True)
    # Теперь смерджим получившийся датафрейм с датафреймом книг
    final_rating = ratings_with_books.merge(count_rating, on='title')
    # Возьмем только те книги, которые оценивались хотя бы 50 раз
    final_rating = final_rating[final_rating['num_of_ratings'] >= 50]
    # Удалим дубликаты
    final_rating.drop_duplicates(['user_id', 'title'], inplace=True)
    # Создаем сводную таблицу
    book_pivot = final_rating.pivot_table(columns='user_id', index='title', values='rating')
    # Заполняем пустые значения нулями и изменим тип данных в датасете
    book_pivot.fillna(value=0, inplace=True)
    book_pivot = book_pivot.astype(dtype='int16', copy=True)
    # Для обучения модели сохраним данные в формате numpy array
    book_numpy = book_pivot.to_numpy()

    # Создаем общий список книг:
    book_names = book_pivot.index

    # Объявление модели
    model = NearestNeighbors(algorithm='brute')

    # Обучение модели:
    print("Training model...")
    time.sleep(2)
    model.fit(book_numpy)

    # Запись модели и данных в файлы
    print("Saving model and data in files...")
    time.sleep(2)
    pickle.dump(model, open('./pickles/model.pkl', 'wb'))
    pickle.dump(book_names, open('./pickles/book_names.pkl', 'wb'))
    pickle.dump(final_rating, open('./pickles/final_rating.pkl', 'wb'))
    pickle.dump(book_pivot, open('./pickles/book_pivot.pkl', 'wb'))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
