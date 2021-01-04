# this file assumes that in the parent directory a folder
# called 'etl_data_set'-exists in which the renamed
# etl-data set is located

import unittest
import os, sys

sys.path.append(os.path.abspath(os.getcwd()))

from etldr.etl_character_groups import ETLCharacterGroups
from etldr.etl_data_names import ETLDataNames
from etldr.etl_data_reader import ETLDataReader



class etldr(unittest.TestCase):
    """Test the etl data reader module.
    """

    def test_read_dataset_file(self):
        """Test the ETLDataReader.read_dataset_file method.
        """

        reader = ETLDataReader(os.path.join(os.getcwd(), "etl_data_set"))

        imgs, labels = [], []

        for name in ETLDataNames:
            _imgs, _labels = reader.read_dataset_file(1, name, ETLCharacterGroups.all)
            #imgs.append(_imgs)
            labels.append(_labels)
        
        correct_labels = ["0", "上", "0", "あ", "ア", "A", "A", "あ", "あ", "あ", "亜"]
        for i in range(11):
            #compare the byte representation
            self.assertEqual(str.encode(labels[i][0]), str.encode(correct_labels[i]))
    
    
    def test_image_resize(self):
        """Test the ETLDataReader.read_dataset_file method with different resizing options.
        """

        size_in = [(12, 12), (12, 37), (-1, 12), (35, 0)]

        correct_out = [(12, 12, 1), (12, 37, 1), (63, 64, 1), (63, 64, 1)]

        reader = ETLDataReader(os.path.join(os.getcwd(), "etl_data_set"))
        imgs, labels = [], []

        for i in range(3):
            _imgs, _labels = reader.read_dataset_file(1, ETLDataNames.ETL1, ETLCharacterGroups.all, resize=size_in[i])
            imgs.append(_imgs)
            #labels.append(_labels)

        for i in range(3):
            #compare the byte representation
            self.assertEqual(imgs[i][0].shape, correct_out[i])

    def test_image_normalizing(self):
        """Test the ETLDataReader.read_dataset_file method with normalizing.
        """
        
        reader = ETLDataReader(os.path.join(os.getcwd(), "etl_data_set"))

        _imgs, _labels = reader.read_dataset_file(1, ETLDataNames.ETL1, ETLCharacterGroups.all, normalize=True)

        self.assertTrue(_imgs[0].max() <= 1.0)

    def test_read_dataset_part(self):
        """Test the ETLDataReader.read_dataset_part method.
        """
        
        reader = ETLDataReader(os.path.join(os.getcwd(), "etl_data_set"))

        _imgs, _labels = reader.read_dataset_part(ETLDataNames.ETL1, ETLCharacterGroups.all)

        self.assertEqual(len(_labels), 141319)

    def test_read_dataset_selection(self):
        """Test the ETLDataReader.read_dataset_file method with filtering.
        """
        
        reader = ETLDataReader(os.path.join(os.getcwd(), "etl_data_set"))

        # test number filter
        _imgs, _labels = reader.read_dataset_file(1, ETLDataNames.ETL1, ETLCharacterGroups.number)
        self.assertEqual(len(_labels), 11560)
        # test number roman latter filter
        _imgs, _labels = reader.read_dataset_file(3, ETLDataNames.ETL1, ETLCharacterGroups.roman)
        self.assertEqual(len(_labels), 11560)
        # test symbol filter
        _imgs, _labels = reader.read_dataset_file(6, ETLDataNames.ETL1, ETLCharacterGroups.symbols)
        self.assertEqual(len(_labels), 11560)
        # test all filter with mixed data set file
        _imgs, _labels = reader.read_dataset_file(5, ETLDataNames.ETL1, ETLCharacterGroups.all)
        self.assertEqual(len(_labels), 11560)
        # test kanji filter
        _imgs, _labels = reader.read_dataset_file(1, ETLDataNames.ETL8G, ETLCharacterGroups.kanji)
        self.assertEqual(len(_labels), 4405)
        # test hiragana filter
        _imgs, _labels = reader.read_dataset_file(1, ETLDataNames.ETL4, ETLCharacterGroups.hiragana)
        self.assertEqual(len(_labels), 6120)
        # test katakana filter
        _imgs, _labels = reader.read_dataset_file(1, ETLDataNames.ETL5, ETLCharacterGroups.katakana)
        self.assertEqual(len(_labels), 10608)
        # test *implicit* all filter with mixed data set file
        _imgs, _labels = reader.read_dataset_file(5, ETLDataNames.ETL1)
        self.assertEqual(len(_labels), 11560)



if __name__ == "__main__":
    unittest.main()
    