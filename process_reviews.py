import json
import os
from datetime import datetime
from review_analyzer import ReviewAnalyzer

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def get_latest_json_file(folder_path):
    json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]
    if not json_files:
        return None
    latest_file = max(json_files, key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))
    return os.path.join(folder_path, latest_file)

def process_reviews(min_length=200):
    analyzer = ReviewAnalyzer()
    processed_reviews = []

    # Get the latest JSON file from the "data" folder
    data_folder = 'data'
    latest_json_file = get_latest_json_file(data_folder)
    if not latest_json_file:
        print("No JSON files found in the 'data' folder.")
        return []

    # Read reviews from the latest JSON file
    with open(latest_json_file, 'r') as file:
        reviews_data = json.load(file)

    reviews = reviews_data['reviews']

    for review_id, review in reviews.items():
        review_text = review['review']

        # Filter reviews based on length
        if len(review_text) < min_length:
            continue

        sentiment_score = analyzer.get_sentiment_score(review_text)
        quality_score = analyzer.get_quality_score(review_text)
        tags = analyzer.get_tags(review_text)

        # Convert timestamps to datetime objects
        timestamp_created = datetime.fromtimestamp(review['timestamp_created'])
        timestamp_updated = datetime.fromtimestamp(review['timestamp_updated'])
        last_played = datetime.fromtimestamp(review['author']['last_played'])

        processed_review = {
            'recommendationid': review['recommendationid'],
            'author': {
                'steamid': review['author']['steamid'],
                'num_games_owned': review['author']['num_games_owned'],
                'num_reviews': review['author']['num_reviews'],
                'playtime_forever': review['author']['playtime_forever'],
                'playtime_last_two_weeks': review['author']['playtime_last_two_weeks'],
                'playtime_at_review': review['author']['playtime_at_review'],
                'last_played': last_played
            },
            'language': review['language'],
            'review': review_text,
            'timestamp_created': timestamp_created,
            'timestamp_updated': timestamp_updated,
            'voted_up': review['voted_up'],
            'votes_up': review['votes_up'],
            'votes_funny': review['votes_funny'],
            'weighted_vote_score': review['weighted_vote_score'],
            'comment_count': review['comment_count'],
            'steam_purchase': review['steam_purchase'],
            'received_for_free': review['received_for_free'],
            'written_during_early_access': review['written_during_early_access'],
            'sentiment_score': sentiment_score,
            'quality_score': quality_score,
            'tags': tags
        }

        processed_reviews.append(processed_review)

    return processed_reviews

def main():
    min_length = 200  # Minimum length of reviews to consider

    # Process the reviews using the LLM
    processed_reviews = process_reviews(min_length)

    # Create the "reviews" folder if it doesn't exist
    reviews_folder = 'reviews'
    os.makedirs(reviews_folder, exist_ok=True)

    # Generate a filename for the processed reviews JSON file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'processed_reviews_{timestamp}.json'
    file_path = os.path.join(reviews_folder, filename)

    # Save the processed reviews in a JSON file
    with open(file_path, 'w') as file:
        json.dump(processed_reviews, file, indent=4, default=str)

    print(f"Processed {len(processed_reviews)} reviews. Saved to {file_path}.")

if __name__ == '__main__':
    main()