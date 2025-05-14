# RAGFORmance
Benchmark for RAG

# Usage

## Using test suite with BEIR datasets 

``` python
from ragformance.scripts.RAG_abstractions.naive_rag import upload_corpus, ask_queries
from ragformance.eval.utils.beir_dataloader import load_beir_dataset

import logging

logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

corpus, queries = load_beir_dataset(filter_corpus = True)

upload_corpus(corpus)
ask_queries(queries[:10])

```

## Example configuration file

``` json
{
    "corpus_text_key": "text"
}


```
