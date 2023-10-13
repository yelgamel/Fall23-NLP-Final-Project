

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import re
import string
from flask import Flask, render_template, request
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


app = Flask(__name__)


# create the main page in web app
@app.route('/')
def index():
    return render_template('index.html')


# create result page in web app and apply analyze_sentiment function
@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        text = request.form['text']
        analysis = analyze_sentiment(text)
        return render_template('result.html', analysis=analysis)


def analyze_sentiment(txt):

    # prepare to tokenize words
    wpt = nltk.WordPunctTokenizer()

    # lower case and remove special characters/whitespaces
    txt = re.sub(r'[^a-zA-Z0-9\s]', '', txt, re.I | re.A)
    txt = txt.lower()
    txt = txt.strip()
    tokens = wpt.tokenize(txt)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))

    # remove stopwords
    filtered_tokens = [token for token in tokens
                       if token not in stop_words
                       and token not in list(string.punctuation)]

    # Initialize WordNetlemmatizer and lemmatize
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = " ".join([lemmatizer.lemmatize(token)
                                  for token in filtered_tokens])

    # join lemmatized tokens
    preprocessed_text = "".join(lemmatized_tokens)

    # Initialize VADER sentiment analyzer
    sia = SentimentIntensityAnalyzer()

    # find sentiment using VADER
    sentiment_scores = sia.polarity_scores(txt)

    # find polarity score
    polarity = round(sentiment_scores['compound'], 2)

    # find sentiment based on polarity
    if polarity > 0:
        sentiment = 'Positive'

    elif polarity < 0:
        sentiment = 'Negative'

    else:
        sentiment = 'Neutral'

    return {'text': preprocessed_text, 'sentiment': sentiment,
            'polarity': polarity}


if __name__ == '__main__':
    app.run(debug=False)
