#!/usr/bin/env python3
import sys
import csv

current_imdb_id = None
movie_title = None
ratings = []
review_texts = []

def sentiment_from_text(text):
    text = text.lower()
    positive_words = ['good', 'great', 'love', 'excellent', 'amazing', 'awesome', 'best', 'nice']
    negative_words = [
        'bad', 'boring', 'hate', 'worst', 'awful', 'terrible', 'poor', 'disappoint',
        'sucks', 'dull', 'annoying', 'waste', 'fail', 'forgettable', 'mediocre', 'lame', 'pathetic'
    ]

    score = 0
    for word in positive_words:
        if word in text:
            score += 1
    for word in negative_words:
        if word in text:
            score -= 2

    if score > 0:
        return '긍정'
    elif score < 0:
        return '부정'
    else:
        return '평범'

def print_result_csv(writer, imdb_id, title, ratings, texts):
    if not ratings or title is None:
        return
    avg_rating = sum(ratings) / len(ratings)
    if avg_rating >= 8:
        rating_sentiment = '긍정'
    elif avg_rating >= 5:
        rating_sentiment = '평범'
    else:
        rating_sentiment = '부정'

    sentiments = [sentiment_from_text(t) for t in texts]
    pos_count = sentiments.count('긍정')
    neg_count = sentiments.count('부정')
    total = len(sentiments)

    sentiment_score = pos_count - neg_count

    if total == 0:
        text_sentiment = '평범'
    else:
        if abs(sentiment_score) <= total * 0.2:
            text_sentiment = '호불호'
        else:
            text_sentiment = '긍정' if sentiment_score > 0 else '부정'

    if (rating_sentiment == '부정' and text_sentiment == '평범') or (text_sentiment == '부정' and rating_sentiment == '평범'):
        overall_sentiment = '부정'
    elif rating_sentiment != text_sentiment and text_sentiment != '평범' and rating_sentiment != '평범':
        overall_sentiment = '호불호'
    else:
        overall_sentiment = rating_sentiment

    writer.writerow([
        imdb_id,
        title,
        f"{avg_rating:.2f}",
        rating_sentiment,
        text_sentiment,
        overall_sentiment
    ])

csv_writer = csv.writer(sys.stdout)
csv_writer.writerow(['IMDB_ID', 'Title', 'Average_Rating', 'Rating_Sentiment', 'Review_Sentiment', 'Overall_Sentiment'])

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split('\t')
    if len(parts) < 3:
        continue

    imdb_id, record_type = parts[0], parts[1]

    if current_imdb_id != imdb_id:
        if current_imdb_id is not None:
            print_result_csv(csv_writer, current_imdb_id, movie_title, ratings, review_texts)
        current_imdb_id = imdb_id
        movie_title = None
        ratings = []
        review_texts = []

    if record_type == 'L':
        movie_title = parts[2]
    elif record_type == 'R' and len(parts) >= 4:
        try:
            rating = float(parts[2])
            ratings.append(rating)
            review_texts.append(parts[3])
        except:
            pass

if current_imdb_id is not None:
    print_result_csv(csv_writer, current_imdb_id, movie_title, ratings, review_texts)
