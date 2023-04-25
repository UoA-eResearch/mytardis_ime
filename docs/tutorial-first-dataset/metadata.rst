Annotate your data with metadata
################################
Now that your files are imported and organised, you can start annotating them.

In |service_name|, there is a basic set of metadata fields applicable for any `Projects`, `Experiments`, `Datasets` or `Datafiles`. They are fields like name, ID, author and institution.

In addition, you can attach more metadata to a `Project`, `Experiment`, `Dataset` or `Datafile` through `Schemas`. They are sets of metadata fields (`Parameters`) defined to store domain- or instrument- specific metadata. For example, you may want to have a `Schema` for describing the study or treatment you have applied to the sample. Alternatively, you may wish to note down the instrument configuration used for acquiring data. Data from a sequencer may benefit from a `Schema` with depth of sequencing and sequencing method as `Parameters`.

In the Instrument Data Wizard, first select the `Project`, `Experiment`, `Dataset` or `Datafile` you wish to edit, then you can change metadata on the right-hand pane.

.. INSERT DEMO OF RIGHT-HAND PANE HERE.

The `Description` tab contains the basic metadata fields, while the `Metadata` tab contains the `Schema` metadata fields.

.. admonition:: Keep your `Schema` names and values consistent
    
    Record `Parameter` names and values consistently, using the same letter casing and units. This will help with finding your data in the future. For example, if you have a Parameter representing a length, decide on the name (e.g. "distance", no uppercase) and the value unit (e.g. millimetre), and use them consistently.

    It's best to create a data dictionary document with your collaborators. See the `Data Dictionary Guide <../data-dictionary>`_.

Sarah's metadata: sequencing depth
==================================
As Sarah, you would like to note down the sequence depth, which is 100, used for each treatment. In genetics, sequence depth measures the `completeness of the sequencing process <https://en.wikipedia.org/wiki/Coverage_(genetics)>`_. You have decided with your team that it should be recorded as a `Schema Parameter` on each `Experiment`, with the name `Depth of sequencing`, and value as an integer.

Try adding this for the Herceptin `Experiment`. Once finished, your editor should look like this.

.. INSERT IMAGE OF FINISHED EDITOR STATE HERE.

