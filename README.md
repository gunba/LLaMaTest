![vrb1](https://github.com/gunba/steam-review-analyzer/assets/11908184/73c030ae-dc47-4d76-96d6-b6e9b58000e8)
![vrb2](https://github.com/gunba/steam-review-analyzer/assets/11908184/cb58e27e-89b3-413f-8ec0-e502b1a92c68)

# Game Review Analysis with LLM, ETL, and PowerBI

This project showcases the use of Large Language Models (LLM), Extract-Transform-Load (ETL) techniques, and PowerBI to analyze and visualize game reviews. The primary focus is on the game "Helldivers 2" and the impact of a review bomb on the game's reception.

## Key Components

- `Helldivers2_ReviewAnalysis.pbix`: The main PowerBI file containing the interactive slides and visualizations. 

- `review_analyzer.py`: Contains the LLM implementation with pre-configured prompts. The `ReviewAnalyzer` object facilitates LLM calls.

- `process_reviews.py`: Applies the LLM model to the JSON reviews sourced from the STEAM API.

- `review_miner.py`: Uses the STEAM API to collect review JSON data for analysis.

- `network_graph/network_graph.py`: Generates a network graph visualization for the PowerBI.

## Proof of Concept

This project demonstrates a proof of concept for analyzing game reviews from any source using LLM, ETL, and PowerBI. The process can be easily adapted to handle reviews from various platforms.

## PowerBI Presentation

The PowerBI presentation follows an interactive slide approach, where users can navigate through the content by clicking the button at the bottom of each slide. The presentation covers the release of Helldivers 2, its initial success, and the subsequent review bombing due to the requirement of PSN logins to play the game.

The presentation explains how STEAM reviews work and introduces the enhancements provided by our tool, including:
- Tags that summarize review content from text
- Review sentiment scores out of 10
- Writing quality scores out of 10

## Analysis Highlights

1. **Visualizing a Review Bomb**
   - Demonstrates the inorganic nature of the negative reviews during the review bomb period.
   - Shows that negative sentiment is strongest around tags specifically related to the boycott.
   - Reveals that actual user sentiment based on writing style often does not align with the thumbs up/thumbs down reviews left by users.
   - Highlights the deterioration of review quality during the review bomb.
   - Compares the negative sentiment around actual game problems with the stronger negative sentiment for tags representing the boycott (PSN, SONY, ACCOUNT, etc.).

2. **Piercing the Veil**
   - Demonstrates how the LLM-powered tags and ratings can be used to circumvent the review bomb and obtain actual user sentiment.
   - Utilizes tags to identify reviews that exhibit review bomb or normal patterns (e.g., users expressing positive sentiment in the review text but giving a thumbs down).
   - Creates a tag co-occurrence network that groups review tags into communities, revealing two distinct communities: review bomb and normal reviews.
   - Highlights tags commonly associated with middling user sentiment (5-7) to uncover legitimate gameplay issues raised by users.

Feel free to explore the PowerBI presentation and the accompanying code to gain insights into the review analysis process and the impact of the review bomb on Helldivers 2.
