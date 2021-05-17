# mdlma-scicat-ingestion
Scripts to manage the metadata about various datasets in Scicat

This repository contains a tool (Python 3.5 or higher) to manage the data at https://scicat-mdlma.desy.de (via its REST interface), which serves as the central instance to get an overview of the or find data related to the MDLMA project.

The Scicat tool is used through scripts `Ingest<SITE>.py`, `Delete<SITE>.py`, et cetera. `<SITE>` is the site, where the data has been aquired, e.g. `P05` beamline at DESY (a more detailed description should always be found in the `location` attribute of a raw dataset).

Run a script by calling e.g. `python Ingest<SITE>.py -h` to get a description of the required and optional arguments.


## Run a simulation

Add `python Ingest<SITE>.py -s` to run a simulation, which means data is NOT being posted into the database. If you want to simulate a full clean run, set `SIMULATION="-s"` in `delete_and_ingest_all.sh` before running this script.


## Add data about other sites

If you want to add scripts that ingest data from another site, first inherit a class from [RawDatasetBuilder](ScicatTool/Datasets/Dataset.py) or [DerivedDatasetBuilder](ScicatTool/Datasets/Dataset.py) that builds the data for the API request body by generating a `data_dict`. Similarily, add a subfolder to the [Sites](ScicatTool/Sites) folder that consists of a `Ingestion.py` file, which uses the new `DatasetBuilder`, [ProposalBuilder](ScicatTool/Proposals/Proposal.py), [AttachmentBuilder](ScicatTool/Datasets/Dataset.py), or [OrigDatablockBuilder](ScicatTool/Datablocks/Datablock.py) to create each `data_dict` that the [API functions](ScicatTool/REST/API.py) will be called with. Make sure a `Const.py` file contains the site-specific constant values. Helper functions in [Filesystem](ScicatTool/Filesystem) can support `Ingestion.py` in discovering the actual data on the filesystem. At the end, inherit from [Arguments](ScicatTool/Utils/Arguments.py) for site-specific command line arguments, which the top-level script in the root folder uses when being called by the user.


## Links

More information about the project: https://www.hzg.de/ms/mdlma/

More information about Scicat: https://scicatproject.github.io/

More information about DESY IT: https://it.desy.de/
