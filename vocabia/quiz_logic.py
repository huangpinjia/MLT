import json
import random

def load_words():
    with open('word_data.json', 'r') as f:
        return json.load(f)

def generate_quiz(words, num_questions=5):
    selected = random.sample(words, num_questions)
    questions = []
    for item in selected:
        question = {
            'word': item['word'],
            'definition': item['definition'],
            'choices': item['choices'],
            'answer': item['choices'].index(item['definition'])  # index of correct answer
        }
        random.shuffle(question['choices'])
        questions.append(question)
    return questions
