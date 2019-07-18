from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as sen_plt


class SentimentAnalyzer(object):

    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        self.labels = ['negative', 'neutral', 'positive']
        self.explode = (0.1, 0, 0)
        self.colors = ['gold', 'yellowgreen', 'lightcoral',]

    def _generate_scores(self, text):
        return self.analyzer.polarity_scores(text)

    def generate_sentiment_graph(self, text, filename):
        score = self._generate_scores(text)
        sizes = [score['neg'], score['neu'], score['pos']]
        sen_plt.pie(sizes,explode=self.explode,labels=self.labels,colors=self.colors, autopct='%1.1f%%', shadow=True, startangle=140)
        sen_plt.axis('equal')
        #circle=sen_plt.Circle( (0,0), 0.7, color='white')
        #p = sen_plt.gcf()
        #p.gca().add_artist(circle)
        sen_plt.savefig(filename)