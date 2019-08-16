import requests

from bs4 import BeautifulSoup
from difflib import SequenceMatcher

class Score:

    def __init__(self, url, name,stop_words):
        self.url = url
        self.name = name
        self.stop_words = stop_words

    def get_title(self, content):
        try:
            title = content.title.string
            return title.lower()
        except Exception:
            return ''

    def check_name(self, content):
        if not content: return 0
        for text in content.stripped_strings:
            if self.url == 'http://atom.org':
                print text
            if self.name in text.lower():
                return 1
        return 0

    def get_content(self):
        try:
            html = requests.get(self.url)
            soup = BeautifulSoup(html.content, 'html.parser')
            return soup
        except Exception:
            return None

    @staticmethod
    def similarity(word1, word2):
        return SequenceMatcher(None, word1, word2).ratio()

    def get_score_helper(self, title):
        names = self.name.split()
        score = -1
        names = [w for w in names if not w in self.stop_words]
        for name in names: score = max(score, self.similarity(name, title))
        return (score,self.url)

    def get_score(self):
        content = self.get_content()
        title = self.get_title(content)
        name_exists = self.check_name(content)
        if name_exists: return (1.0,self.url)
        return self.get_score_helper(title)

