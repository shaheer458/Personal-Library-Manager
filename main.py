import json
import streamlit as st

# Streamlit app title
st.title("📖 Personal Library Manager")

# Initialize session state for library
if 'library' not in st.session_state:
    st.session_state.library = []

# Function to add a book
def add_book():
    with st.form("Add Book"):
        title = st.text_input("Enter the Title of Book")
        author = st.text_input("Enter the Author Name")
        year = st.text_input("Enter the Year of Publication")
        genre = st.text_input("Enter the Genre")
        read_status = st.selectbox("Have you read it?", ["yes", "no"])
        submitted = st.form_submit_button("Add Book")

        if submitted:
            book = {
                "Title": title,
                "Author": author,
                "Year": year,
                "Genre": genre,
                "Read": read_status.lower() == "yes"
            }
            st.session_state.library.append(book)
            st.success(f"Book '{title}' added successfully!")

# Function to remove a book
def remove_book():
    titles = [book["Title"] for book in st.session_state.library]
    title = st.selectbox("Select a book to remove", titles)
    if st.button("Remove Book"):
        st.session_state.library = [book for book in st.session_state.library if book["Title"] != title]
        st.success(f"Book '{title}' removed successfully!")

# Function to search for a book
def search_book():
    query = st.text_input("Enter a keyword to search (title, author, genre):")
    if query:
        results = [book for book in st.session_state.library if 
                   query.lower() in book["Title"].lower() or 
                   query.lower() in book["Author"].lower() or 
                   query.lower() in book["Genre"].lower()]
        if results:
            st.subheader("Search Results")
            for book in results:
                st.write(f"- {book['Title']} by {book['Author']} ({book['Year']} - {book['Genre']}) [Read: {'Yes' if book['Read'] else 'No'}]")
        else:
            st.warning("Book not found.")

# Function to display all books
def display_books():
    if not st.session_state.library:
        st.info("No books in the library.")
    else:
        st.subheader("Books in Your Library")
        for book in st.session_state.library:
            st.write(f"- {book['Title']} by {book['Author']} ({book['Year']} - {book['Genre']}) [Read: {'Yes' if book['Read'] else 'No'}]")

# Function to show statistics
def show_statistics():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book["Read"])
    genres = {book["Genre"] for book in st.session_state.library}

    st.subheader("📊 Library Statistics")
    st.write(f"Total books: {total_books}")
    st.write(f"Books read: {read_books}")
    st.write(f"Unique Genres: {', '.join(genres) if genres else 'None'}")

# Function to save library to file
def save_library():
    filename = st.text_input("Enter filename to save (e.g., library.json):")
    if st.button("Save Library"):
        with open(filename, "w") as file:
            json.dump(st.session_state.library, file, indent=4)
        st.success(f"Library saved to '{filename}' successfully!")

# Function to load library from file
def load_library():
    filename = st.text_input("Enter filename to load (e.g., library.json):")
    if st.button("Load Library"):
        try:
            with open(filename, "r") as file:
                st.session_state.library = json.load(file)
            st.success(f"Library loaded from '{filename}' successfully!")
        except FileNotFoundError:
            st.error(f"File '{filename}' not found.")

# Sidebar menu
menu = st.sidebar.selectbox("Menu", [
    "Add a Book", "Remove a Book", "Search for a Book",
    "Display ALL Books", "Show Statistics",
    "Save Library to File", "Load Library from File"
])

# Display selected functionality
if menu == "Add a Book":
    add_book()
elif menu == "Remove a Book":
    remove_book()
elif menu == "Search for a Book":
    search_book()
elif menu == "Display ALL Books":
    display_books()
elif menu == "Show Statistics":
    show_statistics()
elif menu == "Save Library to File":
    save_library()
elif menu == "Load Library from File":
    load_library()
