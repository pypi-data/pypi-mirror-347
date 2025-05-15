__author__ = 'Danilo S. Carvalho <danilo@jaist.ac.jp>'

from typing import Tuple, List, Union
from saf.data_model.document import Document
from saf.data_model.sentence import Sentence
from saf.data_model.token import Token
from .importer import Importer


class ListImporter(Importer):
    """Importer class for converting a list of tokenized sentences with optional annotations into an Annotable document.

    The expected format is a list of tokenized sentences, each sentence being a
    list of tuples (token, label_1, label_2, ...) where the labels are optional and correspond to the listed
    annotation fields in their respective order.

        Args:
            annotations (list of str): list of keys identifying the annotation fields in the sentence list, in the order they will appear with each token.
                Default keys can be found in the constants.annotation module.
                Example: ["POS", "DEP", ...]
        """
    def __init__(self, annotations: List[str] = None):
        super(ListImporter, self).__init__(None, None)
        self.annotations = annotations

    def import_document(self, document: List[List[Union[str, Tuple[str, ...]]]]) -> Document:
        """Imports a list of tokenized sentences with optional annotations.

        Args:
            document (List[List[Union[str, Tuple[str, ...]]]]): A list of tokenized sentences, each sentence being a
            list of tuples (token, label_1, label_2, ...) where the labels are optional and correspond to the listed
            annotation fields in their respective order.

        Returns: The imported document.

        """
        doc = Document()

        for sent in document:
            sentence = Sentence()

            for token_raw in sent:
                token = Token()
                if (isinstance(token_raw, str)):
                    token.surface = token_raw
                else:
                    token.surface = token_raw[0]
                    for i, annot in enumerate(self.annotations):
                        token.annotations[annot] = token_raw[i + 1]

                sentence.tokens.append(token)

            sentence._surface = " ".join([tok.surface for tok in sentence.tokens])
            doc.sentences.append(sentence)

        return doc
