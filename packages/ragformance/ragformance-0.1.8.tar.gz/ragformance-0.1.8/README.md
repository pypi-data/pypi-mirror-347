# RAGFORmance

[![Build status](https://github.com/FOR-sight-ai/RAGFORmance/actions/workflows/publish.yml/badge.svg?branch=main)](https://github.com/FOR-sight-ai/ragformance/actions)
[![Docs status](https://img.shields.io/readthedocs/RAGFORmance)](TODO)
[![Version](https://img.shields.io/pypi/v/ragformance?color=blue)](https://pypi.org/project/ragformance/)
[![Python Version](https://img.shields.io/pypi/pyversions/ragformance.svg?color=blue)](https://pypi.org/project/ragformance/)
[![Downloads](https://static.pepy.tech/badge/ragformance)](https://pepy.tech/project/ragformance)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/FOR-sight-ai/ragformance/blob/main/LICENSE)

  <!-- Link to the documentation -->
  <a href="TODO"><strong>Explore RAGFORmance docs »</strong></a>
  <br>

</div>

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
answers = ask_queries(queries[:10])

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


## Contributing

Contributions to the Forcolate library are welcome! If you have ideas for new features, improvements, or bug fixes, please open an issue or submit a pull request.

## Acknowledgement

This project received funding from the French ”IA Cluster” program within the Artificial and Natural Intelligence Toulouse Institute (ANITI) and from the "France 2030" program within IRT Saint Exupery. The authors gratefully acknowledge the support of the FOR projects.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
