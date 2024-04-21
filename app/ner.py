import spacy
from natasha import (
    Segmenter,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    MorphVocab,
    Doc
)

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()

morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)

def normalize(text):
    doc = Doc(text)

    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)

    for token in doc.tokens:
        token.lemmatize(morph_vocab)
        
    return ' '.join(x.lemma for x in doc.tokens)


model = spacy.load('ru_core_news_lg')


def ner(text):
    result = {'PER': [], 'ORG': [], 'LOC': []}

    for ent in model(text).ents:
        if ent.label_ == 'LOC':
            result[ent.label_] += [ent.text]
        else:
            result[ent.label_] += [normalize(ent.text)]
    
    return result
