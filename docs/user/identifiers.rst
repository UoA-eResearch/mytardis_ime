.. _identifiers:
Identifiers for Projects, Experiments and Datasets
##################################################

Identifiers are labels that distinguish a Project, Experiment or Dataset from others in |service_name|. You can use the field to store a meaningful code or label decided by you or your research group, as well as IDs assigned by external organisations such as a national research information system or your institution. This can help you find your data later through the search functionality in |service_name|.

An identifier can contain letters, numbers, spaces and other special symbols. An identifier must be unique to the class of objects it is applied to. For example, a Project's identifier must not be the same as another Project's. A Project, Experiment or Dataset may have multiple identifiers.

In the Instrument Data Wizard, you must specify at least one identifier for each Project, Experiment and Dataset.


What should I use as an identifier for my Project?
==================================================
You can use:

- an externally-assigned identifier such as a Research Activity ID (RAID), if available. 
- your institution's project code for the project, if available.
- The project name or another unique designation.

More identifiers can be added to the Project after importing.

What should I use as an identifier for my Experiment?
=====================================================
You can use:

- A code for the experiment, if your research group has a coding system for individual experiments.
- The experiment name or another unique designation.

More identifiers can be added to the Experiment after importing.

What should I use as an identifier for my Dataset?
==================================================
You can use:

- A code for the dataset, if your research group has a coding system for individual datasets.
- The dataset name or another unique designation

The identifier must be unique across all Datasets. There may be cases where you want to use the dataset name as the identifier, and there are similarly named Datasets. For example, you may have two experiments that use the same microscopy instrument, and the acquired images are stored in a Dataset in each Experiment, both named "Microscopy". To keep the identifiers unique, you can prefix the two identifiers with the identifier of the Experiment the dataset falls under, to distinguish between them.