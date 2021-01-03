.. role:: raw-html-m2r(raw)
   :format: html


ETL_data_reader
===============

A python package for conveniently loading the ETL data set.

Intro
-----

The ETL data set is a collection of roughly 1.600.000 handwritten characters.
Notably it includes Japanese Kanji, Hiragana and Katakana.
The data set can be found `on the ETL website <http://etlcdb.db.aist.go.jp/>`_ (a registration is needed to download the data set).
:raw-html-m2r:`<br/>`
Because the data set is stored in a custom data structure it can be hard to load.
This python package provides an easy way to load this data set and filter entries.\ :raw-html-m2r:`<br/>`
An example of using this package can be found in my application: `DaKanjiRecognizer <https://github.com/CaptainDario/DaKanjiRecognizer>`_. There it was used for `training an CNN to recognize japanese kanji characters <UPDATE HERE PLEASE>`_.\ :raw-html-m2r:`<br/>`
General information about the data set can be found in the table below.

.. list-table::
   :header-rows: 1

   * - name
     - type
     - content
     - res
     - Bit depth
     - code
     - samples perlabel
     - total samples
   * - ETL1
     - M-Type
     - Numbers :raw-html-m2r:`<br/>` Roman :raw-html-m2r:`<br/>` Symbols :raw-html-m2r:`<br/>` Katakana
     - 64x63
     - 4
     - JIS X 0201
     - ~1400
     - 141319
   * - ETL2
     - K-Type
     - Hiragana :raw-html-m2r:`<br/>` Katakana :raw-html-m2r:`<br/>` Kanji :raw-html-m2r:`<br/>` Roman :raw-html-m2r:`<br/>` Symbols
     - 60x60
     - 6
     - CO59
     - ~24
     - 52796
   * - ETL3
     - C-Type
     - Numeric :raw-html-m2r:`<br/>` Capital Roman :raw-html-m2r:`<br/>` Symbols
     - 72x76
     - 4
     - JIS X 0201
     - 200
     - 9600
   * - ETL4
     - C-Type
     - Hiragana
     - 72x76
     - 4
     - JIS X 0201
     - 120
     - 6120
   * - ETL5
     - C-Type
     - Katakana
     - 72x76
     - 4
     - JIS X 0201
     - ~200
     - 10608
   * - ETL6
     - M-Type
     - Katakana :raw-html-m2r:`<br/>` Symbols
     - 64x63
     - 4
     - JIS X 0201
     - 1383
     - 157662
   * - ETL7
     - M-Type
     - Hiragana :raw-html-m2r:`<br/>` Symbols
     - 64x63
     - 4
     - JIS X 0201
     - 160
     - 16800
   * - ETL8  (8B)
     - 8B-Type
     - Hiragana :raw-html-m2r:`<br/>` Kanji
     - 64x63
     - 1
     - JIS X 0208
     - 160
     - 157662
   * - ETL9  (8G)
     - 8G-Type
     - Hiragana :raw-html-m2r:`<br/>` Kanji
     - 128x127
     - 4
     - JIS X 0208
     - 200
     - 607200
   * - ETL10 (9B)
     - 9B-Type
     - Hiragana :raw-html-m2r:`<br/>` Kanji
     - 64x63
     - 1
     - JIS X 0208
     - 160
     - 152960
   * - ETL11 (9G)
     - 9G-Type
     - Hiragana :raw-html-m2r:`<br/>` Kanji
     - 128x127
     - 4
     - JIS X 0208
     - 200
     - 607200


Setup
-----

First download the source code from this repository.
Next install the necessary packages from the *"requirements.txt"*.

.. code-block::

   pip install -r requirements.txt

The second step is to do some renaming of the data set folders and files.
First rename the folders like this:


* ETL8B -> ETL1
* ETL8G -> ETL9
* ETL9B -> ETL10
* ETL9G -> ETL11.\ :raw-html-m2r:`<br/>`

Finally rename all files in the folders to have a naming scheme like: :raw-html-m2r:`<br/>`


* ETL_data_set\ETLX\ETLX_Y :raw-html-m2r:`<br/>`
  (\ *X and Y are numbers*\ )

On the `ETL website <http://etlcdb.db.aist.go.jp/file-formats-and-sample-unpacking-code>`_ is also a file called "euc_co59.dat" given. This **file should also be included** in the "data set"-folder on the same level as the data set part folders.

The folder structure should look like this now: :raw-html-m2r:`<br/>`

.. code-block:: bash

   ETL_data_set_folder (main folder)
   |   euc_co59.dat
   |
   |---ETL1
   |       ETL1_1
   |          |
   |       ETL1_13
   |---ETL2
   |       ETL2_1
   |          |
   |       ETL2_5
   |
   |--- |
   |
   |---ETL10
   |       ETL10_1
   |          |
   |       ETL10_5
   |---ETL11
           ETL11_1
              |
           ETL11_50

Usage
-----

You can import the package with:

.. code-block:: python

   from etl_data_reader import ETL_data_reader

To load the data set you need an ``ETL_data_reader``\ -instance.

.. code-block:: python

   path_to_data_set = "the\path\to\the\data\set"

   reader = ETL_data_reader(path_to_data_set)

where ``path_to_data_set`` should be the path to the main folder of your data set copy.\ :raw-html-m2r:`<br/>`
Example: "E:/data/ETL_data_set/" :raw-html-m2r:`<br/>`
:raw-html-m2r:`<br/>`

Now there are basically three ways to load data.

Load one data set file
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from etl_data_names import ETL_data_names

   katakana, number = ETL_character_groups.katakana, ETL_character_groups.number

   imgs, labels = reader.read_dataset_file(part=2, data_set=ETL_data_names.ETL7, katakana, number)

This will load "...\ETL_data_set_folder\ETL7\ETL7_2". :raw-html-m2r:`<br/>`

And store the images and labels which are either *katakana* or *number* in the variables ``imgs`` and ``labels``.

Load one data set part
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from etl_data_names import ETL_data_names

   kanji, hiragana = ETL_character_groups.kanji, ETL_character_groups.hiragana

   imgs, labels = reader.read_dataset_part(data_set=ETL_data_names.ETL2, kanji, hiragana)

This will load all files in the folder "...\ETL_data_set_folder\ETL2\".
Namely: ...\ETL2\ETL2_1, ...\ETL2\ETL2_1 ,..., ...\ETL2\ETL2_5. :raw-html-m2r:`<br/>`

And store the images and labels which are either *kanji* or *hiragana* in the variables ``imgs`` and ``labels``.

Load the whole data set
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from etl_data_names import ETL_data_names

   roman, symbol = ETL_character_groups.roman, ETL_character_groups.symbols

   imgs, labels = reader.read_dataset_whole(roman, symbol)

This will load all *roman* and *symbol* characters from the whole ETL data set.

**Note: filtering data set entries**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As the examples above already showed the loading of data set entries can be restricted to certain groups.
Those groups can be seen in: `etl_character_groups.py <src/etl_character_groups.py>`_

**Note: processing the images while loading**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All of the above methods have the optional parameters: :raw-html-m2r:`<br/>`
``resize : Tuple[int, int] = (64, 64)`` :raw-html-m2r:`<br/>`
and :raw-html-m2r:`<br/>` 
``normalize : bool = True``\ :raw-html-m2r:`<br/>`
The ``resize``\ -parameter resizes all images to the given size.\ :raw-html-m2r:`<br/>`
The ``normalize``\ -parameter normalizes the grayscale values of the images between $[0.0, 1.0]$.

**Warning:**
If those parameters are set to negative values no resizing/normalization will be done. :raw-html-m2r:`<br/>`
**This will lead to an error if the data set is read with ``read_dataset_whole()``\ !**

Development
-----------

For development *python 3.8* was used. :raw-html-m2r:`<br/>`
The documentation was made with Sphinx and m2r.
m2r is being used to automatically convert this README.md to .rst.
This happens when the ``sphinx-build``\ -command is invoked.

Limitations
-----------

This implementation **does not** allow to access all the stored data.
Currently one can load:


* images
* label of the image

of every ETL data set entry.

However this package should be easily extendable to add support for accessing the other data.

Additional Notes
----------------

Pull requests and issues are welcome.
