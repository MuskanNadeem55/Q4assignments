import streamlit as st
import json
import os

FILE_PATH = os.path.join(os.getcwd(), "library.json")

def load_library():
    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_library(data):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)

if "library" not in st.session_state:
    st.session_state.library = load_library()

def add_book(title, author, year, genre, read):
    book = {"title": title, "author": author, "year": year, "genre": genre, "read": read}
    st.session_state.library.append(book)
    save_library(st.session_state.library)
    st.success("✅ Book added successfully!")

def remove_book(title):
    st.session_state.library = [book for book in st.session_state.library if book['title'].lower() != title.lower()]
    save_library(st.session_state.library)
    st.success("🗑️ Book removed successfully!")

def toggle_read_status(title):
    for book in st.session_state.library:
        if book['title'].lower() == title.lower():
            book['read'] = not book['read']
            st.success(f"🔁 Marked as {'Read' if book['read'] else 'Unread'}")
            break
    save_library(st.session_state.library)

def search_books(keyword, by='title'):
    return [book for book in st.session_state.library if keyword.lower() in book[by].lower()]

def filter_books_by_genre(genre):
    return [book for book in st.session_state.library if book['genre'].lower() == genre.lower()]

def display_statistics():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book['read'])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    return total_books, percentage_read

# --- Custom Styles ---
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
            font-size: 17px;
            background: linear-gradient(to right, #e0f7fa, #fff3e0);
            color: #212121;
        }
        .stButton>button {
            background: linear-gradient(to right, #1a2980, #26d0ce);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
        }
        .stButton>button:hover {
            background: linear-gradient(to right, #26d0ce, #1a2980);
        }
        .book-card {
            background-color: white;
            border-left: 6px solid #42a5f5;
            padding: 14px;
            border-radius: 10px;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
            margin: 10px 0;
        }
        .genre-tag {
            display: inline-block;
            padding: 2px 10px;
            font-size: 0.8em;
            border-radius: 10px;
            background-color: #ffe082;
            color: #424242;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📚 Personal Library Manager")

menu = [
    "Add a Book", 
    "Remove a Book", 
    "Search for a Book", 
    "Display All Books", 
    "Display Statistics",
    "Mark Book as Read/Unread",
    "Filter by Genre"
]
choice = st.sidebar.selectbox("📌 Menu", menu)

if choice == "Add a Book":
    st.subheader("📘 Add a New Book")
    title = st.text_input("📖 Title")
    author = st.text_input("✍️ Author")
    year = st.number_input("📅 Publication Year", min_value=0, max_value=2100, value=2024)
    genre = st.selectbox("📂 Genre", ["Fiction", "Non-fiction", "Mystery", "Fantasy", "Science Fiction", "Biography", "History", "Self-help", "Other"])
    read = st.checkbox("✅ Have you read this book?")
    if st.button("➕ Add Book"):
        if title and author:
            add_book(title, author, year, genre, read)
        else:
            st.error("❌ Title and Author are required!")

elif choice == "Remove a Book":
    st.subheader("🗑️ Remove a Book")
    title = st.text_input("Enter the title of the book to remove")
    if st.button("❌ Remove Book"):
        if title:
            remove_book(title)
        else:
            st.warning("⚠️ Please enter a book title.")

elif choice == "Search for a Book":
    st.subheader("🔍 Search for a Book")
    search_by = st.radio("Search by", ["title", "author"])
    keyword = st.text_input("Enter your search keyword")
    if st.button("🔎 Search"):
        results = search_books(keyword, search_by)
        if results:
            for book in results:
                st.markdown(f"""
                <div class='book-card'>
                    <strong>📖 {book['title']}</strong> <br>
                    ✍️ {book['author']} ({book['year']})<br>
                    <span class='genre-tag'>{book['genre']}</span> — {'✅ Read' if book['read'] else '📌 Unread'}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No matching books found.")

elif choice == "Display All Books":
    st.subheader("📚 Your Library")
    if st.session_state.library:
        for book in st.session_state.library:
            st.markdown(f"""
            <div class='book-card'>
                <strong>📖 {book['title']}</strong> <br>
                ✍️ {book['author']} ({book['year']})<br>
                <span class='genre-tag'>{book['genre']}</span> — {'✅ Read' if book['read'] else '📌 Unread'}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 Your library is empty!")

elif choice == "Display Statistics":
    st.subheader("📊 Library Statistics")
    total_books, percentage_read = display_statistics()
    st.write(f"📚 *Total Books:* {total_books}")
    st.progress(percentage_read / 100)
    st.write(f"✅ *Percentage Read:* {percentage_read:.2f}%")

elif choice == "Mark Book as Read/Unread":
    st.subheader("🔁 Update Book Read Status")
    title = st.text_input("Enter the title of the book to toggle status")
    if st.button("🔄 Toggle Read/Unread"):
        if title:
            toggle_read_status(title)
        else:
            st.warning("⚠️ Please enter a book title.")

elif choice == "Filter by Genre":
    st.subheader("🔍 Filter Books by Genre")
    genre = st.selectbox("Choose Genre", sorted(set([book['genre'] for book in st.session_state.library])))
    filtered_books = filter_books_by_genre(genre)
    if filtered_books:
        for book in filtered_books:
            st.markdown(f"""
            <div class='book-card'>
                <strong>📖 {book['title']}</strong> <br>
                ✍️ {book['author']} ({book['year']})<br>
                <span class='genre-tag'>{book['genre']}</span> — {'✅ Read' if book['read'] else '📌 Unread'}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 No books found for this genre.")

if st.sidebar.button("🔄 Reset Library Data"):
    st.session_state.library = []
    save_library([])
    st.warning("⚠️ Library data reset!")

st.markdown("---")

