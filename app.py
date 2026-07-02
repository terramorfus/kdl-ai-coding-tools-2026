import streamlit as st
import nltk
import spacy
from gensim.models.phrases import Phrases, Phraser
from gensim.utils import simple_preprocess
from collections import defaultdict
import pandas as pd
import plotly.express as px
import math
import os

nltk.download('stopwords', quiet=True)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

@st.cache_resource
def load_nlp_model():
    try:
        return spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    except OSError:
        import spacy.cli
        spacy.cli.download('en_core_web_sm')
        return spacy.load('en_core_web_sm', disable=['parser', 'ner'])

@st.cache_resource
def load_stop_words(stop_language):
    from nltk.corpus import stopwords
    stop_words = []
    stop_words.extend(stopwords.words(stop_language))
    stop_words.extend(['would', 'said', 'says', 'also', 'good', 'lord',
                       'come', 'let', 'say', 'speak', 'know', 'hamlet'])
    stop_file = os.path.join(DATA_DIR, 'earlyModernStopword.txt')
    if os.path.exists(stop_file):
        with open(stop_file, 'r', encoding='utf-8') as f:
            for line in f:
                stop_words.append(line.strip())
    return set(stop_words)

def make_trigrams(tokens, min_count, threshold):
    bigram = Phrases(tokens, min_count=min_count, threshold=threshold)
    bigram_model = Phraser(bigram)
    trigram = Phrases(bigram[tokens], threshold=threshold)
    trigram_model = Phraser(trigram)
    result = []
    for doc in tokens:
        bigram_result = bigram_model[doc]
        trigram_result = trigram_model[bigram_result]
        result.append(trigram_result)
    return result

def make_lemma(tokens, nlp, min_count, threshold):
    data_ngrams = make_trigrams(tokens, min_count, threshold)
    texts_out = []
    for sent in data_ngrams:
        doc = nlp(' '.join(sent))
        texts_out.append([token.lemma_ for token in doc if token.lemma_ != '-PRON-'])
    return texts_out

def process_text(text, stop_language, min_count, threshold, nlp):
    stop_words = load_stop_words(stop_language)
    docs = []
    for line in text.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        docs.append(line.split())
    if not docs:
        return None
    words = [simple_preprocess(str(s), deacc=True) for s in docs]
    cleaned = []
    for doc in words:
        processed = [w for w in simple_preprocess(str(doc)) if w not in stop_words]
        if processed:
            cleaned.append(processed)
    if not cleaned:
        return None
    lemma = make_lemma(cleaned, nlp, min_count, threshold)
    tokens = [item for sublist in lemma for item in sublist]
    freq = defaultdict(int)
    for t in tokens:
        freq[t] += 1
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return sorted_freq

st.set_page_config(page_title='Text Word Frequency Analyser', layout='centered')
st.title('Text Word Frequency Analyser')
st.markdown('Upload a text file to see a visualisation of the most frequent words.')

uploaded_file = st.file_uploader('Choose a text file', type=['txt'])

with st.sidebar:
    st.header('Settings')
    stop_language = st.selectbox('Stop word language', ['english'], index=0)
    top_n = st.slider('Number of top words', min_value=5, max_value=50, value=10)
    min_count = st.number_input('Min n-gram count', min_value=1, max_value=20, value=5)
    threshold = st.number_input('N-gram threshold', min_value=1, max_value=500, value=100)
    run_button = st.button('Run Analysis')

if uploaded_file is not None and run_button:
    text = uploaded_file.read().decode('utf-8', errors='ignore')
    with st.spinner('Processing text...'):
        nlp = load_nlp_model()
        freq = process_text(text, stop_language, min_count, threshold, nlp)
    if freq is None:
        st.warning('No words remained after filtering. Try adjusting the settings.')
    else:
        df = pd.DataFrame(freq[:top_n], columns=['Word', 'Count'])
        df['Pct'] = ((df['Count'] / df['Count'].sum()) * 100).round(3).astype(str) + '%'
        fig = px.bar(df, x='Word', y='Count', hover_data=[df['Pct']],
                     text='Count', color='Word',
                     title=f'Top {top_n} Words',
                     color_discrete_sequence=px.colors.qualitative.Dark24)
        fig.update_layout(
            title={'y': 0.90, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
            width=750, height=550, showlegend=False)
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        with st.expander('Show raw data'):
            st.dataframe(df)

st.markdown('---')
st.markdown('Built with Streamlit, NLTK, Gensim, spaCy, and Plotly.')
