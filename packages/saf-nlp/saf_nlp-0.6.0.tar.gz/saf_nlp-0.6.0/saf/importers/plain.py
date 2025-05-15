__author__ = 'Danilo S. Carvalho <danilo@jaist.ac.jp>, Vu Duc Tran <vu.tran@jaist.ac.jp>'

from saf.data_model.document import Document
from saf.data_model.sentence import Sentence
from saf.data_model.token import Token
from nltk.tokenize import sent_tokenize, word_tokenize
from .importer import Importer


class PlainTextImporter(Importer):
    def __init__(self, sentence_tokenizer=sent_tokenize, word_tokenizer=word_tokenize):
        super().__init__(sentence_tokenizer, word_tokenizer)

    def import_document(self, document):
        doc = Document()

        sentences_raw = self.sent_tokenizer(document)
        if (sentences_raw[0] == document):
            sentences_raw = document.split("\n")

        for sent_raw in sentences_raw:
            tokens_raw = self.word_tokenizer(sent_raw)

            sentence = Sentence()

            for token_raw in tokens_raw:
                token = Token()
                token.surface = token_raw
                sentence.tokens.append(token)

            sentence._surface = " ".join([tok.surface for tok in sentence.tokens])
            doc.sentences.append(sentence)

        return doc
