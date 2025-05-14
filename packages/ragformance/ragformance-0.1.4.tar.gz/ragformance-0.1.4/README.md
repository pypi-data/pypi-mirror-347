# RAGFORmance
Benchmark for RAG

# Usage

## Using test suite with BEIR datasets 

``` python
from ragformance.scripts.RAG_abstractions.naive_rag import upload_corpus, ask_queries
from ragformance.eval.utils.beir_dataloader import load_beir_dataset

from ragformance.eval.metrics import trec_eval_metrics
from ragformance.eval.metrics import visualize_semantic_F1, display_semantic_quadrants

import logging

logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

corpus, queries = load_beir_dataset(filter_corpus = True)

upload_corpus(corpus)
ask_queries(queries[:10])

metrics = trec_eval_metrics(answers)

quadrants = visualize_semantic_F1(corpus, answers)

display_semantic_quadrants(quadrants)

```

## Example configuration file

``` json
{
    "corpus_text_key": "text"
}


```
