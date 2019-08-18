import operator
import socket

from lib.score import Score
from nltk.stem import PorterStemmer
from joblib import Parallel, delayed

PS = PorterStemmer()
STOPWORDS = {'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than'}
HTTP = 'http://'
class Generate():
    def __init__(self,name):
        self.common_ext = [
            '.com',
            '.org',
            '.net',
            '.co',
            '.in',
            '.edu'
        ]
        self.name = name

    def get_valid_urls(self,urls):
        valid_urls = []
        for url in urls:
            try:
                socket.gethostbyname(url)
            except Exception :
                continue
            valid_urls.append(HTTP + url)
        return valid_urls

    def abbrvtions(self,names):
        names_list = []
        n = len(names)
        names_list.append(names[0][0] + ''.join(names[1:n]))
        names_list.append(''.join(names[0:n-1]) + names[n-1][0])
        for i in range(1,n-1):
            s = ''.join(names[0:i-1]) + names[i][0] + ''.join(names[i+1:n])
            names_list.append(s)
        return names_list

    def short_form(self,names):
        names_list = []
        n = len(names)
        names_list.append(PS.stem(names[0]) + ''.join(names[1:n]))
        names_list.append(''.join(names[0: n - 1]) + PS.stem(names[n - 1]))
        for i in range(1, n - 1):
            s = ''.join(names[0:i - 1]) + PS.stem(names[i]) + ''.join(names[i + 1:n])
            names_list.append(s)
        return names_list

    def pairs(self,names):
        names_list = []
        n = len(names)
        names_list.append(''.join(names[1:n]))
        names_list.append(''.join(names[0:n-1]))
        for i in range(1,n-1):
            s = ''.join(names[0:i]) + ''.join(names[i+1:n])
            names_list.append(s)
        return names_list

    def comb_names(self):
        names_list = []
        name = self.name.split()
        names_list.append(''.join(name))
        names_temp = [i for i in name if i not in STOPWORDS]
        names_list.extend(self.abbrvtions(names_temp))
        names_list.extend(self.short_form(names_temp))
        names_list.extend(self.pairs(names_temp))
        return names_list

    def get_urls(self):
        size = len(self.name.split())
        if size == 1: names_list = [self.name]
        else: names_list = list(set(self.comb_names()))
        url_list = []
        for one_name in names_list:
            temp = [one_name + ext for ext in self.common_ext]
            url_list.extend(temp)
        valid_urls = self.get_valid_urls(url_list)
        return valid_urls

    def get_predicted_url(self, valid_urls):
        scores = {}
        #print('valid urls', valid_urls)
        n_jobs = len(valid_urls)
        if not n_jobs: return (0,"No possible url")
        scores = Parallel(n_jobs = n_jobs, verbose = 5)\
                        (delayed(Score(url, self.name, STOPWORDS).get_score)() for url in valid_urls)
        scores.sort(key = operator.itemgetter(0), reverse = True)
        #print scores
        return scores[0]

    def get(self):
        valid_urls = self.get_urls()
        return self.get_predicted_url(valid_urls)