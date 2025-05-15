__author__ = 'danilo@jaist.ac.jp'

from typing import List, Self

from .annotable import Annotable
from .token import Token


class Sequence(Annotable):
    """Description of a sequence.

    Attributes:
    tokens (list of Token): Sequence of tokens composing the sequence, in reading order.
    annotations (dict): [optional] Sequence level annotations, identified by the dictionary key.
        Examples: sequence type, batch / sample identifier, sequence-level vectors.
    """

    def __init__(self):
        super(Sequence, self).__init__()
        self.tokens: List[Token] = []

    @classmethod
    def from_dict(cls, obj: dict) -> Self:
        seq = cls()
        if ("annotations") in obj:
            seq.annotations = obj["annotations"]

        if ("tokens" in obj):
            for surf, annot in zip(obj["tokens"]["surface"], obj["tokens"]["annotations"]):
                token = Token()
                token.surface = surf
                token.annotations = annot
                seq.tokens.append(token)

        return seq

    def to_dict(self) -> dict:
        obj = dict()
        if (self.annotations):
            obj["annotations"] = self.annotations

        if (self.tokens):
            obj["tokens"] = {
                "surface": [tok.surface for tok in self.tokens],
                "annotations": [tok.annotations for tok in self.tokens]
            }

        return obj
