# -*- coding: utf-8 -*-
import afilter, re, math
from collections import Counter


def bing(results, alt, lang="sv-SE"):
    # If not an array, it should be transformed into one
    if not isinstance(results, list):
        results = [results]
    if not isinstance(alt, list):
        alt = [alt]

    # First check
    for a in alt:

        text = a.content[lang.split('-')[0]]
        pointValue = 100
        hits = 0
        points = 0

        for result in results:
            hits += get_hits(result['webPages']['value'], text)
            points += get_points(result['webPages']['value'], text, pointValue)

        a.pointify['hits'] = hits
        a.pointify['points'] = points

    if all(a.pointify['hits'] == 0 for a in alt):
        for a in alt:

            text = a.content[lang.split('-')[0]]

            pointValue = 80
            hits = 0
            points = 0
            # Filter out functional words and remove special characters
            words = afilter.rm_fwords(text, lang.split('-')[0]).split(' ')

            for result in results:
                for word in words:
                    hits += get_hits(result['webPages']['value'], word)
                    points += get_points(result['webPages']['value'], word, pointValue)

            a.pointify['hits'] = hits
            a.pointify['points'] = (points / len(words))

    return alt

def bingReverse(results, words):
    # If not an array, it should be transformed into one
    if not isinstance(results, list):
        results = [results]
    if not isinstance(words, list):
        words = [words]
    points = {}

    # First check
    pointValue = 100
    for word in words:
        i = 0
        for result in results:
            i += get_hits(result['webPages']['value'], word)
            points[word] = i * pointValue

    return points

def get_hits(pages, text):
    hits = 0
    text = re.sub('\W+',' ', text).strip().lower()
    for page in pages:
        page['name'] = re.sub('\W+', ' ', page['name']).strip().lower()
        page['snippet'] = re.sub('\W+', ' ', page['snippet']).strip().lower()

        title_hits = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(text), page['name']))
        snippet_hits = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(text), page['snippet']))
        hits += title_hits+snippet_hits
    return hits

def get_points(pages, text, pointValue):
    points = 0
    text = re.sub('\W+',' ', text).strip().lower()
    for page in pages:
        page['name'] = re.sub('\W+', ' ', page['name']).strip().lower()
        page['snippet'] = re.sub('\W+', ' ', page['snippet']).strip().lower()

        title_hits = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(text), page['name']))
        snippet_hits = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(text), page['snippet']))

        points += (title_hits+snippet_hits)*pointValue
        pointValue = pointValue-2

    return points

# Todo make real
def nbd(hits_term1, hits_term2, hits_combined, hits_the):
    lhits1 = math.log10(hits_term1)
    lhits2 = math.log10(hits_term2)
    lhits_mix = math.log10(hits_combined)
    npages = hits_the
    fix = 1000

    lN = math.log10(npages * fix)
    numerator = max([lhits1, lhits2]) - lhits_mix
    denomin = lN - min([lhits1, lhits2])

    return numerator / denomin


# Answer search - Question words split check
    '''
    for answer in answers:
        searches['answers'].append(bing.search(answer, lang))

    if all(value == 0 for value in points.values()):
        i = 0
        test = {}
        for search in searches['answers']:
            words = afilter.rm_fwords(question, lang.split('-')[0]).split(' ')
            for word in words:
                i += check_occurences(search, word)
            points[search['queryContext']['originalQuery']] = i/100

    #Return dict with answer and i
    '''