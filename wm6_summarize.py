from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

import nltk
nltk.download('punkt')
nltk.download('stopwords')

def process_summarize(sIn):
    if sIn != "" and not(sIn is None):
        summarizer = LsaSummarizer()
        parser = PlaintextParser.from_string(sIn, Tokenizer("russian"))
        summarized_text = summarizer(parser.document, sentences_count=10)  # Меняем число предложений
        return "\n".join(str(sentence) for sentence in summarized_text)
    return 'Необходимо заполнить поле стенограмма'
