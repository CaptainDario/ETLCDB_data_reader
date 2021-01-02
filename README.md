# ETL_data_reader
A python package for conveniently loading the ETL data set.

## Intro

The ETL data set is a collection of roughly 1.600.000 handwritten characters.
Notably it includes Japanese Kanji, Hiragana and Katakana.
The data set can be found [on the ETL website](http://etlcdb.db.aist.go.jp/) (a registration is needed to download the data set).
<br/>
Because the data set is stored in a custom data structure it can be hard to load.
This python package provides an easy way to load this data set and filter entries.<br/>
An example of using this package can be found in my application: [DaKanjiRecognizer](https://github.com/CaptainDario/DaKanjiRecognizer). There it was used for [training an CNN to recognize japanese kanji characters](UPDATE HERE PLEASE).<br/>
General information about the data set can be found in the table below.

|    name    |   type  |                    content                                              |   res   | Bit depth |    code    | samples perlabel | total samples |
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

## Setup
First download the source code from this repository.
Next install the necessary packages from the *"requirements.txt"*.
```
pip install -r requirements.txt
```
The second step is to do some renaming of the data set folders and files.
First rename the folders like this:
* ETL8B -> ETL1
* ETL8G -> ETL9
* ETL9B -> ETL10
* ETL9G -> ETL11.<br/>

Finally rename all files in the folders to have a naming scheme like: <br/>
* ETL_data_set\ETLX\ETLX_Y <br/>
(*X and Y are numbers*)

On the [ETL website](http://etlcdb.db.aist.go.jp/file-formats-and-sample-unpacking-code) is also a file called "euc_co59.dat" given. This **file should also be included** in the "data set"-folder on the same level as the data set part folders.

The folder structure should look like this now: <br/>
```bash
ETL_data_set_folder (main folder)
│   euc_co59.dat
│
├───ETL1
│       ETL1_1
│          ⋮
│       ETL1_13
├───ETL2
│       ETL2_1
│          ⋮
│       ETL2_5
├───ETL3
│       ETL3_1
│       ETL3_2
├───ETL4
│       ETL4_1
├───ETL5
│       ETL5_1
├───ETL6
│       ETL6_1
│          ⋮
│       ETL6_12
├───ETL7
│       ETL7_1
│       ETL7_2
├───ETL8
│       ETL8_1
│          ⋮
│       ETL8_3
├───ETL9
│       ETL9_1
│          ⋮
│       ETL9_33
├───ETL10
│       ETL10_1
│          ⋮
│       ETL10_5
└───ETL11
        ETL11_1
           ⋮
        ETL11_50
```


## Usage
You can import the package with:
```python
from etl_data_reader import ETL_data_reader
```
To load the data set you need an ```ETL_data_reader```-instance.
```python
path_to_data_set = "the\path\to\the\data\set"

reader = ETL_data_reader(path_to_data_set)
```
where ```path_to_data_set``` should be the path to the main folder of your data set copy.<br/>
Example: "E:/data/ETL_data_set/" <br/>
<br/>


Now there are basically three ways to load data.

### Load one data set file
```python
katakana, number = ETL_character_groups.katakana, ETL_character_groups.number

reader.read_dataset_file()
```

### Load one data set part
```python
kanji, hiragana = ETL_character_groups.kanji, ETL_character_groups.hiragana

reader.read_dataset_part()
```

### Load the whole data set
```python
roman, symbol = ETL_character_groups.roman, ETL_character_groups.symbols

reader.read_dataset_whole(roman, symbol)
```
This will load all *kanji* and *hiragana* characters from the whole ETL data set.

#### **Note: filtering data set entries**
As the examples above already showed the loading of data set entries can be restricted to certain groups.
Those groups can be seen in: [etl_character_groups.py](src/etl_character_groups.py)

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

## Development
For development *python 3.8* was used. <br/>
The documentation was made with Sphinx.

## Limitations
This implementation **does not** allow to access all the stored data.
Currently one can load:
* images
* label of the image
  
of every ETL data set entry.

However this package should be easily extendable to add support for accessing the other data.

## Additional Notes
Pull requests and issues are welcome.