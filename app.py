from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import joblib

app = Flask(__name__)

# Load model
model = joblib.load('model.joblib')

# Load datasets
dataframes = [
    pd.read_csv('./data/3.1-data-sheet-udemy-courses-business-courses.csv'),
    pd.read_csv('./data/3.1-data-sheet-udemy-courses-design-courses.csv'),
    pd.read_csv('./data/3.1-data-sheet-udemy-courses-music-courses.csv'),
    pd.read_csv('./data/3.1-data-sheet-udemy-courses-web-development.csv')
]
all_courses = pd.concat(dataframes, ignore_index=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'GET':
        return redirect(url_for('index'))

    topic = request.form['topic'].lower()

    # Drop rows where course_title is missing
    cleaned_df = all_courses.dropna(subset=['course_title'])

    # Filter on topic match (case-insensitive)
    filtered = cleaned_df[cleaned_df['course_title'].str.lower().str.contains(topic, na=False)]

    results = filtered[['course_title', 'url', 'price', 'num_lectures', 'level',
                        'content_duration', 'subject']].drop_duplicates().to_dict(orient='records')

    return render_template('recommend.html', courses=results)


# 404 Error Handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404