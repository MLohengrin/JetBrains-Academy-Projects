# Text Generator

from collections import defaultdict
from nltk.tokenize import WhitespaceTokenizer
import random

with open(input(), 'r', encoding='utf-8') as f:
    corpus = f.readlines()

corpus_str = ''.join(corpus)
tokens = WhitespaceTokenizer().tokenize(corpus_str)

trigrams = [tokens[i] + ' ' + tokens[i + 1] + ' ' + tokens[i + 2] for i in range(len(tokens) - 2)]
big_dict = defaultdict(dict)

for tris in trigrams:
    head_a, head_b, tail = tris.split()
    head = f'{head_a} {head_b}'
    big_dict[head].setdefault(tail, 0)
    big_dict[head][tail] += 1

sentences = []

for i_sent in range(10):
    while True:
        first_word, second_word = random.choice(list(big_dict.keys())).split()
        if first_word[0].isupper() and first_word[-1] not in ['.', '!', '?']:
            sentence = [first_word, second_word]
            break
    while True:
        last_two = f'{sentence[-2]} {sentence[-1]}'
        population = list(big_dict[last_two].keys())
        weight = list(big_dict[last_two].values())
        next_word = random.choices(population, weights=weight)[0]
        sentence.append(next_word)
        if next_word[-1] in ['.', '!', '?'] and len(sentence) >= 5:
            break
    sentences.append(' '.join(sentence))

print(*sentences, sep='\n')
