Import your data into the Instrument Data Wizard
================================================
To import your data into the Instrument Data Wizard, open the Wizard and click the `Import data files` button.

.. image:: import-1.png

A step-by-step wizard will show up, with the first page giving a brief introduction to the |service_name| hierarchy.

.. image:: import-2.png

Add the first `Project`, `Experiment`, `Dataset` and `Datafiles`
----------------------------------------------------------------
Click *Next*. In the subsequent dialogs, the wizard will ask you where you would like to organise your data. Because we are starting with a blank metadata file, the wizard will ask you to create a new Project, Experiment and Dataset. 

As Sarah, you would like to import your raw data for the Keytruda trial. See if you can re-create this hierarchy in the Instrument Data Wizard:

* Project: Name: "Breast Cancer Drug Treatment Genomics", with ID "BREAST04".
* Experiment: Name: "Keytruda", with ID "Keytruda".
* Dataset: Name: "Raw", with ID "Keytruda-Raw".
* Data files: Add all the .fastq files in the tutorial data folder, under `tutorial-data/keytruda/`.

Once finished, your editor should look like this.

.. image:: import-3.png

.. admonition:: What if I want to add data into an existing `Project` in the repository?

    If there is already a Project for your data in the data repository, you need to import it into the Instrument Data Wizard before you can start adding files to it. You can follow the instructions for :doc:`Adding data to existing Projects, Experiments or Datasets in the data repository <../adding-to-existing-structure>`.

Add more data
-------------
What if you have files you need to organise separately from the initial import? Or if you need to add more files into the same dataset? For example, you may wish to ingest more than one sample or instrument run data files.

You can click the `Import data files` button again, and the step-by-step wizard will prompt you to add files and ask how you would like to organise them.

As Sarah, you also have some raw data in the Herceptin trial you would like to import. 

After clicking the `Import data files` button and going through the initial explanation screen, you will now be presented with a choice to add files to an existing `Project`, or create a new `Project`. 

.. image:: import-4.png

Since this is data for the same project, choose the "Breast Cancer Drug Treatment Genomics" `Project`.


Then proceed through the rest of the wizard using this setup.

* Create a new Experiment with name "Herceptin", and ID "Herceptin".
* Create a new Dataset with the name "Raw", and ID "Herceptin-Raw".
*  Data files: Add the .fastq files in the tutorial data folder, under `tutorial/herceptin/`.

Once finished, your editor should look like this.

.. image:: import-5.png

Save your progress
------------------
Click the `Save` button, and save under the tutorial data folder. Name it "metadata.yml".

.. admonition:: Save as you go!
    
    Remember to save your changes as you work! As the Instrument Data Wizard is still being developed, bugs and crashes may happen at inopportune moments. After a crash, you can reopen the file using the `Open` button.

.. admonition:: Exercise

    Try to re-create the hierarchy as described in the :ref:`example data structure plan <sample-data-structure-plan>`.

