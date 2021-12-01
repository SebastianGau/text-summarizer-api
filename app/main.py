from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

# Data Handling
import logging
from timeit import default_timer as timer
import os
import sys

# Server
from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from typing import List

# sumy
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk
nltk.download('punkt')

# intialize REST API using the FastAPI framework
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


@app.post("/summarize", response_model=SummarizeTextResponse)
def summarize(request: SummarizeTextRequest) -> SummarizeTextResponse:
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
        parser = HtmlParser.from_url(request.url, Tokenizer(request.language))
    else:
        raise ValueError('please specify text or url parameter in the request')

    for sentence in summarizer(parser.document, request.sentencecount):
        resp.summarizedtext = resp.summarizedtext + str(sentence)

    end = timer()
    resp.executiontime = end - start
    return resp


class HealthResponse(BaseModel):
    ok: bool = True


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    h = HealthResponse()
    h.ok = True
    return h


class RegisterFunctionRequest(BaseModel):
    pythoncode: str = ""
    functionid: int = 1


def store_function(functionid: int, pythoncode: str):
    file = open(str(functionid) + ".py", "a")
    file.write(pythoncode)
    file.close()


def load_function(functionid: int):
    sys.path.append(os.getcwd())
    function_module = __import__(str(functionid))
    if (not callable(function_module.invoke)):
        raise ValueError('invoke function is not callable or undefined')
    return function_module


def remove_function(id: int):
    os.remove(str(id) + ".py")


def invoke_function(id: int, arguments: List[str]):
    function_module = load_function(id)
    result = function_module.invoke(arguments)
    return result


@app.post("/registerfunction")
def registerfunction(request: RegisterFunctionRequest):
    store_function(request.functionid, request.pythoncode)
    try:
        load_function(request.functionid)
    except Exception as error:
        remove_function(request.functionid)
        raise HTTPException(status_code=404, detail=str(error))


class InvokeFunctionRequest(BaseModel):
    functionid: int = 1
    arguments: List[str] = []


class InvokeFunctionResponse(BaseModel):
    output: List[str] = ""


@app.post("/invokefunction", response_model=InvokeFunctionResponse)
def invokefunction(request: InvokeFunctionRequest) -> InvokeFunctionResponse:
    resp = InvokeFunctionResponse()
    try:
        resp.output = invoke_function(request.functionid, request.arguments)
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error))
    return resp


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
