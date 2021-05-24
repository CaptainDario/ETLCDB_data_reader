# this file assumes that in the parent directory a folder
# called 'etl_data_set'-exists in which the renamed
# etl-data set is located

import unittest
import os
import sys
import time
import multiprocessing as mp
import numpy as np

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
        
        print("started: test_read_dataset_file")

        reader = ETLDataReader(os.path.join(os.getcwd(), "etl_data_set"))

        imgs, labels = [], []

        for name in ETLDataNames:
            _imgs, _labels = reader.read_dataset_file(1, name, [ETLCharacterGroups.all])
            labels.append(_labels)
        
        print(labels)
        correct_labels = ["0", "上", "0", "あ", "ア", "ア", "ア", "あ", "あ", "あ", "亜"]
        for i in range(11):
            #compare the byte representation
            self.assertEqual(str.encode(labels[i][0]), str.encode(correct_labels[i]))

        print("finished: test_read_dataset_file")
    
    
    def test_image_resize(self):
        """Test the ETLDataReader.read_dataset_file method with different resizing options.
        """

        print("started: test_image_resize")

        size_in = [(12, 12), (12, 37), (-1, 12), (35, 0)]

        correct_out = [(12, 12, 1), (12, 37, 1), (63, 64, 1), (63, 64, 1)]

        reader = ETLDataReader(os.path.join(os.getcwd(), "etl_data_set"))
        imgs, labels = [], []

        for i in range(3):
            _imgs, _labels = reader.read_dataset_file(1, ETLDataNames.ETL1, [ETLCharacterGroups.all], resize=size_in[i])
            imgs.append(_imgs)
            #labels.append(_labels)

        for i in range(3):
            #compare the byte representation
            self.assertEqual(imgs[i][0].shape, correct_out[i])

        print("finished: test_image_resize")

    def test_image_normalizing(self):
        """Test the ETLDataReader.read_dataset_file method with normalizing.
        """
        
        print("started: test_image_normalizing")
        
        reader = ETLDataReader(os.path.join(os.getcwd(), "etl_data_set"))

        _imgs, _labels = reader.read_dataset_file(1, ETLDataNames.ETL1, [ETLCharacterGroups.all], normalize=True)

        self.assertTrue(_imgs[0].max() <= 1.0)

        print("finished: test_image_normalizing")

    def test_read_dataset_part(self):
        """Test the ETLDataReader.read_dataset_part method.
        """
        
        print("started: test_read_dataset_part")
        
        reader = ETLDataReader(os.path.join(os.getcwd(), "etl_data_set"))

        _imgs, _labels = reader.read_dataset_part(ETLDataNames.ETL1, [ETLCharacterGroups.all])

        self.assertEqual(len(_labels), 141251)

        print("finished: test_read_dataset_part")
    
    def test_read_dataset_part_parallel(self):
        """Test the ETLDataReader.read_dataset_part method in parallel mode.
        """
        
        print("started: test_read_dataset_part_parallel")
        
        reader = ETLDataReader(os.path.join(os.getcwd(), "etl_data_set"))

        t_1_1 = time.perf_counter()
        _imgs_1, _labels_1 = reader.read_dataset_part(ETLDataNames.ETL9, [ETLCharacterGroups.all])
        t_1_2 = time.perf_counter()
        
        t_2_1 = time.perf_counter()
        _imgs_2, _labels_2 = reader.read_dataset_part(ETLDataNames.ETL9, [ETLCharacterGroups.all], mp.cpu_count())
        t_2_2 = time.perf_counter()

        time_1 = t_1_2 - t_1_1
        time_2 = t_2_2 - t_2_1

        print("running with 1 process in", time_1)
        print("running with", mp.cpu_count(), "processes in", time_2)
        print("absolute difference:", time_1 - time_2)
        print("speedup:", time_1 / time_2)
        print("efficiency:", time_2 / mp.cpu_count())

        self.assertEqual(len(_labels_2), len(_labels_1))

        print("finished: test_read_dataset_part_parallel")
    
    def test_read_dataset_whole_parallel(self):
        """Test the ETLDataReader.read_dataset_whole method in parallel mode.
        """
        
        print("started: test_read_dataset_whole_parallel")
        
        reader = ETLDataReader(os.path.join(os.getcwd(), "etl_data_set"))

        t_1_1 = time.perf_counter()
        _imgs_1, _labels_1 = reader.read_dataset_whole([ETLCharacterGroups.all])
        t_1_2 = time.perf_counter()
        
        t_2_1 = time.perf_counter()
        _imgs_2, _labels_2 = reader.read_dataset_whole([ETLCharacterGroups.all], mp.cpu_count())
        t_2_2 = time.perf_counter()

        time_1 = t_1_2 - t_1_1
        time_2 = t_2_2 - t_2_1

        print("running with 1 process in", time_1)
        print("running with", mp.cpu_count(), "processes in", time_2)
        print("absolute difference:", time_1 - time_2)
        print("speedup:", time_1 / time_2)
        print("efficiency:", time_2 / mp.cpu_count())

        self.assertEqual(len(_labels_2), len(_labels_1))

        print("finished: test_read_dataset_whole_parallel")

    def test_read_dataset_selection(self):
        """Test the ETLDataReader.read_dataset_file method with filtering.
        """
        
        print("started: test_read_dataset_selection")
        
        reader = ETLDataReader(os.path.join(os.getcwd(), "etl_data_set"))

        # test all filter with mixed data set file
        _imgs, _labels = reader.read_dataset_file(1, ETLDataNames.ETL1, [ETLCharacterGroups.number])
        self.assertEqual(len(_labels), 11530)
        self.assertEqual(len(_imgs), 11530)
        # test number filter
        _imgs, _labels = reader.read_dataset_file(1, ETLDataNames.ETL1, [ETLCharacterGroups.all])
        print(len(_imgs), len(_labels))
        self.assertEqual(len(_labels), 11530)
        self.assertEqual(len(_imgs), 11530)
        # test number roman latter filter
        _imgs, _labels = reader.read_dataset_file(3, ETLDataNames.ETL1, [ETLCharacterGroups.roman])
        self.assertEqual(len(_labels), 11558)
        self.assertEqual(len(_imgs), 11558)
        # test symbol filter
        _imgs, _labels = reader.read_dataset_file(6, ETLDataNames.ETL1, [ETLCharacterGroups.symbols])
        self.assertEqual(len(_labels), 11554)
        self.assertEqual(len(_imgs), 11554)
        # test kanji filter
        _imgs, _labels = reader.read_dataset_file(1, ETLDataNames.ETL8G, [ETLCharacterGroups.kanji])
        self.assertEqual(len(_labels), 4405)
        self.assertEqual(len(_imgs), 4405)
        # test hiragana filter
        _imgs, _labels = reader.read_dataset_file(1, ETLDataNames.ETL4, [ETLCharacterGroups.hiragana])
        self.assertEqual(len(_labels), 6120)
        self.assertEqual(len(_imgs), 6120)
        # test katakana filter
        _imgs, _labels = reader.read_dataset_file(1, ETLDataNames.ETL5, [ETLCharacterGroups.katakana])
        self.assertEqual(len(_labels), 10608)
        self.assertEqual(len(_imgs), 10608)
        # test *implicit* all filter with mixed data set file
        _imgs, _labels = reader.read_dataset_file(5, ETLDataNames.ETL1)
        self.assertEqual(len(_labels), 11545)
        self.assertEqual(len(_imgs), 11545)

        print("finished: test_read_dataset_selection")



if __name__ == "__main__":
    unittest.main()