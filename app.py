import streamlit as st
import pickle
import requests
import streamlit.components.v1 as components

# Load data
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values
# selectvalue=st.selectbox("Select movie from dropdown", movies_list)



# Streamlit setup

OMDB_API_KEY = "e6050982"

def fetch_poster(movie_title):
    """
    Fetch the movie poster from the OMDb API using the movie title.
    """
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check for HTTP request errors
        data = response.json()
        if data.get("Response") == "True":
            return data.get("Poster", "No poster available")
        else:
            return "No poster available"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
        return "Error fetching poster"

st.header("Movie Recommendation System")
# selectvalue = st.selectbox("Select movie from dropdown", movies_list)


imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/frontend/public")
imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154)
   
    ]

imageCarouselComponent(imageUrls=imageUrls, height=200)
selectvalue=st.selectbox("Select movie from dropdown", movies_list)


# OMDb API Key (replace with your actual key)

def recommend(movie):
    """
    Recommend 5 similar movies based on the similarity matrix.
    """
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommendations = []
    recommend_poster = []
    for i in distances[1:6]:  # Skip the first one because it's the same movie
        movie_title = movies.iloc[i[0]]['title']
        recommendations.append(movie_title)
        recommend_poster.append(fetch_poster(movie_title))
    return recommendations, recommend_poster

if st.button("Show Recommended"):
    movie_name, movie_poster = recommend(selectvalue)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
