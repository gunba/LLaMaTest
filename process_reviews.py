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
    return latest_file

def process_reviews(min_length=200):
    analyzer = ReviewAnalyzer()
    processed_reviews = []
    
    # Find latest json file to process.
    data_folder = 'raw_reviews'
    latest_json_file = get_latest_json_file(data_folder)
    if not latest_json_file:
        print(f"No JSON files found in the '{data_folder}' folder.")
        return []
    
    with open(os.path.join(data_folder, latest_json_file), 'r') as file:
        reviews_data = json.load(file)
    
    # Object structure is list -> [0] -> reviews dict
    reviews = reviews_data[0]['reviews']
    
        # Review ID is stored twice (same as 'recommendationId' in the review structure)
    for review_id, review in reviews.items():
        review_text = review['review']

        # Skip reviews that are too short
        if len(review_text) < min_length:
            continue

        try:
            # Tags has the longest instruct input, try it first
            tags = analyzer.get_tags(review_text)
            sentiment_score = analyzer.get_sentiment_score(review_text)
            quality_score = analyzer.get_quality_score(review_text)

            # Throw away any review where the LLM cannot generate a result (not common)
            if sentiment_score is None or quality_score is None or tags is None:
                print(f"Skipping review {review_id} due to missing analysis results.")
                continue

        # Review text can be greater than context length
        except ValueError as e:
            print(f"Skipping review {review_id} due to error: {str(e)}")
            continue

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
    
    reviews_folder = 'processed_reviews'
    os.makedirs(reviews_folder, exist_ok=True)
    file_path = os.path.join(reviews_folder, latest_json_file)
    with open(file_path, 'w') as file:
        json.dump(processed_reviews, file, indent=4, default=str)

    return processed_reviews

def main():
    processed_reviews = process_reviews()

    print(f"Processed {len(processed_reviews)} reviews. Saved to processed_reviews folder.")

if __name__ == '__main__':
    main()