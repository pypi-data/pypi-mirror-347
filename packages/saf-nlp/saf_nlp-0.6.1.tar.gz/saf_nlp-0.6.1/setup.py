import os
from distutils.core import setup

PKG_ROOT = os.path.abspath(os.path.dirname(__file__))


def load_requirements() -> list:
    """Load requirements from file, parse them as a Python list"""

    with open(os.path.join(PKG_ROOT, "requirements.txt"), encoding="utf-8") as f:
        all_reqs = f.read().split("\n")
    install_requires = [str(x).strip() for x in all_reqs]

    return install_requires

setup(
    name='saf-nlp',
    version='0.6.1',
    packages=['saf', 'saf.test', 'saf.constants', 'saf.importers', 'saf.importers.tokenizers', 'saf.annotators',
              'saf.data_model', 'saf.formatters'],
    url='',
    license='',
    author=['Danilo S. Carvalho', 'Vu Duc Tran'],
    author_email=['danilo.carvalho@manchester.ac.uk', 'vu.tran@jaist.ac.jp'],
    description='Simple Annotation Framework',
    install_requires=load_requirements()
)
