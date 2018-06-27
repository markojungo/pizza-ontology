import owlready as owr
import os

owr.onto_path.append(os.getcwd())
onto = owr.Ontology("http://pyonto.com/ontologies/pyonto.owl")


class Drug(owr.Thing):
    ontology = onto


class DrugAssociation(Drug):
    pass


class has_for_cost(owr.FunctionalProperty):
    ontology = onto
    domain = [Drug]
    range = [float]


onto.save()
