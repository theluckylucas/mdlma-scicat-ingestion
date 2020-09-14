# mdlma-scicat-ingestion
Scripts to manage the metadata about various datasets in Scicat

This repository contains a tool (Python 3.5 or higher) to manage the data at https://scicat-mdlma.desy.de (via its REST interface), which serves as the central instance to get an overview of the or find data related to the MDLMA project.

The Scicat tool is used through scripts `Ingest<SITE>.py`, `Delete<SITE>.py`, et cetera. `<SITE>` is the site, where the data has been aquired, e.g. `P05` beamline at DESY (a more detailed description should always be found in the `location` attribute of a raw dataset).

Run a script by calling e.g. `python Ingest<SITE>.py -h` to get a description of the required and optional arguments.


## Add data about other sites

If you want to add scripts that ingest data from another site, first inherit a class from [DatasetBuilder](ScicatTool/Datasets/Dataset.py) that builds the data for the API request body by generating a dict. Similarily, add a subfolder to the [Sites](ScicatTool/Sites) folder that consists of a `Ingestion.py` files, which uses the new `DatasetBuilder`, [ProposalBuilder](ScicatTool/Proposals/Proposal.py), or [DatablockBuilder](ScicatTool/Datablocks/Datablock.py) to create dicts that will the [API functions](ScicatTool/REST/API.py) will be called with. Helper functions in [Filesystem](ScicatTool/Filesystem) can support in discovering the actual data on the filesystem. In th end, inherit from [Arguments](ScicatTool/Utils/Arguments.py) for site-specific command line arguments, which the top-level script in the root folder uses when being called from the user.


## Links

More information about the project: https://www.hzg.de/ms/mdlma/

More information about Scicat: https://scicatproject.github.io/

More information about DESY IT: https://it.desy.de/
