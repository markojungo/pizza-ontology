from owlready import get_ontology
from shutil import copyfile
import os


class Ontology():
    def __init__(self, onto):
        self._onto = onto

    def get_classes(self):
        for c in self._onto.classes:
            print(c)


def main():
    path = os.getcwd() + "\\pizza.owl"
    copyfile(path, os.getcwd() + "\\pizza_copy.owl")  # copied file for testing

    owlready_ontology = get_ontology(os.getcwd() + "\\pizza_copy.owl")
    onto = Ontology(owlready_ontology)
    onto.get_classes()


if __name__ == '__main__':
    main()
