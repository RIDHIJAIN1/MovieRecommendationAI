import pandas as pd;
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle;


movies = pd.read_csv('datasett.csv') 

# print("Dataset Head:")
# print(movies.head())

# print("Dataset Columns:")
# print(movies.columns)
movies = movies[['id', 'title', 'overview', 'genre']]
# Create 'tags' by concatenating 'overview' and 'genre'
movies['tags'] = movies['overview'] + " " + movies['genre']

# Drop 'overview' and 'genre' columns
new_data = movies.drop(columns=['overview', 'genre'])
# print("New Data Head:")
# print(new_data.head())
cv = CountVectorizer(max_features=10000, stop_words='english')

# Fit and transform the 'tags' column
vectorized_data = cv.fit_transform(new_data['tags'].values.astype('U')).toarray()
print("Vectorized Data Shape:", vectorized_data.shape)

similarity = cosine_similarity(vectorized_data)
# print("similarity" , similarity)

mydata =new_data[new_data['title']== "The Godfather"].index[0]
print("My data " , mydata)

# distance = sorted(list(enumerate(similarity[2])),reverse=True, key=lambda vector:vector[1])
# for i in distance[0:5]:
#     print(new_data.iloc[i[0]].title)

def recommend(movie_title):
    index = new_data[new_data['title'] == movie_title].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommendations = []
    for i in distances[1:6]:  # Skip the first one because it's the same movie
        recommendations.append(new_data.iloc[i[0]]['title'])
    return recommendations

# Get and print recommendations
godfather_recommendations = recommend("The Godfather")
ironman_recommendations = recommend("Iron Man")

print("Recommendations for 'The Godfather':")
for movie in godfather_recommendations:
    print(movie)

print("\nRecommendations for 'Iron Man':")
for movie in ironman_recommendations:
    print(movie)

    pickle.dump(new_data , open('movies_list.pkl', 'wb'))
    pickle.dump(similarity , open('similarity.pkl', 'wb'))
    mydata =pickle.load( open('movies_list.pkl', 'rb'))
    print("myyyyyy" , mydata)