from abc import ABC, abstractmethod
import json
from vocab import vocab
class inputFile(ABC):
    @abstractmethod
    def read(self) -> list:
        pass
class JSON(inputFile):
    def __init__(self, path_provider):
        self.path_provider = path_provider

    def read(self):
        result = []
        try:
            with open(self.path_provider(), "r", encoding="utf-8") as file:
                jsonEx = json.load(file)
                for entry in jsonEx["vocabs"]:
                    for word, meaning in entry.items():
                        result.append(vocab(word, meaning, ""))
        except Exception as e:
            print(e)
        return result
class anotherReader:
    def __init__(self, input_file: inputFile):
        self.input_file = input_file
        pass
    def read(self):
        return self.input_file.read()
