import pandas as pd
import numpy as np
import nltk
import re
import string
from flask import Flask, request, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)


def process_movie_data(file_name):
    movies = pd.read_csv(file_name, sep=',')
    movies = movies.rename(columns=lambda x: x.strip().lower())

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
    movies['type'] = 'movie'

    return movies

def process_tv_data(file_name):
    tv_series = pd.read_csv(file_name, sep=',')
    tv_series = tv_series.rename(columns=lambda x: x.strip().lower())

    # slice off unused columns
    tv_series = tv_series[['series name', 'details', 'year',
                        'runtime', 'ranking',
                        'genre', 'rating', 'votes', 'actor 1',
                        'actor 2', 'actor 3', 'actor 4']]

    # rename columns
    tv_series = tv_series.rename(columns={
                                'series name': 'title',
                                'details': 'description',
                                'actor 1': 'actor-1',
                                'actor 2': 'actor-2',
                                'actor 3': 'actor-3',
                                'actor 4': 'actor-4'})

    tv_series.fillna('', inplace=True)
    tv_series['director'] = ''
    tv_series['type'] = 'tv series'

    return tv_series

def process_video_game_data(file_name):
    video_games = pd.read_csv(file_name, sep=',')
    video_games = video_games.rename(columns=lambda x: x.strip().lower())

    # slice off unused columns
    video_games = video_games[['video game name', 'details', 'year',
                            'ranking', 'genre', 'rating', 'votes',
                            'director', 'actor-1', 'actor-2',
                            'actor-3', 'actor-4']]

    # rename columns
    video_games = video_games.rename(columns={'video game name': 'title',
                                            'details': 'description'})

    video_games.fillna('', inplace=True)
    video_games['type'] = 'video game'

    return video_games

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

def calculate_cosine_similarity(title, item_matrix, vectorizer):
    # Transform the user input
    title_vector = vectorizer.transform([title])

    # Calculate cosine similarity
    cosine_similarities = cosine_similarity(title_vector, item_matrix)

    return cosine_similarities

# media
movies = process_movie_data('../data/movies.csv')
tv_series = process_tv_data('../data/tv-series.csv')
video_games = process_video_game_data('../data/video-games.csv')
media = pd.concat([movies, tv_series, video_games], axis=0)
corpus_columns = ['actor-1', 'actor-2', 'actor-3', 'actor-4', 'description', 'director', 'genre', 'title']
media['corpus'] = media[corpus_columns].apply(lambda x: ' '.join(x), axis=1)

# prepare to tokenize words
nltk.download('wordnet')
wpt = nltk.WordPunctTokenizer()

# download stopwords
nltk.download('stopwords')
stop_words = nltk.corpus.stopwords.words('english')

media_clean = media.apply(np.vectorize(process))

# Define TF-IDF vectorizers for each dataset
tfidf_vec = TfidfVectorizer()
tfidf_matrix = tfidf_vec.fit_transform(media_clean['corpus'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        title_orig = request.form.get('title', default=None, type=str)
        key_words = request.form.get('key_words', default="", type=str)
        requested_media = request.form.getlist('media', type=str)
        genre = request.form.get('genre')
        ranking = request.form.get('ranking', default=None, type=float)
        runtime = request.form.get('runtime', default=None, type=float)
        year = request.form.get('year', default=None, type=int)
        rating = request.form.get('rating', default=None, type=float)
        num_votes = request.form.get('num_votes', default=None, type=int)
        num_recommendations = request.form.get('num_recommendations', default=10, type=int)
    except ValueError as e:
        print("Could not process Request: ", e)

    key_words = process(key_words)

    # when list is empty, provide recommendations for all media types
    if not requested_media:
        requested_media = ["movie", "tv series", "video game"]

    item_matrix = tfidf_matrix
    vectorizer = tfidf_vec
    item_df = media

    title = title_orig.lower()

    media_titles = media['title'].str.lower()
    if (media_titles == title).any():
        idx = np.where(title == media_titles)[0][0]
        user_data = " ".join([media.iloc[idx]['corpus'], key_words])

        # Calculate cosine similarity
        cosine_similarities = calculate_cosine_similarity(user_data, item_matrix, vectorizer)

        # Get the indices of the top recommendations
        similar_indices = cosine_similarities[0].argsort()[-2::-1]
    else:
        user_data = " ".join([title, key_words])

        # Calculate cosine similarity
        cosine_similarities = calculate_cosine_similarity(user_data, item_matrix, vectorizer)

        # Get the indices of the top recommendations
        similar_indices = cosine_similarities[0].argsort()[::-1]

    # # Convert to float
    # item_df['ranking'] = pd.to_numeric(
    #     item_df['ranking'], errors='coerce')

    # item_df['runtime'] = pd.to_numeric(
    #     item_df['runtime'], errors='coerce')

    # item_df['votes'] = pd.to_numeric(
    #     item_df['votes'], errors='coerce')

    # # Filter the data based on user preferences and remove rows with NaN values
    # if not ((ranking is None) or (year is None) or (rating is None) or (runtime is None) or (num_votes is None)):

    #     filtered_df = item_df[
    #         (item_df['ranking'] >= ranking) &
    #         (item_df['runtime'] <= runtime) &
    #         (item_df['year'] == year) &
    #         (item_df['rating'] >= rating) &
    #         (item_df['votes'] >= num_votes)].dropna()
    # else:
    #     filtered_df = item_df.dropna()

    recommendations = []
    ids = []
    media_types = []
    for index in similar_indices:
        if len(recommendations) >= num_recommendations:
            break

        title = item_df['title'].iloc[index]
        media_type = item_df['type'].iloc[index]

        if media_type in requested_media:
            recommendations.append(title)
            ids.append(index)
            if item_df['type'].iloc[index] == 'video game':
                media_types.append("Video Game")
            elif item_df['type'].iloc[index] == 'movie':
                media_types.append('Movie')
            else:
                media_types.append('TV Series')

    return render_template(
        'recommendations.html',
        recommendations=zip(recommendations, ids, media_types),
        num_recommendations=num_recommendations,
        title=title_orig
    )

@app.route('/search', methods=['GET'])
def search():
    try:
        media_id = request.args.get('media_id', default=None, type=int)
        print("Searching for ", media_id)
    except ValueError as e:
        print("Could not process Request: ", e)

    item_df = media
    title = item_df['title'].iloc[media_id]
    actors = ", ".join([item_df['actor-1'].iloc[media_id],
                        item_df['actor-2'].iloc[media_id],
                        item_df['actor-3'].iloc[media_id],
                        item_df['actor-4'].iloc[media_id]])
    director = item_df['director'].iloc[media_id]
    description = item_df['description'].iloc[media_id]
    genre = item_df['genre'].iloc[media_id]


    return render_template(
        'search.html',
        media_id=media_id,
        title=title,
        actors=actors,
        director=director,
        description=description,
        genre=genre
    )

if __name__ == '__main__':
    app.run(debug=True)
