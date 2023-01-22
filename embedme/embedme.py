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

    def add_vectors(self, name, vectors, meta):
        self.data[name] = {"vectors": vectors, "meta": meta}

    def prepare_search(self):
        if self.vectors is None:
            self.vectors = np.stack([data["vectors"] for data in self.data.values()])

    def search_vectors(self, vector, top_n=10):
        self.prepare_search()
        distances = np.dot(self.vectors, vector)
        top_indices = np.argsort(distances)[::-1][:top_n]
        return [self.data[name]["meta"] for name in self.data.keys()][top_indices]

    def save_data(self, data, name):
        np.save(f"{self.data_folder}/{name}.npy", data)
        with open(f"{self.data_folder}/{name}.json", "w") as f:
            json.dump(data.tolist(), f)

    def load_data(self, name):
        data = np.load(f"{self.data_folder}/{name}.npy")
        with open(f"{self.data_folder}/{name}.json", "r") as f:
            metadata = json.load(f)
        return data, metadata

    def delete_data(self, name):
        os.remove(f"{self.data_folder}/{name}.npy")
        os.remove(f"{self.data_folder}/{name}.json")
