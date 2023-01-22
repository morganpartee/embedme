import os
import json
import numpy as np
import openai


class Embedme:
    def __init__(self, data_folder=".embedme", model="text-embedding-ada-002"):
        self.data_folder = data_folder
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        self.data = {}  # store the data here
        self.vectors = None
        self.model = model

    def get_embedding(self, text):
        text = text.replace("\n", " ")
        return openai.Embedding.create(input=[text], model=self.model)["data"][0][
            "embedding"
        ]

    def add(self, data, save=True):
        name = data["name"]
        embeddings = self.get_embedding(data["text"])

        self.add_vectors(name=name, vectors=embeddings, meta=data)

        if save:
            self.save()

    def add_vectors(self, name, vectors, meta):
        self.data[name] = {"vectors": vectors, "meta": meta}
        # Remove the prebuild array when we add new stuff
        self.vectors = None

    def search(self, text):
        embeddings = self.get_embedding(text)
        return self.search_vectors(embeddings)

    def prepare_search(self):
        if self.vectors is None or self.vectors.shape[0] != len(self.data):
            self.vectors = np.stack([data["vectors"] for data in self.data.values()])

    def search_vectors(self, vector, top_n=10):
        self.prepare_search()
        distances = np.dot(self.vectors, vector)
        top_indices = np.argsort(distances)[::-1][:top_n]
        names = [name for name in self.data.keys()]

        # Remove vectors
        return [
            {
                k: v
                for i in top_indices
                for k, v in self.data[names[i]].items()
                if k != "vectors"
            }
        ]

    def save(self):
        with open(f"{self.data_folder}/embed.json", "w") as f:
            json.dump(self.data, f)

    def load(self):
        with open(f"{self.data_folder}/embed.json", "r") as f:
            self.data = json.load(f)

    def delete(self):
        os.remove(f"{self.data_folder}/embed.json")
