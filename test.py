from owlready import get_ontology, onto_path
# from shutil import copyfile
import os

# path = os.getcwd() + "\\pizza.owl"
# copyfile(path, os.getcwd() + "\\pizza_copy.owl")  # copied file for testing

onto_path.append(os.getcwd())
onto = get_ontology("http://pizza.com/ontologies/pizza_copy.owl").load()

