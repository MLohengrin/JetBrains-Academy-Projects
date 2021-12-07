# Key Terms Extraction

import string

import nltk as nltk
from lxml import etree
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
root = etree.parse('news.xml').getroot()
lemmatizer = WordNetLemmatizer()
taboos = stopwords.words('english')
taboos.extend(string.punctuation)
titles = []
dataset = []

for news in root[0]:
    title = news[0]
    titles.append(title.text)
    corpus = news[1]
    tokens = word_tokenize(corpus.text.lower())
    # tokens_dict = defaultdict(int)
    tokens_dict = list()
    for word in tokens:
        lem_word = lemmatizer.lemmatize(word)
        if lem_word in taboos or nltk.pos_tag([lem_word])[0][1] != 'NN':
            continue
        # tokens_dict[lem_word] += 1
        tokens_dict.append(lem_word)
    dataset.append(" ".join(tokens_dict))
    # most_common = []
    # dealf_sorted = sorted(tokens_dict, reverse=True)
    # for k in sorted(dealf_sorted, key=tokens_dict.__getitem__, reverse=True):
    #     most_common.append(k)

tfidf_matrix = vectorizer.fit_transform(dataset)
terms = vectorizer.get_feature_names()
all_values = tfidf_matrix.toarray()
most_commons = []

for i in range(tfidf_matrix.shape[0]):
    i_dict = dict()
    values = all_values[i]
    for word, value in zip(terms, values):
        i_dict[word] = value
    dealf_sorted = sorted(i_dict, reverse=True)
    most_commons.append(list())
    for k in sorted(dealf_sorted, key=i_dict.__getitem__, reverse=True):
        most_commons[i].append(k)
    # print(most_commons[i])

# print(tfidf_matrix.shape[0], tfidf_matrix.shape[1])

for i in range(tfidf_matrix.shape[0]):
    print(f'{titles[i]}:')
    print(*[w for w in most_commons[i][:5]])
    print()
