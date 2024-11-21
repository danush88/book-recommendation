import streamlit as st
import pandas as pd
import hashlib
import os

# Streamlit Page Configurations
st.set_page_config(page_title="Personalized Book Recommendation System", page_icon="📚", layout="wide")
st.title("📚 Curated Knowledge Book Recommendation System")

# Updated Dataset
data = {
    "title": [
        "Introduction to Algorithms", "Lean In", "The Great Gatsby",
        "To Kill a Mockingbird", "Sapiens", "Atomic Habits",
        "Clean Code", "Harry Potter", "The Pragmatic Programmer",
        "Educated", "1984", "Pride and Prejudice", "Deep Work",
        "The Power of Habit", "The Alchemist", "Thinking, Fast and Slow",
        "The Catcher in the Rye", "The Subtle Art of Not Giving a F*ck",
        "The Art of War", "Meditations", "The Lean Startup", 
        "Zero to One", "The Four Agreements", "The 7 Habits of Highly Effective People", 
        "How to Win Friends and Influence People", "The Road", 
        "Brave New World", "The Fellowship of the Ring", 
        "The Hobbit", "The Art of Computer Programming", 
        "Cracking the Coding Interview", "Hooked: How to Build Habit-Forming Products",
        "Becoming", "A Brief History of Time", "The Selfish Gene", 
        "Dune", "Foundation", "The Girl with the Dragon Tattoo", 
        "Gone Girl", "Man’s Search for Meaning"
    ],
    "author": [
        "Thomas H. Cormen", "Sheryl Sandberg", "F. Scott Fitzgerald",
        "Harper Lee", "Yuval Noah Harari", "James Clear",
        "Robert C. Martin", "J.K. Rowling", "Andrew Hunt",
        "Tara Westover", "George Orwell", "Jane Austen", "Cal Newport",
        "Charles Duhigg", "Paulo Coelho", "Daniel Kahneman",
        "J.D. Salinger", "Mark Manson", "Sun Tzu", "Marcus Aurelius", 
        "Eric Ries", "Peter Thiel", "Don Miguel Ruiz", 
        "Stephen R. Covey", "Dale Carnegie", "Cormac McCarthy", 
        "Aldous Huxley", "J.R.R. Tolkien", "J.R.R. Tolkien", 
        "Donald Knuth", "Gayle Laakmann McDowell", "Nir Eyal",
        "Michelle Obama", "Stephen Hawking", "Richard Dawkins", 
        "Frank Herbert", "Isaac Asimov", "Stieg Larsson", 
        "Gillian Flynn", "Viktor E. Frankl"
    ],
    "genre": [
        "Educational", "Self-Help", "Fiction",
        "Fiction", "Non-Fiction", "Self-Help",
        "Educational", "Fantasy", "Educational",
        "Biography", "Dystopian", "Romance", "Productivity",
        "Self-Help", "Fiction", "Psychology",
        "Fiction", "Self-Help", "Philosophy", "Philosophy", 
        "Business", "Business", "Self-Help", 
        "Self-Help", "Self-Help", "Fiction", 
        "Dystopian", "Fantasy", "Fantasy", 
        "Educational", "Educational", "Business",
        "Biography", "Science", "Science", 
        "Science Fiction", "Science Fiction", "Mystery", 
        "Mystery", "Psychology"
    ],
    "target_audience": [
        "Student", "Professional", "Casual Reader",
        "Casual Reader", "Student", "Professional",
        "Student", "Casual Reader", "Student",
        "Professional", "Casual Reader", "Casual Reader", "Professional",
        "Professional", "Casual Reader", "Student",
        "Casual Reader", "Professional", "Student", "Professional",
        "Professional", "Professional", "Casual Reader", 
        "Professional", "Professional", "Casual Reader", 
        "Casual Reader", "Casual Reader", "Casual Reader", 
        "Student", "Student", "Professional",
        "Casual Reader", "Student", "Student", 
        "Casual Reader", "Casual Reader", "Casual Reader", 
        "Casual Reader", "Professional"
    ]
}

book_df = pd.DataFrame(data)

# User Authentication Functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password, entered_password):
    return stored_password == hash_password(entered_password)

if 'user_authenticated' not in st.session_state:
    st.session_state.user_authenticated = False
    st.session_state.user_info = {}
    st.session_state.feedback_data = []

def login():
    st.session_state.user_authenticated = True

def logout():
    st.session_state.user_authenticated = False
    st.session_state.user_info = {}

# User Authentication
if not st.session_state.user_authenticated:
    st.sidebar.subheader("User Authentication")
    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Sign Up":
        email = st.sidebar.text_input("Enter your email")
        password = st.sidebar.text_input("Enter your password", type="password")
        role = st.sidebar.selectbox("Select your role", ["Student", "Professional", "Casual Reader"])
        if st.sidebar.button("Create Account"):
            st.session_state.user_info = {
                "email": email,
                "password": hash_password(password),
                "role": role
            }
            st.sidebar.success("Account created successfully!")
    elif choice == "Login":
        email = st.sidebar.text_input("Enter your email")
        password = st.sidebar.text_input("Enter your password", type="password")
        if st.sidebar.button("Login"):
            if verify_password(st.session_state.user_info.get("password", ""), password):
                login()
                st.sidebar.success(f"Welcome back {email}!")
            else:
                st.sidebar.error("Invalid email or password")
else:
    st.sidebar.success(f"Logged in as {st.session_state.user_info.get('email', 'User')}")
    if st.sidebar.button("Logout"):
        logout()

# User Preferences
st.sidebar.subheader("📋 Set Your Preferences")
favorite_genres = st.sidebar.multiselect("Select your favorite genres", book_df["genre"].unique())
preferred_authors = st.sidebar.text_input("Favorite authors (comma-separated)")

if st.sidebar.button("Save Preferences"):
    st.session_state.user_info["preferences"] = {
        "genres": favorite_genres,
        "authors": preferred_authors.split(",")
    }
    st.sidebar.success("Preferences saved!")

# Book Recommendation Function
def recommend_books(role, genres=None, authors=None):
    # Filter by role
    filtered_books = book_df[book_df["target_audience"] == role]

    # Filter by genres
    if genres:
        filtered_books = filtered_books[filtered_books["genre"].isin(genres)]

    # Filter by authors
    if authors:
        filtered_books = filtered_books[
            filtered_books["author"].str.contains('|'.join(authors), case=False, na=False)
        ]

    return filtered_books

# Book Recommendation Module
st.header("📖 Book Recommender System")
st.write("Get personalized book recommendations based on your role and preferences.")

if st.session_state.user_authenticated:
    user_role = st.session_state.user_info.get("role", "Casual Reader")
    user_preferences = st.session_state.user_info.get("preferences", {})
    genres = user_preferences.get("genres", [])
    authors = user_preferences.get("authors", [])

    recommendations = recommend_books(user_role, genres, authors)

    if not recommendations.empty:
        st.write("## Recommended Books")
        for _, book in recommendations.iterrows():
            st.markdown(f"### **{book['title']}**")
            st.write(f"- **Author:** {book['author']}")
            st.write(f"- **Genre:** {book['genre']}")
            st.markdown("---")
    else:
        st.write("No recommendations found based on your preferences.")
else:
    st.write("Please log in to view recommendations.")

# Feedback Module
st.header("💬 Book Feedback")
st.write("Share your thoughts on the books you've read!")

feedback_title = st.text_input("Enter the book title")
feedback_comment = st.text_area("Leave your feedback")
if st.button("Submit Feedback"):
    st.session_state.feedback_data.append({"title": feedback_title, "comment": feedback_comment})
    st.success("Thank you for your feedback!")

# Display Feedback
if st.session_state.feedback_data:
    st.write("## Feedback from Users")
    for feedback in st.session_state.feedback_data:
        st.markdown(f"**Book Title:** {feedback['title']}")
        st.markdown(f"**Feedback:** {feedback['comment']}")
        st.markdown("---")

# Book Rating and Review Module
st.subheader("⭐ Book Rating and Review")
selected_book = st.selectbox("Select a book to rate and review", book_df['title'])
rating = st.slider("Rate this book", 1, 5)
review = st.text_area("Write your review")
if st.button("Submit Review"):
    st.success(f"Thank you for reviewing **{selected_book}**!")
    st.write(f"Your rating: {rating}")
    st.write(f"Your review: {review}")
    # Placeholder for saving review in a database.

# Bookshelf Management Module
st.subheader("📚 My Bookshelf")
if 'bookshelf' not in st.session_state:
    st.session_state.bookshelf = []

add_to_shelf = st.selectbox("Add a book to your bookshelf", book_df['title'])
if st.button("Add to Bookshelf"):
    if add_to_shelf not in st.session_state.bookshelf:
        st.session_state.bookshelf.append(add_to_shelf)
        st.success(f"Added **{add_to_shelf}** to your bookshelf!")
    else:
        st.warning("This book is already in your bookshelf.")

st.write("### Your Bookshelf:")
if st.session_state.bookshelf:
    for book in st.session_state.bookshelf:
        st.write(f"- {book}")
else:
    st.write("Your bookshelf is empty.")

# Reading History Module
st.subheader("📖 Reading History")
if 'reading_history' not in st.session_state:
    st.session_state.reading_history = []

read_book = st.selectbox("Mark a book as read", book_df['title'])
if st.button("Mark as Read"):
    if read_book not in st.session_state.reading_history:
        st.session_state.reading_history.append(read_book)
        st.success(f"Marked **{read_book}** as read!")
    else:
        st.warning("This book is already in your reading history.")

st.write("### Your Reading History:")
if st.session_state.reading_history:
    for book in st.session_state.reading_history:
        st.write(f"- {book}")
else:
    st.write("You have no reading history yet.")

# File Sharing Module
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.subheader("📤 File Sharing")
uploaded_file = st.file_uploader("Upload a file to share with others", type=["pdf", "txt", "epub"])
if uploaded_file:
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Successfully uploaded **{uploaded_file.name}**!")
    st.write(f"📂 [Download {uploaded_file.name}](./{file_path})")

st.markdown("---")
st.write("Thank you for using the Personalized Book Recommendation System!")
