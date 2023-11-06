import pandas as pd
import numpy as np
import nltk
import re
import string
from flask import Flask, request, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)


# Load datasets
movies = pd.read_csv('../data/movies.csv')
movies.rename(columns=lambda x: x.strip().lower(), inplace=True)

# slice off unused columns
movies = movies[['movie name', 'detail about movie',
                 'year', 'runtime', 'ranking of movie',
                 'genre', 'rating', 'votes', 'director',
                 'actor 1', 'actor 2', 'actor 3', 'actor 4']]

# rename columns
movies = movies.rename(columns={'movie name': 'title',
                                'detail about movie': 'description',
                                'ranking of movie': 'ranking',
                                'actor 1': 'actor-1',
                                'actor 2': 'actor-2',
                                'actor 3': 'actor-3',
                                'actor 4': 'actor-4'})

movies.fillna('', inplace=True)
movie_corpus_columns = ['title', 'director', 'actor-1', 'actor-2', 'actor-3', 'actor-4', 'description']
movies['corpus'] = movies[movie_corpus_columns].apply(lambda x: ' '.join(x), axis=1)

#
#
#
tv_series = pd.read_csv('../data/tv-series.csv')
tv_series.rename(columns=lambda x: x.strip().lower(), inplace=True)

tv_series = tv_series[['series name', 'details', 'year',
                       'runtime', 'ranking',
                       'genre', 'rating', 'votes', 'actor 1',
                       'actor 2', 'actor 3', 'actor 4']]

tv_series = tv_series.rename(columns={
                              'series name': 'title',
                              'details': 'description',
                              'actor 1': 'actor-1',
                              'actor 2': 'actor-2',
                              'actor 3': 'actor-3',
                              'actor 4': 'actor-4'})

tv_series.fillna('', inplace=True)

tv_series_corpus_columns = ['title', 'actor-1', 'actor-2', 'actor-3', 'actor-4', 'description']
tv_series['corpus'] = tv_series[tv_series_corpus_columns].apply(lambda x: ' '.join(x), axis=1)

#
#
#
video_games = pd.read_csv('../data/video-games.csv')
video_games.rename(columns=lambda x: x.strip().lower(), inplace=True)

video_games = video_games[['video game name', 'details', 'year',
                           'ranking', 'genre', 'rating', 'votes',
                           'director', 'actor-1', 'actor-2', 
                           'actor-3', 'actor-4']]

video_games = video_games.rename(columns={'video game name': 'title',
                                          'details': 'description'})

video_games.fillna('', inplace=True)

video_games_corpus_columns = ['title', 'director', 'actor-1', 'actor-2', 'actor-3', 'actor-4', 'description']
video_games['corpus'] = video_games[video_games_corpus_columns].apply(lambda x: ' '.join(x), axis=1)

print(movies.columns)
print(tv_series.columns)
print(video_games.columns)

raise NotImplementedError
#
#
#

nltk.download('wordnet')

# prepare to tokenize words
wpt = nltk.WordPunctTokenizer()

# download stopwords
nltk.download('stopwords')
stop_words = nltk.corpus.stopwords.words('english')


# create function to normalize corpus
def process(txt):
    # lower case and remove special characters/whitespaces
    txt = re.sub(r'[^a-zA-Z0-9\s]', '', str(txt), re.I | re.A)
    txt = txt.lower()
    txt = txt.strip()

    # tokenize
    tokens = wpt.tokenize(txt)

    # filter stopwords
    filtered_tokens = [
        token for token in tokens if token not in stop_words
        and token not in list(string.punctuation)]

    # re-create and join
    txt = " ".join(filtered_tokens)

    return txt


normalize_corpus = np.vectorize(process)

movie_corpus = normalize_corpus(new_movies)
movie_corpus = pd.DataFrame(movie_corpus)
movie_corpus.columns = ['title', 'description', 'year', 'runtime', 'ranking',
                        'genre', 'rating', 'votes', 'director', 'Actor 1',
                        'Actor 2', 'ACTOR 3', 'ACTOR 4']


series_corpus = normalize_corpus(new_series)
series_corpus = pd.DataFrame(series_corpus)
series_corpus.columns = ['title', 'description', 'year', 'runtime', 'ranking',
                         'genre', 'rating', 'votes', 'ACTOR 1', 'ACTOR 2',
                         'ACTOR 3', 'ACTOR 4']


games_corpus = normalize_corpus(new_games)
games_corpus = pd.DataFrame(games_corpus)
games_corpus.columns = ['title', 'description', 'year', 'ranking', 'genre',
                        'rating', 'votes',  'DIRECTOR ', 'ACTOR-1', 'ACTOR-2',
                        'ACTOR-3', 'ACTOR-4']

#
#
#

# Define TF-IDF vectorizers for each dataset
tfidf_vec_movies = TfidfVectorizer()
movies_tfidf_matrix = tfidf_vec_movies.fit_transform(
    movie_corpus['description'])

tfidf_vec_series = TfidfVectorizer()
series_tfidf_matrix = tfidf_vec_series.fit_transform(
    series_corpus['description'])

tfidf_vec_games = TfidfVectorizer()
games_tfidf_matrix = tfidf_vec_games.fit_transform(
    games_corpus['description'])

#
#
#


@app.route('/')
def index():
    return render_template('index.html')


def calculate_cosine_similarity(user_input, item_matrix, vectorizer):
    # Transform the user input
    user_input_vector = vectorizer.transform([user_input])

    # Calculate cosine similarity
    cosine_similarities = cosine_similarity(user_input_vector, item_matrix)

    return cosine_similarities


@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    genre = request.form.get('genre')
    ranking = request.form.get('ranking')
    runtime = request.form.get('runtime')
    year = request.form.get('year')
    rating = request.form.get('rating')
    num_votes = request.form.get('num_votes')
    num_recommendations = request.form.get('num_recommendations')

    recommendations = []

    if user_input is not None:
        user_input = user_input.lower()

    # Handle optional input fields
    if not ranking:
        ranking = np.nan
    else:
        ranking = float(ranking)

    if not runtime:
        runtime = np.nan
    else:
        runtime = float(runtime)

    if not year:
        year = np.nan 
    else:
        year = int(year)

    if not rating:
        rating = np.nan 
    else:
        rating = float(rating)

    if not num_votes:
        num_votes = np.nan
    else:
        num_votes = int(num_votes)

    if not num_recommendations:
        num_recommendations = 10
    else:
        num_recommendations = int(num_recommendations)

    # Create dataframes for the selected genre
    if genre == 'Movies':
        item_df = new_movies
        item_matrix = movies_tfidf_matrix
        vectorizer = tfidf_vec_movies
    elif genre == 'TV Series':
        item_df = new_series
        item_matrix = series_tfidf_matrix
        vectorizer = tfidf_vec_series
    elif genre == 'Video Games':
        item_df = new_games
        item_matrix = games_tfidf_matrix
        vectorizer = tfidf_vec_games

    if user_input is not None:
        # Calculate cosine similarity
        cosine_similarities = calculate_cosine_similarity(
            user_input, item_matrix, vectorizer)

        # Get the indices of the top recommendations
        similar_indices = cosine_similarities[0].argsort()[
            :-num_recommendations-1:-1]

        # Convert to float
        item_df['ranking'] = pd.to_numeric(
            item_df['ranking'], errors='coerce')

        item_df['runtime'] = pd.to_numeric(
            item_df['runtime'], errors='coerce')

        item_df['votes'] = pd.to_numeric(
            item_df['votes'], errors='coerce')


    # Filter the data based on user preferences and remove rows with NaN values
    if not (np.isnan(ranking) or np.isnan(year) or np.isnan(rating)
            or np.isnan(runtime) or np.isnan(num_votes)):
        
        filtered_df = item_df[
            (item_df['ranking'] >= ranking) &
            (item_df['runtime'] <= runtime) &
            (item_df['year'] == year) &
            (item_df['rating'] >= rating) &
            (item_df['votes'] >= num_votes)].dropna()
    else:
        filtered_df = item_df.dropna()

    for index in similar_indices:
        title = item_df['title'].iloc[index]
        if title not in filtered_df['title'].values:
            recommendations.append(title)

    return render_template('recommendations.html', recommendations=recommendations)


if __name__ == '__main__':
    app.run(debug=False)
