# Multilingual Online Translator

import requests
from bs4 import BeautifulSoup
import sys

languages = {1: 'Arabic', 2: 'German', 3: 'English', 4: 'Spanish', 5: 'French', 6: 'Hebrew',
             7: 'Japanese', 8: 'Dutch', 9: 'Polish', 10: 'Portuguese', 11: 'Romanian',
             12: 'Russian', 13: 'Turkish'}

# print("Hello, you're welcome to the translator. Translator supports:")
# for k, v in languages.items():
#     print(f'{k}. {v}')
# print('Type the number of your language:')
# lang_from = input()
# print('Type the number of language you want to translate to:')
# lang_to = input()
# print('Type the word you want to translate:')
# word = input().lower()

lang_from, lang_to, word = sys.argv[1], sys.argv[2], sys.argv[3].lower()
try:
    lang_from = [v.lower() for v in languages.values()].index(lang_from) + 1
except ValueError:
    print(f"Sorry, the program doesn't support {lang_from}")
    exit()

try:
    if lang_to == 'all':
        lang_to = 0
    else:
        lang_to = [v.lower() for v in languages.values()].index(lang_to) + 1
except ValueError:
    print(f"Sorry, the program doesn't support {lang_to}")
    exit()

f = open(f'{word}.txt', 'w', encoding='utf-8')

for n in languages.keys():
    if (int(lang_to) != 0 and int(lang_to) != n) or (int(lang_to) == 0 and int(lang_from) == n):
        continue
    else:
        lang_url = f'{languages[int(lang_from)].lower()}-{languages[n].lower()}'

        try:
            r = requests.get(f'https://context.reverso.net/translation/{lang_url}/{word}',
                             headers={'User-Agent': 'Mozilla/5.0'})
        except ConnectionError:
            print("Something wrong with your internet connection")
            exit()

        soup = BeautifulSoup(r.content, 'html.parser')
        # print(str(r.status_code) + ' OK' if r else 'Error')
        # print()
        translations = soup.find_all('a', class_='translation')
        examples = soup.find_all('div', class_='ltr')
        t_list = []
        e_list = []
        for t in translations:
            if t.text != 'Translation':
                t_list.append(t.text.strip().replace(',', '').replace('?', ''))
        for e in examples:
            e_list.append(e.text.strip())

        if len(t_list) == 1:
            print(f'Sorry, unable to find {word}')
            exit()

        out = ''
        out += f'\n{languages[n]} Translations:\n'
        # print(f'\n{languages[n]} Translations:')
        for i in range(min(45, len(t_list) - 1)):
            out += f'{t_list[i + 1]}\n'

        out += f'\n{languages[n]} Examples:\n'
        # print(f'\n{languages[n]} Examples:')
        for i in range(2, min(412, len(e_list) - 2), 2):
            # print(f'{e_list[i]}\n{e_list[i + 1]}\n')
            out += f'{e_list[i]}\n{e_list[i + 1]}\n\n'

        print(out, end='')
        f.write(out)

f.close()
