# mdlma-scicat-ingestion
Scripts to manage the metadata about various datasets in Scicat

This repository contains a tool (Python 3.5 or higher) to manage the data at https://scicat-mdlma.desy.de (via its REST interface), which serves as the central instance to get an overview of the or find data related to the MDLMA project.

The Scicat tool is used through scripts `Ingest<SITE>.py`, `Delete<SITE>.py`, et cetera. `<SITE>` is the site, where the data has been aquired, e.g. `P05` beamline at DESY (a more detailed description should always be found in the `location` attribute of a raw dataset).

Run a script by calling e.g. `python Ingest<SITE>.py -h` to get a description of the required and optinal arguments.

More information about the project: https://www.hzg.de/ms/mdlma/

More information about Scicat: https://scicatproject.github.io/

More information about DESY IT: https://it.desy.de/
