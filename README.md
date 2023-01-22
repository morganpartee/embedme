Embedme
Embedme is a python module that allows you to easily use embeddings from text fields with OpenAI's Embedding API and store them in a local folder.

Installation
To install Embedme, you can use pip:

```sh
pip install embedme
```

## Usage

Embedme provides a simple interface to use embeddings from text fields with OpenAI's Embedding API and store them in a local folder.

Check out the example notebook for a better example, but useage is something like:

```py
import openai
import nltk
from embedme import Embedme

# Downloading the NLTK corpus
nltk.download('gutenberg')

# Creating an instance of the Embedme class
embedme = Embedme(data_folder='.embedme', model="text-embedding-ada-002")

# Getting the embeddings for the text
text = nltk.corpus.gutenberg.raw('melville-moby_dick.txt')
embeddings = embedme.get_embedding(text)

# Adding the embeddings to the Embedme instance
embedme.add_vectors(name='moby_dick', vectors=embeddings, meta={'text': 'Moby Dick by Herman Melville'})

# Searching the vectors
result = embedme.search_vectors(embeddings)

# Printing the result
print(result)
```

## Follow Us

Some friends and I are writing about large language model stuff at [SensibleDefaults.io](https://sensibledefaults.io), honest to god free. Follow us (or star this repo!) if this helps you!

## Note

Embedme uses OpenAI's Embedding API to get embeddings for text fields, so an API key is required to use it. You can get one from https://beta.openai.com/signup/

The token limit today is about 8k, so... you're probably fine
