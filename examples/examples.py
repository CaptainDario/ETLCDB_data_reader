import sys
import os
import time

sys.path.append(os.path.abspath(os.getcwd()))

from etldr.etl_data_reader import ETLDataReader


def load_one_data_set_file(reader : ETLDataReader):
    """The first example of the README.

    Args:
        reader : ETLDataReader instance to load the data set part.
    """

    from etldr.etl_data_names import ETLDataNames
    from etldr.etl_character_groups import ETLCharacterGroups

    include = [ETLCharacterGroups.katakana, ETLCharacterGroups.number]

    imgs, labels = reader.read_dataset_file(2, ETLDataNames.ETL7, include)

def load_one_data_set_part(reader : ETLDataReader):
    """The second example of the README.

    Args:
        reader : ETLDataReader instance to load the data set part.
    """

    from etldr.etl_data_names import ETLDataNames
    from etldr.etl_character_groups import ETLCharacterGroups

    include = [ETLCharacterGroups.kanji, ETLCharacterGroups.hiragana]

    imgs, labels = reader.read_dataset_part(ETLDataNames.ETL2, include)


def load_one_data_set_part_parallel(reader : ETLDataReader):
    """The second example of the README.

    Args:
        reader : ETLDataReader instance to load the data set part.
    """

    from etldr.etl_data_names import ETLDataNames
    from etldr.etl_character_groups import ETLCharacterGroups

    include = [ETLCharacterGroups.kanji, ETLCharacterGroups.hiragana]

    imgs, labels = reader.read_dataset_part(ETLDataNames.ETL2, include, 16)


def  load_the_whole_data_set(reader : ETLDataReader):
    """The third example of the README.

    Args:
        reader : ETLDataReader instance to load the data set part.
    """

    from etldr.etl_character_groups import ETLCharacterGroups

    include = [ETLCharacterGroups.roman, ETLCharacterGroups.symbols]

    imgs, labels = reader.read_dataset_whole(include)


def  load_the_whole_data_set_parallel(reader : ETLDataReader):
    """The third example of the README.

    Args:
        reader : ETLDataReader instance to load the data set part.
    """

    from etldr.etl_character_groups import ETLCharacterGroups

    include = [ETLCharacterGroups.roman, ETLCharacterGroups.symbols]

    imgs, labels = reader.read_dataset_whole(include, 16)



if __name__ == "__main__":
    path_to_data_set = r"F:\data_sets\ETL_kanji"

    reader = ETLDataReader(path_to_data_set)

    # uncomment one of these examples
    #load_one_data_set_file(reader)
    #load_one_data_set_part(reader)
    #load_the_whole_data_set(reader)
    #load_one_data_set_part_parallel(reader)
    #load_the_whole_data_set_parallel(reader)
