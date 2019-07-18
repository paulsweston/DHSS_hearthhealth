import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import state_union
from wordcloud import WordCloud,STOPWORDS
from matplotlib import figure
import matplotlib.pyplot as plt



 

document = 'Today the Netherlands celebrates King\'s Day. To honor this tradition, the Dutch embassy in San Francisco invited me to.All work and no play makes jack dull boy. All work and no play makes jack a dull boy."'
sentences = nltk.sent_tokenize(document) 
stopWords = set(stopwords.words('english'))  
ps = PorterStemmer()
 
data = []
wordsFiltered = []
for sent in sentences:
    data = data + nltk.pos_tag(nltk.word_tokenize(sent))
 
for word in data: 
     if word[0] not in stopWords:  
         if ('.' not in word[1]) or ('!' not in word[1]) :
            wordsFiltered.append(ps.stem(word[0]))

print(wordsFiltered)

def wordcloud_draw(data, color = 'black'):
    words = ' '.join(data)
    cleaned_word = " ".join([word for word in words.split()
                            if 'http' not in word
                                and not word.startswith('@')
                                and not word.startswith('#')
                                and not word.startswith('.')
                                and not word.startswith("'")
                                and not word.startswith(',')
                                and word != 'RT'
                            ])
    wordcloud = WordCloud(stopwords=STOPWORDS,
                      background_color=color,
                      width=2500,
                      height=2000
                     ).generate(cleaned_word)
    f = figure.Figure( figsize =(7,7) )
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
    wordcloud.to_file('N.png')
 
wordcloud_draw(wordsFiltered,'white')

