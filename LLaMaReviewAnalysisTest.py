import os
from datetime import datetime
from llama_cpp import Llama
import time
import re

model_name = "Meta-Llama-3-8B-Instruct.Q6_K.gguf"
model_path = os.path.join(os.path.dirname(__file__), model_name)

model_kwargs = {
    "n_ctx": 2000,  # Context length to use
    "n_threads": 16,  # Number of CPU threads to use
    "n_gpu_layers": -1,  # Number of model layers to offload to GPU
}

generation_kwargs = {
    "max_tokens": 100,  # Max number of new tokens to generate
    "stop": ["<|endoftext|>", "</s>"],  # Text sequences to stop generation on
    "echo": False,  # Echo the prompt in the output
    "top_k": 1,  # This is essentially greedy decoding, since the model will always return the highest-probability token. Set this value > 1 for sampling decoding
}

llm = Llama(model_path=model_path, **model_kwargs)

def get_sentiment_score(review_text):
    prompt = f"""
    Please provide only the overall sentiment score for the following review on a scale of 1 to 10. Do not include any explanations or additional text. The review text is wrapped in <review> tags.

    <review>{review_text}</review>"""

    res = llm(prompt, **generation_kwargs)
    output = res["choices"][0]["text"].strip()
    
    # Extract the sentiment score using a regular expression
    match = re.search(r'\d+', output)
    if match:
        sentiment_score = int(match.group())
        return sentiment_score
    else:
        return None

def get_tags(review_text, start_char='[', end_char=']'):
    prompt = f"""
    Here is a review of a video-game. Respond with comma delimited tags that describe the product in the format "{start_char}tag1, tag2, tag3, ...{end_char}". 
    Do not use adjectives or descriptions. Only include the tags and wrapping characters in your response. The review text is wrapped in <review> tags.
    <review>{review_text}</review>"""

    res = llm(prompt, **generation_kwargs)
    output = res["choices"][0]["text"]

    # Find the tags wrapped by the start and end characters
    start_index = output.find(start_char)
    end_index = output.find(end_char)

    if start_index == -1 or end_index == -1 or start_index >= end_index:
        return None

    # Extract the tags between the start and end characters
    tags_text = output[start_index + 1 : end_index]
    print('RAW TAGS: ' + tags_text)

    # Split the tags by comma
    tags = tags_text.split(",")

    # Remove underscores, leading/trailing whitespace and convert to lowercase
    tags = [tag.replace("_", " ").strip().lower() for tag in tags]

    # Filter out any empty or blank tags
    tags = [tag for tag in tags if tag]

    return tags if tags else None

# Example list of review texts
review_texts = [
    "You know it's really pathetic to see all these negative reviews about how things are broken or not optimized. My God it's an EARLY RELEASE/ EARLY ACCESS game! It's not done and it's only been out for 2 days at this point! But I personally absolutely LOVE IT. I've been watching and waiting for this game for 6 months since I learned about it. Honestly I'm soo greatful that they released it now in the shape that it's in. I had two disconnects the first day and NONE today with an 8 hour play session. I have been waiting on a game just like this.. forever. It has mechanics I didn't even know I wanted. The grind is fantastic, same with gun play and intense combat. Missions are left to you to actually find locations and items. They are barebones but it's more than ok, clearly they r working on it. Oh and there are 150 various missions at release, so yeah that's awesome as well. I am just greatful to Madfinger Games for putting so much love into this and releasing it when they did. This game is gonna have an awesome future and I'll be right there with it.",
    "This game is fun! It has fantastic bones to it. Yes, sure it has its issues. Its an alpha that's 3 days old. However Im 33 hours in already and love it. I'm excited to see the future of the game. It has so much potential. Unfortunately some people are having issues, luckily for me I am not one of them. I also only have a 2070ti as well so nothing crazy. I manage to play the game just fine.",
    "I honestly enjoy the game alot, despite performance, despite tons of bugs and overall issues with gameplay I can still look past those things and try to find enjoyment but server issues and being unable to squad up with friends and que into a server makes this game total trash. Ive spent more time tonight attempting to get into a server then actually playing. Id avoid this game until the either servers and matchmaking are fixed or the game settles down in playerbase.",
]

start_time = time.time()

for i, review_text in enumerate(review_texts, start=1):
    print(f"Review {i}:")
    print("Content:", review_text)
    
    sentiment_score = get_sentiment_score(review_text)
    print("Sentiment Score:", sentiment_score)
    
    tags = get_tags(review_text)
    print("Tags:", tags)

end_time = time.time()
total_time = end_time - start_time
average_time_per_review = total_time / len(review_texts)

print(f"Total time: {total_time:.2f} seconds")
print(f"Average time per review: {average_time_per_review:.2f} seconds")