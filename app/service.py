import streamlit as st
from ner import ner
from sentiment import sentiment
from tag_prediction import get_tag
from keywords_wordcloud import show_keywords_cloud
from summarization import summarize
from parser import parse

def get_answer(text):
    
    tag = get_tag(text)
    st.info(f'Категория: {tag}')

    summarization = summarize(text, n_words=10)  
    st.info(f'Суммаризация : {summarization}')

    sentiment_result = sentiment(text)
    st.info(f'Тональность: {sentiment_result}')

    ner_results = ner(text)
    PER = set([res.title() for res in ner_results['PER']])
    LOC = set([res.title() for res in ner_results['LOC']])
    ORG = set([res.upper() for res in ner_results['ORG'] if res not in LOC])
    LOC = [x for x in LOC if x not in ORG]

    if PER:
        pers = ', '.join(PER)
        st.info(f'Люди: {pers}')

    if LOC:
        locs = ', '.join(LOC)
        st.info(f'Места: {locs}')
                
    if ORG:
        orgs = ', '.join(ORG)
        st.info(f'Организации и компании: {orgs}')

    show_keywords_cloud(text)

st.set_page_config(
    page_title='Классификатор новостей',
    page_icon=':news:',
    layout='wide'
)

with st.container():
    st.sidebar.title("Параметры")
    st.title("Классификатор новостей")

    method = st.radio(
        "Выберите режим:",
        ["Ввести текст новости", "Ввести ссылку на news.mail.ru"],
        index=0,
        )

    if method == 'Ввести текст новости':
        with st.form('my_form'):
            text = st.text_area('Введите новость:', '')
            submitted = st.form_submit_button('Submit')
            if submitted:
                get_answer(text)

    else:
        with st.form('my_form'):
            link = st.text_area('Введите ссылку на news.mail.ru:', '')
            submitted = st.form_submit_button('Submit')
            if submitted:
                if 'mail.ru' in link:
                        text = parse(link)
                        if text == 'До связи':
                            st.info('Не удалось спарсить')
                        else:
                            get_answer(text)
                else:
                    st.info('Ссылка должна быть на news.mail.ru')
            
    st.sidebar.info("Решение команды MISIS DEMIDOVICH\n"
            "[Репозиторий GitHub](https://github.com/l1ghtsource/vk-hse-hack-news-classification).")
