# -*- coding: utf-8 -*-

def rm_fwords(texts, lang="sv"):
    # If texts is not an array, it should be transformed into one
    if not isinstance(texts, list):
        texts = [texts]

    wordlist = open('dict/fwords-'+lang+'.txt', 'r').readlines()
    wordlist = set(([x.strip().lower() for x in wordlist]))

    filteredText = []
    for text in texts:
        final_list = [word for word in text.lower().split() if word not in wordlist]
        final_string = ' '.join(final_list)
        filteredText.append(final_string)

    if len(filteredText) == 1:
        filteredText = filteredText[0]

    return filteredText

def rm_cwords(texts, lang="sv"):
    # If texts is not an array, it should be transformed into one
    if not isinstance(texts, list):
        texts = [texts]

    wordlist = open('dict/cwords-'+lang+'.txt', 'r').readlines()
    wordlist = set(([x.strip() for x in wordlist]))

    filteredText = []
    for text in texts:
        final_list = [word for word in text.lower().split() if word not in wordlist]
        final_string = ' '.join(final_list)
        filteredText.append(final_string)

    if len(filteredText) == 1:
        filteredText = filteredText[0]

    return filteredText