import streamlit as st
import pickle
import pandas as pd
import numpy as np

# -----------------------------
# Load data
# -----------------------------
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Book Recommender", page_icon="📚", layout="wide")

# Custom CSS for style (same look as video)
st.markdown("""
    <style>
    .main {
        background-color: #F5F5F5;
    }
    .stButton>button {
        background-color: #007BFF;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("📚 Navigation")
menu = ["🏆 Popular Books", "🔍 Recommend Books"]
choice = st.sidebar.radio("Go to:", menu)

# -----------------------------
# 1️⃣ Popular Books Section
# -----------------------------
if choice == "🏆 Popular Books":
    st.title("🔥 Top 50 Popular Books")

    for i in range(0, len(popular_df), 5):
        cols = st.columns(5)
        for j, col in enumerate(cols):
            if i + j < len(popular_df):
                book = popular_df.iloc[i + j]
                with col:
                    st.image(book["Image-URL-M"], width=130)
                    st.markdown(f"{book['Book-Title']}")
                    st.caption(book["Book-Author"])
                    st.write(f"⭐ {book['avg_rating']:.2f}")
                    st.write(f"👥 {book['num_ratings']} ratings")

# -----------------------------
# 2️⃣ Recommend Books Section
# -----------------------------
elif choice == "🔍 Recommend Books":
    st.title("🔍 Book Recommendation System")

    selected_book = st.selectbox("Select a Book You Like:", pt.index)

    if st.button("📖 Recommend Similar Books"):
        index = np.where(pt.index == selected_book)[0][0]
        distances = similarity_scores[index]
        similar_items = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]

        st.subheader("📚 You Might Also Like:")

        cols = st.columns(5)
        for idx, col in enumerate(cols):
            book_title = pt.index[similar_items[idx][0]]
            temp_df = books[books["Book-Title"] == book_title]
            image_url = temp_df["Image-URL-M"].values[0]
            author = temp_df["Book-Author"].values[0]

            with col:
                st.image(image_url, width=130)
                st.markdown(f"{book_title}")
                st.caption(author)



