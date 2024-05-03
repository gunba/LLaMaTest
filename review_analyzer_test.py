from review_analyzer import ReviewAnalyzer
import re

analyzer = ReviewAnalyzer()

review_text = "So overall I liked the game but it’s not perfect. Story feels random. Same goes for dialogs. Combat is really fun but to a point. Closer to the end amount of enemies is so big that they start overlapping heavily and it’s barely possible to keep the cool flow of dodging and parrying and performing combos. Level design is good as it breaks monotony with some platforming sections that aren't annoying. Main character animations are really cool and give a lot of joy when performing things (even running). Rest of the graphical design is meh. Soundtrack on the other hand is superb. It fits perfectly the game to a degree where I want to replay the game to hear it again. Fun to play but I hoped for more after all the reviews. It took me 7h to finish it on Normal. I would give it 7.5/10 - not a must play but you won't regret spending money on it."
review_text = re.sub(r'[^a-zA-Z0-9\s]', '', review_text)

sentiment_score = analyzer.get_sentiment_score(review_text)
quality_score = analyzer.get_quality_score(review_text)
tags = analyzer.get_tags(review_text)

print("Sentiment Score:", sentiment_score)
print("Quality Score:", quality_score)
print("Tags:", tags)