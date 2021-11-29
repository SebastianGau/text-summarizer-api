from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

# Data Handling
import logging
from timeit import default_timer as timer

# Server
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

# Modeling
import os

# sumy
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk
nltk.download('punkt')

os.environ["PORT"] = "5000"
app = FastAPI()


# Initialize logging
my_logger = logging.getLogger()
my_logger.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG, filename='sample.log')


class SummarizeTextRequest(BaseModel):
    text: str = ""
    url: str = ""
    language: str = ""
    sentencecount: int = 10


class SummarizeTextResponse(BaseModel):
    summarizedtext: str = ""
    executiontime: float = 0


class HealthResponse(BaseModel):
    ok: bool = True


@app.post("/summarize", response_model=SummarizeTextResponse)
def invoke(request: SummarizeTextRequest) -> SummarizeTextResponse:
    my_logger.info("invocation starting")
    resp = SummarizeTextResponse()
    start = timer()

    # prepare text summary
    stemmer = Stemmer(request.language)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(request.language)
    
    if request.text:
        parser = PlaintextParser.from_string(request.text, Tokenizer(request.language))
    elif request.url:
        parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    else:
        raise ValueError('please specify text or url parameter in the request')
    

    for sentence in summarizer(parser.document, request.sentencecount):
        print(sentence)
        resp.summarizedtext = resp.summarizedtext + str(sentence)

    end = timer()
    resp.executiontime = end - start
    return resp


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    h = HealthResponse()
    h.ok = True
    return h


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
