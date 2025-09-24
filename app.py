# app.py
import streamlit as st
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


nlp = spacy.load("en_core_web_sm")

def summarize_text(text, num_sentences=3):
    doc = nlp(text)
    word_frequencies = {}
    
    for word in doc:
        if word.text.lower() not in STOP_WORDS and word.text.lower() not in punctuation:
            if word.text.lower() not in word_frequencies:
                word_frequencies[word.text.lower()] = 1
            else:
                word_frequencies[word.text.lower()] += 1
    
    max_freq = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] = word_frequencies[word] / max_freq

    sentence_scores = {}
    for sent in doc.sents:
        for word in sent:
            if word.text.lower() in word_frequencies:
                if sent not in sentence_scores:
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
    
    summary = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    final_summary = ' '.join([sent.text for sent in summary])
    return final_summary


st.title("Chota Don")
text_input = st.text_area("Enter text to summarize:", height=300)
num_sentences = st.slider("Number of sentences in summary:", min_value=1, max_value=10, value=3)

if st.button("Summarize"):
    if text_input.strip():
        summary = summarize_text(text_input, num_sentences)
        st.subheader("Summary:")
        st.write(summary)
    else:
        st.warning("Please enter some text.")
