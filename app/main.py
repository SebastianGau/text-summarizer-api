from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

# Data Handling
import logging

# Server
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel


# intialize REST API using the FastAPI framework
app = FastAPI()

# Initialize logging
my_logger = logging.getLogger()
my_logger.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG, filename='sample.log')


class HealthResponse(BaseModel):
    ok: bool = True


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    h = HealthResponse()
    h.ok = True
    return h


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
