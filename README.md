# ETLCDB_data_reader
A python package for conveniently loading the ETLCDB.
The complete documentation including the API can be found [here](https://captaindario.github.io/ETL_data_reader/build/index.html).

## Intro

The ETLCDB is a collection of roughly 1.600.000 handwritten characters.
Notably it includes Japanese Kanji, Hiragana and Katakana.
The data set can be found [on the ETLCDB website](http://etlcdb.db.aist.go.jp/) (a registration is needed to download the data set).
<br/>
Because the data set is stored in a custom data structure it can be hard to load.
This python package provides an easy way to load this data set and filter entries.<br/>
An example of using this package can be found in my application: [DaKanji](https://github.com/CaptainDario/DaKanji-mobile). There it was used for [training an CNN to recognize hand written Japanese characters, numbers and roman letters](https://github.com/CaptainDario/DaKanjiRecognizer-ML).<br/>
General information about the data set can be found in the table below.

|    name    |   type  |                    content                                              |   res   | Bit depth |    code    | samples per label | total samples | 
|:----------:|:-------:|:-----------------------------------------------------------------------:|:-------:|:---------:|:----------:|:----------------:|:-------------:|
| ETL1       | M-Type  | Numbers <br/> Roman <br/> Symbols <br/> Katakana                        |  64x63  |     4     | JIS X 0201 |   ~1400          |     141319    |
| ETL2       | K-Type  | Hiragana <br/> Katakana <br/> Kanji <br/> Roman <br/> Symbols           |  60x60  |     6     |    CO59    |     ~24          |      52796    |
| ETL3       | C-Type  | Numeric <br/> Capital Roman <br/> Symbols                               |  72x76  |     4     | JIS X 0201 |     200          |       9600    |
| ETL4       | C-Type  | Hiragana                                                                |  72x76  |     4     | JIS X 0201 |     120          |       6120    |
| ETL5       | C-Type  | Katakana                                                                |  72x76  |     4     | JIS X 0201 |    ~200          |      10608    |
| ETL6       | M-Type  | Katakana <br/> Symbols                                                  |  64x63  |     4     | JIS X 0201 |    1383          |     157662    |
| ETL7       | M-Type  | Hiragana <br/> Symbols                                                  |  64x63  |     4     | JIS X 0201 |     160          |      16800    |
| ETL8  (8B) | 8B-Type | Hiragana <br/> Kanji                                                    |  64x63  |     1     | JIS X 0208 |     160          |     157662    |
| ETL9  (8G) | 8G-Type | Hiragana <br/> Kanji                                                    | 128x127 |     4     | JIS X 0208 |     200          |     607200    |
| ETL10 (9B) | 9B-Type | Hiragana <br/> Kanji                                                    |  64x63  |     1     | JIS X 0208 |     160          |     152960    |
| ETL11 (9G) | 9G-Type | Hiragana <br/> Kanji                                                    | 128x127 |     4     | JIS X 0208 |     200          |     607200    |

**Note:** <br>
The ETL6 and ETL7 parts include half width katakana which are stored as roman letters.
As an example: "ｹ" is stored as "ke".
Those are automatically converted from this package.
Also full width numbers and letters are converted when using the package.
Example: ０ -> 0 and Ａ -> A


## Setup
First download the wheel from the [releases page](https://github.com/CaptainDario/ETLCDB_data_reader/releases).
Now install the wheel with:
```bash
pip install .\path\to\etl_data_reader_CaptainDario-2.0-py3-none-any.whl
```
Or install it directly via https:
```bash
pip install https://github.com/CaptainDario/ETLCDB_data_reader/releases/download/v2.1.4/etl_data_reader_CaptainDario-2.1.4-py3-none-any.whl
```
Assuming you already have [downloaded the ETLCDB](http://etlcdb.db.aist.go.jp/obtaining-etl-character-database) and [unpack.zip](http://etlcdb.db.aist.go.jp/file-formats-and-sample-unpacking-code).

You can either run

``` python
from etldr.extract_downloads import *

extract_etlcdb("path/to/etlcdb")
```


<details>
  <summary>Or do the preprocessing yourself</summary>
  
You have to do some renaming of the data set folders and files.
First rename the folders like this:
* ETL8B -> ETL8
* ETL8G -> ETL9
* ETL9B -> ETL10
* ETL9G -> ETL11.<br/>

Finally rename all files in the folders to have a naming scheme like: <br/>
* ETL_data_set\ETLX\ETLX_Y <br/>
(*X and Y are numbers*)

On the [ETLCDB website](http://etlcdb.db.aist.go.jp/file-formats-and-sample-unpacking-code) is also a file called "euc_co59.dat" provided in a zip called `unpack.zip`. This **file should also be included in the "data set"-folder** on the same level as the data set part folders.
</details>

The folder structure should look like this now: <br/>
```bash
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
```


## Usage
Now you can import the package with:
```python
import etldr
```

To load the data set you need an ```ETLDataReader```-instance.
```python
path_to_data_set = "the\path\to\the\data\set"

reader = etldr.DataReader(path_to_data_set)
```
where ```path_to_data_set``` should be the path to the main folder of your data set copy.<br/>
Example: "E:/data/ETL_data_set/" <br/>
<br/>

Now there are basically three ways to load data.

### Load one data set file
```python
from etldr.etl_data_names import ETLDataNames
from etldr.etl_character_groups import ETLCharacterGroups

include = [ETLCharacterGroups.katakana, ETLCharacterGroups.number]

imgs, labels = reader.read_dataset_file(2, ETLDataNames.ETL7, include)
```
This will load "...\ETL_data_set_folder\ETL7\ETL7_2". <br/>

And store the images and labels which are either *katakana* or *number* in the variables ```imgs``` and ```labels```.

### Load one data set part
```python
from etldr.etl_data_names import ETLDataNames
from etldr.etl_character_groups import ETLCharacterGroups

include = [ETLCharacterGroups.kanji, ETLCharacterGroups.hiragana]

imgs, labels = reader.read_dataset_part(ETLDataNames.ETL2, include)
```
This will load all files in the folder "...\ETL_data_set_folder\ETL2\".
Namely: ...\ETL2\ETL2_1, ...\ETL2\ETL2_1 ,..., ...\ETL2\ETL2_5. <br/>

And store the images and labels which are either *kanji* or *hiragana* in the variables ```imgs``` and ```labels```.

### Load the whole data set
**Warning: This will use a lot of memory.** <br/>
```python
from etldr.etl_character_groups import ETLCharacterGroups

include = [ETLCharacterGroups.roman, ETLCharacterGroups.symbols]

imgs, labels = reader.read_dataset_whole(include)
```
This will load all *roman* and *symbol* characters from the whole ETLCDB.
### Load the whole data set using multiple processes
**Warning: This will use a lot of memory.** <br/>
```python
from etldr.etl_character_groups import ETLCharacterGroups

include = [ETLCharacterGroups.roman, ETLCharacterGroups.symbols]

imgs, labels = reader.read_dataset_whole(include, 16)
```
This will load all *roman* and *symbol* characters from the whole ETLCDB using 16 processes.


#### **Note: filtering data set entries**
As the examples above already showed the loading of data set entries can be restricted to certain groups.
Those groups can be seen in: [etl_character_groups.py](https://captaindario.github.io/ETLCDB_data_reader/build/etl_character_groups.html)

#### **Note: processing the images while loading**
All of the above methods have the optional parameters: <br/>
```resize : Tuple[int, int] = (64, 64)``` <br/>
and <br/> 
```normalize : bool = True```<br/>
The ```resize```-parameter resizes all images to the given size.<br/>
The ```normalize```-parameter normalizes the grayscale values of the images between $[0.0, 1.0]$.

**Warning:**
If those parameters are set to negative values no resizing/normalization will be done. <br/>
**This will lead to an error if the data set is read with ```read_dataset_whole()```!**

## Limitations
This implementation **does not** allow to access all the stored data.
Currently one can load:
* image
* label of the image
  
of every ETLCDB entry.

However this package should be easily extendable to add support for accessing the other data.
## Development notes
For development *python 3.9* was used. <br/>

### documentation
The documentation was made with Sphinx and m2r.
m2r is being used to automatically convert this README.md to .rst.
This happens when the ```sphinx-build```-command is invoked in the 'docs'-folder. <br>
Build the docs (should be run in docs folder): <br>
```
sphinx-build source build
```

### packages
A list of all packages needed for development can be found in 'requirements.txt'.

### testing
Some [simple test cases](./tests/test_etldr.py) are defined in the tests folder.
Testing was only performed on Windows 10.<br>
All tests can be executed with:
```
python tests\test_etldr.py
```
Specific tests can be run with:
```
python tests\test_etldr.py etldr.test_read_dataset_part_parallel
```
Those commands should be executed on the top level of this package.

### building the wheel
The wheel can be build with:
```
python setup.py sdist bdist_wheel
```


## Additional Notes
Pull requests and issues are welcome.

If you open a pull request make sure to [run the tests before](./run_test).
