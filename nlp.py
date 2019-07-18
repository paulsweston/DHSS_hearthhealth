import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from wordcloud import WordCloud,STOPWORDS
from matplotlib import figure
import matplotlib.pyplot as plt


class LanguageProcessor(object):
    def __init__(self):
        self.downloadpath = './nltk_data'
        nltk.data.path.append(self.downloadpath)
        self._init_nltk_packages()

    def _init_nltk_packages(self):
        nltk.download('punkt', download_dir=self.downloadpath)
        nltk.download('stopwords', download_dir=self.downloadpath)
        nltk.download('averaged_perceptron_tagger', download_dir=self.downloadpath)

    def generate_word_cloud(self, document, filepath):
        sentences = nltk.sent_tokenize(document)
        stopWords = set(stopwords.words('english'))
        ps = PorterStemmer()

        data = []
        wordsFiltered = []
        for sent in sentences:
            data = data + nltk.pos_tag(nltk.word_tokenize(sent))

        for word in data:
            if word[0] not in stopWords:
                if ('.' not in word[1]) and ('!' not in word[1]) and not word[1].startswith('@') and not word[1].startswith('#') and not word[1].startswith('.')and not word[1].startswith("'") and not word[1].startswith(','):
                    wordsFiltered.append(ps.stem(word[0]))

        self._save_word_cloud(wordsFiltered, filepath, 'white')



    def _save_word_cloud(self, data, filepath, color='black'):
        fdist = nltk.FreqDist(data)

        word_dict={}
        for word, frequency in fdist.most_common(50):
            word_dict[word]=frequency
        wordcloud = WordCloud(stopwords=STOPWORDS,
                        background_color=color,
                        width=2500,
                        height=2000
                        )
        wordcloud.fit_words(word_dict)
        f = figure.Figure( figsize =(7,7) )
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.show()
        wordcloud.to_file(filepath)

