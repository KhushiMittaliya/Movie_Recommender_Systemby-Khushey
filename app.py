from flask import Flask, request, render_template
import pickle
import pandas as pd

app = Flask(__name__)

# Load movie data
movies_dict = pd.read_csv('movies.csv')
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Reset index if needed
movies_dict = movies_dict.reset_index(drop=True)

def recommend(movie):
    movie = movie.lower()
    if movie not in movies_dict['title'].str.lower().values:
        return ["Movie not found. Please try another."]

    idx = movies_dict[movies_dict['title'].str.lower() == movie].index[0]
    distances = list(enumerate(similarity[idx]))
    movies_list = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]
    return [movies_dict.iloc[i[0]].title for i in movies_list]

@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = []
    if request.method == 'POST':
        movie_name = request.form['movie']
        recommendations = recommend(movie_name)
    return render_template('index.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
