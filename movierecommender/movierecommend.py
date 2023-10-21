

# Movie Recommendation System


from flask import Flask, request, render_template
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import re
import numpy as np
import difflib


app = Flask(__name__)


# Load the movie dataset
df = pd.read_csv('tmdb_5000_movies.csv')  # Load your movie dataset

df = df[['title', 'tagline', 'overview', 'genres', 'popularity']]
df.tagline.fillna('', inplace=True)
df['description'] = df['tagline'].map(str) + ' ' + df['overview']
df.dropna(inplace=True)

stop_words = nltk.corpus.stopwords.words('english')


def normalize_document(doc):
    # lower case and remove special characters\whitespaces
    doc = re.sub(r'[^a-zA-Z0-9\s]', '', doc, re.I | re.A)
    doc = doc.lower()
    doc = doc.strip()

    # tokenize document
    tokens = nltk.word_tokenize(doc)

    # filter stopwords out of document
    filtered_tokens = [token for token in tokens
                       if token not in stop_words]

    # re-create document from filtered tokens
    doc = ' '.join(filtered_tokens)
    return doc


normalize_corpus = np.vectorize(normalize_document)

movie_corpus = normalize_corpus(list(df['description']))


# Preprocess and vectorize movie descriptions
tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=2)
tfidf_matrix = tfidf.fit_transform(movie_corpus)


# Calculate cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form['user_input']

    # Find the best match for the user input among movie titles
    matches = difflib.get_close_matches(user_input, df['title'], n=5,
                                        cutoff=0.6)

    if matches:
        user_input = matches[0]

        # Find the index of the movie with the highest cosine similarity
        idx = df.index[df['title'] == user_input].tolist()[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the top 30 recommended movies
        top_recommendations = []
        for score in sim_scores[1:11]:
            movie_index = score[0]
            movie_title = df['title'].iloc[movie_index]
            top_recommendations.append(movie_title)

    # Check if the user input movie title exists in the DataFrame
    if user_input not in df['title'].values:
        return render_template('error.html',
                               message="Movie Not Found."
                               " Please Enter a Correct Title.")

    # Pass the user input and close match suggestions to the template
    return render_template('recommendations.html',
                           user_input=user_input,
                           recommendations=top_recommendations)


if __name__ == '__main__':
    app.run(debug=False)
