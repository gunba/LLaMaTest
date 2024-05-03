import os
from llama_cpp import Llama
import re

class ReviewAnalyzer:
    def __init__(self, model_name="Meta-Llama-3-8B-Instruct.Q6_K.gguf", max_tokens=25, context_length=2000):
        model_path = os.path.join(os.path.dirname(__file__), model_name)
        
        model_kwargs = {
            "n_ctx": context_length,
            "n_threads": 16,
            "n_gpu_layers": -1,
        }
        
        generation_kwargs = {
            "max_tokens": max_tokens,
            "stop": ["<|endoftext|>", "</s>"],
            "echo": False,
            "top_k": 1,
        }
        
        self.llm = Llama(model_path=model_path, **model_kwargs)
        self.generation_kwargs = generation_kwargs

    def get_sentiment_score(self, review_text):
        prompt = f"""    
        Review: {review_text}
        
        Rating (out of 10): """

        res = self.llm(prompt, **self.generation_kwargs)
        output = res["choices"][0]["text"].strip()
        
        # Extract the sentiment score using a regular expression
        match = re.search(r'\d+', output)
        if match:
            sentiment_score = int(match.group())
            return sentiment_score
        else:
            return None

    def get_quality_score(self, review_text):
        prompt = f"""
        Review: {review_text}
        
        Review Writing Quality Rating (out of 10): """

        res = self.llm(prompt, **self.generation_kwargs)
        output = res["choices"][0]["text"].strip()
        
        # Extract the quality score using a regular expression
        match = re.search(r'\d+', output)
        if match:
            quality_score = int(match.group())
            return quality_score
        else:
            return None

    def get_tags(self, review_text):
        prompt = f"""
        Here is a review of a product. Respond with comma delimited tags that describe the product in the format "tag1,tag2,tag3,...". 
        Do not use adjectives or descriptions. Only include the tags in your response, and end the tags with a non-alphanumeric character that is not a comma. The review text is wrapped in <review> tags.
        <review>{re.sub(r'[^a-zA-Z0-9\s]', '', review_text)}</review>
        
        Tags: """

        res = self.llm(prompt, **self.generation_kwargs)
        output = res["choices"][0]["text"].strip()

        # Find the index of the first non-alphanumeric character that is not a comma
        end_index = None
        for i, char in enumerate(output):
            if not char.isalnum() and not char.isspace() and char != ',':
                end_index = i
                break

        if end_index is None:
            end_index = len(output)

        # Extract the tags before the non-alphanumeric character or the end of the string
        tags_text = output[:end_index]

        # Split the tags by comma
        tags = tags_text.split(",")

        # Remove underscores, leading/trailing whitespace and convert to lowercase
        tags = [tag.replace("_", " ").strip().lower() for tag in tags]

        # Filter out any empty or blank tags
        tags = [tag for tag in tags if tag]

        return tags if tags else None