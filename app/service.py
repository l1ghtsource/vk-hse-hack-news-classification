import streamlit as st
from ner import ner
from sentiment import sentiment
from tag_prediction import get_tag

def get_answer(text):
    
    tag = get_tag(text)
    st.info(f'Категория: {tag}')

    keywords = 'слова, слова, слова'    
    st.info(f'Ключевые слова: {keywords}')

    sentiment_result = sentiment(text)
    st.info(f'Тональность: {sentiment_result}')

    ner_results = ner(text)
    PER = ner_results['PER']
    LOC = ner_results['LOC']
    ORG = ner_results['ORG']

    if PER:
        pers = ', '.join(PER)
        st.info(f'Люди: {pers}')

    if LOC:
        locs = ', '.join(LOC)
        st.info(f'Места: {locs}')
                
    if ORG:
        orgs = ', '.join(ORG)
        st.info(f'Организации и компании: {orgs}')

st.set_page_config(
    page_title='Классификатор новостей',
    page_icon=':paper:',
    layout='wide'
)

with st.container():
    st.sidebar.title("Параметры")
    st.title("Классификатор новостей")

    with st.form('my_form'):
        text = st.text_area('Введите новость:', '')
        submitted = st.form_submit_button('Submit')
        if submitted:
            get_answer(text)
        
    st.sidebar.info("Решение команды MISIS DEMIDOVICH\n"
            "[Репозиторий GitHub](https://github.com/l1ghtsource/).")
