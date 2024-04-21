import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop = stopwords.words('russian')

from string import punctuation
punkt= [p for p in punctuation] + ["`", "``" ,"''", "'"]

import fasttext
import pymorphy2
from fasttext.FastText import _FastText

lemmatizer = pymorphy2.MorphAnalyzer(path='/home/ubuntu/hack/pymorphy2-dicts-ru-2.4.404381.4453942/pymorphy2_dicts_ru/data', lang='ru')


def tokenize(sent):
    try:
        sent = word_tokenize(sent)
        return [word for word in sent if word not in stop and word not in punkt]
    except:
        return []
    

def lemmatize(sent):
    try:
        return " ".join([lemmatizer.normal_forms(word)[0] for word in sent])
    except:
        return " "


def preprocess_sent(sent):
    return lemmatize(tokenize(sent))


model_path = '/home/ubuntu/hack/optimized.model' # процесс обучения можно найти в vk-hse-classifier.ipynb
ft_model = _FastText(model_path=model_path)


def get_tag(text):
    result = ft_model.predict(preprocess_sent(text), k=1)[0][0].split('__')[2]
    return result
