from wordcloud import WordCloud 
import matplotlib.pyplot as plt 
import yake
import streamlit as st
import io

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

from ner import normalize

russian_stopwords = stopwords.words('russian')
stopwords = set(russian_stopwords + ['также', 'однако', 'это', 'словам', 'кроме', 'Также', 'Однако', 'Это', 'Словам', 'Кроме'])

yake_kw = yake.KeywordExtractor() 


def show_keywords_cloud(text):
    
    KeyWords = yake_kw.extract_keywords(text) 
    keywords = set([normalize(kw) for kw, _ in KeyWords])
    
    wordcloud = WordCloud(width = 400, height = 400,
                    background_color ='white',
                    stopwords = stopwords,
                    min_font_size = 10).generate(' '.join(keywords))
                        
    plt.figure(figsize = (4, 4), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight', pad_inches=0)
    img_buffer.seek(0)
    
    st.image(img_buffer, caption='Облако ключевых слов')


def get_keywords(text):
    KeyWords = yake_kw.extract_keywords(text) 
    keywords = [kw for kw, _ in KeyWords]

    return ' '.join(keywords[:1])
