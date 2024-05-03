import json
import datetime
import os
from steamreviews import download_reviews_for_app_id

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def collect_reviews(app_id, num_reviews=100, day_range=28, save_json=True):
    # Set the request parameters for filtering reviews
    request_params = {
        'language': 'english',
        'purchase_type': 'steam',
        'filter': 'recent',
        'day_range': day_range
    }

    reviews = download_reviews_for_app_id(
        app_id,
        query_count=num_reviews,
        chosen_request_params=request_params
    )

    if save_json:
        # Get the current script's directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Create the "data" folder if it doesn't exist
        data_dir = os.path.join(script_dir, 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        # Generate a timestamp for the filename
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        json_filename = f'{app_id}_{timestamp}.json'
        
        # Save the collected reviews in a JSON file in the "data" folder
        json_filepath = os.path.join(data_dir, json_filename)
        with open(json_filepath, 'w') as file:
            json.dump(reviews, file, indent=4)
        
        print(f"Collected {len(reviews)} reviews for app ID {app_id}. Saved to {json_filepath}.")
    else:
        # Return the collected reviews as a list
        return reviews

def main():
    # Set the app ID for which you want to collect reviews
    app_id = 1172470  # Apex Legends

    # Set the number of reviews to collect
    num_reviews = 1000

    # Set the day range for recent reviews
    day_range = 28

    # Collect reviews and save them in a JSON file
    collect_reviews(app_id, num_reviews, day_range)

if __name__ == '__main__':
    main()