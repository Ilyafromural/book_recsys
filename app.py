import pickle
import streamlit as st
import numpy as np


st.set_page_config(page_title='Books Recommendation app', layout="wide")

# Устанавливаем картинку на задний фон
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://img.freepik.com/free-photo/close-up-arrangement-with-books_23-2148255899.jpg?w=740&t=st=1706426470~exp=1706427070~hmac=fa288e9a1f98a7a89e790ebcb1b563a4845b50dabba7694a55b8b138ebcaae87");
background-size: 100%;
background-position: bottom;
background-repeat: no-repeat;
background-attachment: local;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Заголовок приложения:
st.header('Books Recommendation app', divider='orange')

# Загружаем модель и необходимые данные
model = pickle.load(open('pickles/model.pkl', 'rb'))  # модель
book_names = pickle.load(open('pickles/book_names.pkl', 'rb'))  # список книг
final_rating = pickle.load(open('pickles/final_rating.pkl', 'rb'))  # рейтинг книг
book_pivot = pickle.load(open('pickles/book_pivot.pkl', 'rb'))  # сводная таблица по книгам


# Функция для загрузки ссылок на страницы с обложками книг
def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    posters_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]: 
        ids = np.where(final_rating['title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_rating.iloc[idx]['image_url']
        posters_url.append(url)

    return posters_url


# Функция для получения рекомендаций
def recommend_book(book_name):
    books_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(
        book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6
    )

    poster_url = fetch_poster(suggestion)
    
    for i in range(len(suggestion)):
        books = book_pivot.index[suggestion[i]]
        for j in books:
            books_list.append(j)
    return books_list, poster_url

# Это кнопка выпадающего списка
selected_books = st.selectbox(
    "Type or select a book from the dropdown",
    book_names
)

# Это кнопка "Показать рекомендации"
if st.button('Show Recommendation'):
    recommended_books, poster_url = recommend_book(selected_books)
    col1, col2, col3, col4, col5 = st.columns(5, gap='small')

    with col1:
        st.text(recommended_books[1])
        st.image(poster_url[1])

    with col2:
        st.text(recommended_books[2])
        st.image(poster_url[2])

    with col3:
        st.text(recommended_books[3])
        st.image(poster_url[3])

    with col4:
        st.text(recommended_books[4])
        st.image(poster_url[4])

    with col5:
        st.text(recommended_books[5])
        st.image(poster_url[5])
