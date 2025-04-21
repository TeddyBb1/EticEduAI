from transformers import pipeline

classifier = pipeline("text-classification", model="roberta-base-openai-detector")

def check_ai_probability(text):
    try:
        result = classifier(text[:1000])[0]
        score = round(result['score'] * 100, 2)
        return score if result['label'] == 'AI-generated' else 100 - score
    except Exception as e:
        print(f"AI detection failed: {e}")
        return 0