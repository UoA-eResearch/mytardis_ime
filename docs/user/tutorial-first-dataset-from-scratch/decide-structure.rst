Decide how to describe and structure your data
##############################################

Before you start using the Instrument Data Wizard, it's crucial to plan out and document how your data will be structured for |service_name|. This ensures you and your collaborators (and your future self!) can easily locate and utilize the data within the |service_name| web portal.

How |service_name| structures data
==================================
|service_name| functions as a database, organizing data into a hierarchical structure, like folders and subfolders. This structure comprises three levels, and it's essential to align your data structure accordingly:

* Data files are grouped into `Datasets`.
* `Datasets` are organised into `Experiments`.
* `Experiments` belong to a `Project`.

It's noteworthy that a `Dataset` may belong to multiple `Experiments`, and an `Experiment` may belong to multiple `Projects`.

.. At each level of the hierarchy and at the individual file level, there are mandatory metadata fields that you can use to describe your data. There is also the ability to associate a custom metadata schema at each level, which allows you to record any relevant domain-specific observations and variables. The |service_name| Search functionality allows you to filter for data based on metadata.

Things to consider
==================
Here are some things to consider when deciding how your data should fit into this hierarchy:

* Usually, there should be one `Project` that corresponds to the research project or unit of research activity that you are collecting data for.
* Use `Experiments` to represent a study sample or variable you are studying. Store properties about the sample as metadata in each `Experiment` .
* Create one `Dataset` for each instrument you are using for acquiring data. Use the `Dataset` to contain all data files from that instrument for the `Experiment`. Store instrument run conditions as metadata in each `Dataset`.
* If the data is already using a directory structure, consider how that could translate into the hierarchical groupings.
* Consider whether you need to restrict access for a subset of your data. If so, you can group them as separate `Experiments` or `Datasets`. Later, you can restrict access to them as a whole group.

Sarah's sequencing data
=======================

Imagine yourself as Sarah, exploring how breast cancer cells react to different drug treatments. You work closely within a group of three other PhD students led by Dr Charlotte Henare.

To collect data, you take samples of cancer cells from an anonymous donor from the Hospital, treating the samples with drugs, and sending them off to a sequencing company for processing.

You sent off 15 cell samples (5 for each group) six weeks ago that have:

#. no treatment.
#. treatment with the drug Herceptin.
#. treatment with the drug Keytruda.

The tutorial data you downloaded are the resulting files sent through a USB stick via courier. The data contains the raw :code:`.fastq` files as well as aligned :code:`.bam` files (data processed by a bioinformatician) for each kind of treatment. You are now responsible for organising, setting up access control and adding metadata to the data, before it is ingested into the University's online instrument data repository |service_name| . You and your group members can then access the data through the repository portal and use it in analysis.

Given the sensitive nature of raw data, restricting access to yourself is imperative, while other data can be accessed by the entire group (with the group ID “eres004011-admin”)

After consultations with your collaborators, you have created this data structure plan:

.. _sample-data-structure-plan:

Sample data structure plan
--------------------------

    * **Project** - Named the “Breast Cancer Drug Treatment Genomics” project (ID “BREAST04”).
    * **Experiments** - Each experiment type corresponds to an Experiment (i.e. “No treatment” with ID “NoTreatment”, “Herceptin” with ID “Herceptin”, Keytruda with ID “Keytruda”).
    * **Datasets** - Within each Experiment, two `Datasets` are created: one for raw :code:`.fastq` files named “Raw” with ID “[Treatment ID]-Raw”, and another for aligned :code:`.bam` files named “Aligned” with ID “[Treatment ID]-Aligned”.
    * **Datafiles** - Each Dataset contains five files, one from each tissue sample.
    * Clinical details and sequencing instrument configurations are documented as metadata at the Dataset level.

Exercise: How does your own data fit into this hierarchy?
=========================================================

Think about the data you would like to ingest into |service_name| and discuss with your collaborators. Plan out how you would structure the data. Ask for a consultation with the friendly |service_name| staff if you would like some help!


