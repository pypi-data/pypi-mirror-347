# langchain-predictionguard

This page covers how to use the Prediction Guard ecosystem within LangChain.
It is broken into two parts: installation and setup, and then references to specific Prediction Guard wrappers.

## Installation and Setup

- Install the PredictionGuard Langchain partner package:
```
pip install langchain-predictionguard
```

- Get a Prediction Guard API key (as described [here](https://docs.predictionguard.com/)) and set it as an environment variable (`PREDICTIONGUARD_API_KEY`)

## Prediction Guard Langchain Integrations
|API|Description|Endpoint Docs| Import                                                  | Example Usage                                                                 |
|---|---|---|---------------------------------------------------------|-------------------------------------------------------------------------------|
|Chat|Build Chat Bots|[Chat](https://docs.predictionguard.com/api-reference/api-reference/chat-completions)| `from langchain_predictionguard import ChatPredictionGuard` | [ChatPredictionGuard.ipynb](/notebooks/ChatPredictionGuard.ipynb)             |
|Completions|Generate Text|[Completions](https://docs.predictionguard.com/api-reference/api-reference/completions)| `from langchain_predictionguard import PredictionGuard` | [PredictionGuard.ipynb](/notebooks/PredictionGuard.ipynb)                     |
|Text Embedding|Embed String to Vectores|[Embeddings](https://docs.predictionguard.com/api-reference/api-reference/embeddings)| `from langchain_predictionguard import PredictionGuardEmbeddings` | [PredictionGuardEmbeddings.ipynb](/notebooks/PredictionGuardEmbeddings.ipynb) |

## Getting Started

## Chat Models

### Prediction Guard Chat

See a [usage example](/notebooks/ChatPredictionGuard.ipynb)

```python
from langchain_predictionguard import ChatPredictionGuard
```

#### Usage

```python
# If predictionguard_api_key is not passed, default behavior is to use the `PREDICTIONGUARD_API_KEY` environment variable.
chat = ChatPredictionGuard(model="Hermes-3-Llama-3.1-8B")

chat.invoke("Tell me a joke")
```

## Embedding Models

### Prediction Guard Embeddings

See a [usage example](/notebooks/PredictionGuardEmbeddings.ipynb)

```python
from langchain_predictionguard import PredictionGuardEmbeddings
```

#### Usage
```python
# If predictionguard_api_key is not passed, default behavior is to use the `PREDICTIONGUARD_API_KEY` environment variable.
embeddings = PredictionGuardEmbeddings(model="bridgetower-large-itm-mlm-itc")

text = "This is an embedding example."
output = embeddings.embed_query(text)
```

## LLMs

### Prediction Guard LLM

See a [usage example](/notebooks/PredictionGuard.ipynb)

```python
from langchain_predictionguard import PredictionGuard
```

#### Usage
```python
# If predictionguard_api_key is not passed, default behavior is to use the `PREDICTIONGUARD_API_KEY` environment variable.
llm = PredictionGuard(model="Hermes-2-Pro-Llama-3-8B")

llm.invoke("Tell me a joke about bears")
```