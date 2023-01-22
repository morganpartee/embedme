# Embedme

Embedme is a python module that allows you to easily use embeddings from text fields with OpenAI's Embedding API and store them in a local folder.

It's like a lazy version of pinecone - Numpy is actually pretty fast for embeddings stuff at smaller scale, why overthink stuff? We store the data and vectors as json and build the numpy array before you search (and store it until you add more)

## Installation

To install Embedme, you can use pip:

```sh
pip install embedme
```

## Setup

The only thing you _must_ do before you use `embedme` is setup auth with OpenAI. We use it to embed your items and search queries, so it is required. I don't want to touch **any** of that code - just sign in how they tell you to, either in the script via a file for the key, or an environment variable for your key.

[OpenAI Python Module (With Auth Instructions)](https://github.com/openai/openai-python)

## Usage

Embedme provides a simple interface to use embeddings from text fields with OpenAI's Embedding API and store them in a local folder.

Check out the example notebook for a better example, but useage is something like:

```py
import openai
import nltk
from more_itertools import chunked
from embedme import Embedme
from tqdm import tqdm

# Downloading the NLTK corpus
nltk.download('gutenberg')

# Creating an instance of the Embedme class
embedme = Embedme(data_folder='.embedme', model="text-embedding-ada-002")

# Getting the text
text = nltk.corpus.gutenberg.raw('melville-moby_dick.txt')

# Splitting the text into sentences
sentences = nltk.sent_tokenize(text)

input("Hey this call will cost you money and take a minute. Like, a few cents probably, but wanted to warn you.")

for i, chunk in enumerate(tqdm(chunked(sentences, 20))):
    data = {'name': f'moby_dick_chunk_{i}', 'text': ' '.join(chunk)}
    embedme.add(data, save=False)

embedme.save()
```

And to search:

```py
embedme.search("lessons")
```

You can do anything you would want to with `.vectors` after you call `.prepare_search()` (or... search something, it's automatic mostly), like plot clusters, etc.

## Follow Us

Some friends and I are writing about large language model stuff at [SensibleDefaults.io](https://sensibledefaults.io), honest to god free. Follow us (or star this repo!) if this helps you!

## Note

Embedme uses OpenAI's Embedding API to get embeddings for text fields, so an API key is required to use it. You can get one from https://beta.openai.com/signup/

The token limit today is about 8k, so... you're probably fine
