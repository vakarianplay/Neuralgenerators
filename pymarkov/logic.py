# -*- coding: utf-8 -*-
import re, random

class ExitLoop(Exception):
    pass

class Stemmer:
    cacheLevel = 1
    cache = {}

    vovel = u"аеиоуыэюя"
    perfectiveground = u"((ив|ивши|ившись|ыв|ывши|ывшись)|((?<=[ая])(в|вши|вшись)))$"
    reflexive = u"(с[яь])$"
    adjective = u'(ее|ие|ые|ое|ими|ыми|ей|ий|ый|ой|ем|им|ым|ом|его|ого|ему|ому|их|ых|ую|юю|ая|яя|ою|ею)$';
    participle = u'((ивш|ывш|ующ)|((?<=[ая])(ем|нн|вш|ющ|щ)))$';
    verb = u'((ила|ыла|ена|ейте|уйте|ите|или|ыли|ей|уй|ил|ыл|им|ым|ен|ило|ыло|ено|ят|ует|уют|ит|ыт|ены|ить|ыть|ишь|ую|ю)|((?<=[ая])(ла|на|ете|йте|ли|й|л|ем|н|ло|но|ет|ют|ны|ть|ешь|нно)))$';
    noun = u'(а|ев|ов|ие|ье|е|иями|ями|ами|еи|ии|и|ией|ей|ой|ий|й|иям|ям|ием|ем|ам|ом|о|у|ах|иях|ях|ы|ь|ию|ью|ю|ия|ья|я)$';
    rvre = u'^(.*?[аеиоуыэюя])(.*)$';
    derivational = u'[^аеиоуыэюя][аеиоуыэюя]+[^аеиоуыэюя]+[аеиоуыэюя].*(?<=о)сть?$';

    def __init__(self, cache = 1):
        pass

    def s(self, pattern, repl,  str):
        return re.sub(pattern, repl, str) == str

    def stemWord(self,  word):
        word = word.lower().replace(u'ё', u'е')

        if self.cacheLevel and word in self.cache:
            return self.cache[word]

        stem = word

        try:
            matches = re.match(self.rvre, word)
            if not matches:
                raise ExitLoop()

            start,  RV = matches.groups()

            if not RV:
                raise ExitLoop()

            # Step 1
            if self.s(self.perfectiveground, '', RV):
                RV = re.sub(self.reflexive, '', RV)

                if not self.s(self.adjective, '', RV):
                    RV = re.sub(self.adjective, '', RV)
                    RV = re.sub(self.participle, '', RV)
                else:
                    if self.s(self.verb, '', RV):
                        RV = re.sub(self.noun, '', RV)
                    else:
                        RV = re.sub(self.verb, '', RV)
            else:
                RV = re.sub(self.perfectiveground, '', RV)

            # Step 2
            RV = re.sub(u'и$', '', RV)

            # Step 3
            if re.search(self.derivational, RV):
                RV = re.sub(u'ость?$', '', RV)

            # Step 4
            if self.s(u'ь$', '', RV):
                RV = re.sub(u'ейше?', '', RV)
                RV = re.sub(u'нн$', u'н', RV)
            else:
                RV = re.sub(u'ь$', '', RV)

            stem = start + RV
        except ExitLoop:
            pass

        if self.cacheLevel:
            self.cache[word] = stem

        return stem

class Markov:
    links = {}
    stemmer = Stemmer()
    useStemmer = True
    pair = 'Remove'

    def __init__(self):
        self.links[''] = []

    def normalize(self, word):
        word = word.strip(u',<>/:;"\'[]{}=+_)(*&^%$#@~`').lstrip(u'!?.')
        word = re.sub('[.?!]+$', '.', word)

        return word

    def load(self, text):
        sentences = re.split(u'\s*[\.\?!]+\s*', text)

        for sentence in sentences:
            if sentence == '':
                continue

            words = re.split(u'\s+', sentence+'.')
            wordsCount = len(words)

            self.links[''].append(words[0])

            for i in range(len(words)):
                stem = self.normalize(words[i])
                if self.useStemmer:
                    stem = self.stemmer.stemWord(stem)

                if stem not in self.links:
                    self.links[stem] = []

                if i+1 < wordsCount:
                    self.links[stem].append(words[i+1])
                else:
                    self.links[stem] = []


    def printLinks(self):
        for i in self.links:
            print ("'+i+'"), ("["),
            for j in self.links[i]:
                print ("'+j+'"),
            print ("]")


    def generate(self, num):
        word = random.choice(self.links[''])
        text = word

        for i in range(num-1):
            stem = self.normalize(word)
            if self.useStemmer:
                stem = self.stemmer.stemWord(stem)

            if stem in self.links and len(self.links[stem]) > 0:
                word = random.choice(self.links[stem])
            else:
                word = random.choice(self.links[''])

            text += " " + word

        if self.pair == 'Remove':
            text = re.sub('[\[\]{}"\'<>()]', '', text)
        return text;
