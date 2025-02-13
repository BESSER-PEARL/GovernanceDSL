# GovernanceDSL

This repository contains the development of the governance DSL proposed for human-agent decision-making.
We first start by replicating the DSL presented by J.L.Cánovas and J.Cabot.

* Folder `Xtext/` contains the definition of the grammar of the DSL using Xtext. It generates Python classes for defining the metamodel.
* Folder `ANTLR/` contains the definition of the grammar of the DSL using ANTLR. It generates the object bUML instances.
* `object_model_dsl.py` is the representation of the metamodel of the DSL abstract syntax in bUML. It is composed by the [DomainModel](https://besser.readthedocs.io/en/latest/buml_language/model_types/structural.html) and [ObjectModel](https://besser.readthedocs.io/en/latest/buml_language/model_types/object.html).