from owlready import get_ontology, onto_path
from shutil import copyfile
import os


def main():
    path = os.getcwd() + "\\pizza.owl"
    copyfile(path, os.getcwd() + "\\pizza_copy.owl")  # copied file for testing

    onto_path.append("C:\\Users\\Mark.Jung\\Documents\\pizza-ontology\\")
    onto = get_ontology("http://pizza.com/ontologies/pizza_copy.owl").load()

    for onto_class in onto.classes:
        print(onto_class)


if __name__ == '__main__':
    main()
