
from etldr.etl_codes import ETLCodes
from etldr.etl_data_names import ETLDataNames
from etldr.etl_character_groups import ETLCharacterGroups 

import os
import re
import struct
import multiprocessing as mp

from PIL import Image
import numpy as np
import bitstring
import jaconv

from tqdm.auto import tqdm
from typing import List, Tuple




class ETLDataReader():
    """A class which contains helper functions to load, process and filter the data from the ETL data set.

    Attributes:
        codes     (ETLCodes) : ETLCodes instance for decoding the ETL data set labels. 
        dataset_types (dict) : A dict which maps the data set parts to their type.
        path           (str) : The path to the folder with the data set (should also contain 'euc_c059.dat').
        data_set_parts_with_dummy [ETLDataNames] : A list of the data set parts which have a dummy entry at the beginning.
    """


    def __init__(self, path : str):
        
        self.codes         = None
        self.dataset_types = {}
        self.path          = path
        
        #create an instance of ETLCodes to decode loaded data
        self.codes = ETLCodes(os.path.join(self.path, "euc_co59.dat"))
        
        self.init_dataset_types()

        #ETL8B and 9B have a dummy entry at the beginning
        self.data_set_parts_with_dummy = [ETLDataNames.ETL8B, ETLDataNames.ETL9B]


    def init_dataset_types(self):
        """
        Initialize the dictionary of dataset_types and their codes
        """

        self.dataset_types[ETLDataNames.ETL1 ] = self.codes.code_M
        self.dataset_types[ETLDataNames.ETL2 ] = self.codes.code_K
        self.dataset_types[ETLDataNames.ETL3 ] = self.codes.code_C
        self.dataset_types[ETLDataNames.ETL4 ] = self.codes.code_C
        self.dataset_types[ETLDataNames.ETL5 ] = self.codes.code_C
        self.dataset_types[ETLDataNames.ETL6 ] = self.codes.code_M
        self.dataset_types[ETLDataNames.ETL7 ] = self.codes.code_M
        self.dataset_types[ETLDataNames.ETL8B] = self.codes.code_8B
        self.dataset_types[ETLDataNames.ETL8G] = self.codes.code_8G
        self.dataset_types[ETLDataNames.ETL9B] = self.codes.code_9B
        self.dataset_types[ETLDataNames.ETL9G] = self.codes.code_9G


    def read_dataset_file(self, part : str,
                            data_set : ETLDataNames,
                            include : List[ETLCharacterGroups] = [ETLCharacterGroups.all],
                            resize : Tuple[int, int] = (64, 64),
                            normalize : bool = True,
                            show_loading_bar : bool = True) -> Tuple[np.array, np.array]:
        """Reads, process and filters all entries from the ETL data set file.
        
        Note:
            The loaded images will be a numpy array with dtype=float16.

        Args:
            name      : The name of the file to load.
            data_set  : The data set part which should be loaded (ex.: 'ETL1').
            include   : All character types (Kanji, Hiragana, Symbols, stc.) which should be included.
            resize    : The size the image should be resized (if resize < 1 the images will not be resized). Defaults to (64, 64).
            normalize : Should the gray values be normalized between [0.0, 1.0]. Defaults to True.

        Returns:
            The loaded and filtered data set entries in the given file in the form: (images, labels).
        """

        imgs, labels = [], []

        #get the necessary data set info from the dict
        data_info = self.dataset_types[data_set]

        #open the file and read it byte by byte
        path = os.path.join(self.path, data_set.value, part)
        with open(path, "rb") as f:
            
            #get file size 
            f.seek(0, 2)
            file_size = int(f.tell() / data_info.struct_size)
            f.seek(0, 0)
            #skip dummy entries if necessary
            if(data_set in self.data_set_parts_with_dummy):
                f.seek(data_info.struct_size, 0)
                file_size -= 1

            if(show_loading_bar):
                prog_bar = tqdm(total=file_size, position=0, leave=False)
                prog_bar.set_description("Loading: " + os.path.basename(path) + "   ")

            #iterate over the data set entries
            while(_bytes := f.read(data_info.struct_size)):
                #unpack the packed data
                if(data_info.code.startswith(">")):
                    raw = struct.unpack(data_info.code, _bytes)
                else:
                    raw = bitstring.ConstBitStream(bytes=_bytes)
                    raw = raw.readlist(data_info.code)

                #convert the image and process it if given
                imageF = Image.frombytes('F', data_info.img_size, raw[-1], 'bit', data_info.img_depth)
                img = self.process_image(imageF, resize, data_info.img_depth if normalize else -1)

                #decode the label
                label = data_info.decoder(*[raw[i] for i in data_info.label_index])
                if(label is None):
                    continue
                label = jaconv.h2z(label, kana=True, digit=False, ascii=False)
                label = jaconv.z2h(label, kana=False, digit=True, ascii=True)

                # apply the filter 
                if(self.select_entries(label, include)):
                    imgs.append(img)
                    labels.append(label)

                if(show_loading_bar):
                    prog_bar.update(1)
            
            if(show_loading_bar):
                prog_bar.close()

        #convert lists to numpy arrays
        imgs, lbl = np.array(imgs, dtype="float16"), np.array(labels, dtype="str")
        return imgs, lbl
    
    
    def read_dataset_part(self, data_set : ETLDataNames,
                            include : List[ETLCharacterGroups] = [ETLCharacterGroups.all],
                            processes : int = 1,
                            resize : Tuple[int, int] = (64, 64),
                            normalize : bool = True,
                            save_to : str = "") -> Tuple[np.array, np.array]:
        """Read, process and filter one part (ex.: ETL1) of the ETL data set.
        
        Note:
            The loaded images will be a numpy array with dtype=float16.

        Warning:
            Will throw an error if not all parts of the data set can be found in 'self.path\data_set'.
            Also if the images do not get resized to the same size.
            Throws an FileNotFoundError if the path to save the images to is not valid. 

        Args:
            data_set  : The data set part which should be loaded.
            include   : All character types (Kanji, Hiragana, Symbols, stc.) which should be included.
            processes : The number of processes which should be used for loading the data.
                        Every process will run on a separate CPU core.
                        Therefore it is recommended to not use more than (virtual) processor cores are available.
            resize    : The size the image should be resized (if resize < 1 the images will not be resized). Defaults to (64, 64).
            normalize : Should the gray values be normalized between [0.0, 1.0]. Defaults to True.
            save_to   : If set to a path to a directory all images will be saved there as a jpg image.

        Returns:
            The loaded and filtered data set entries in the form: (images, labels).
        """

        if(processes == 1):
            x, y = self.__read_dataset_part_sequential(data_set, include, resize, normalize)
        elif(processes > 1):
            x, y = self.__read_dataset_part_parallel(data_set, include, processes, resize, normalize)
        else:
            print(processes + "is not a valid amount of processes.")
            print("Loading in sequential mode...")

            x, y = self.__read_dataset_part_sequential(data_set, include, resize, normalize)

        if(save_to != ""):
            self.save_to_file(x, y, save_to)

        return x, y


    def __read_dataset_part_sequential(self, data_set : ETLDataNames,
                            include : List[ETLCharacterGroups] = [ETLCharacterGroups.all],
                            resize : Tuple[int, int] = (64, 64),
                            normalize : bool = True) -> Tuple[np.array, np.array]:
        """Read, process and filter one part (ex.: ETL1) of the ETL data set sequentially.

        This method is the actual sequential implementation of the 'read_dataset_part' method.
        It is run completely in the main process.
        
        Note:
            The loaded images will be a numpy array with dtype=float16.
            This method should only be called through the 'read_dataset_part' method.

        Warning:
            Will throw an error if not all parts of the data set can be found in 'self.path\data_set'.
            Also if the images do not get resized to the same size.

        Args:
            data_set  : The data set part which should be loaded.
            include   : All character types (Kanji, Hiragana, Symbols, stc.) which should be included.
            resize    : The size the image should be resized (if resize < 1 the images will not be resized). Defaults to (64, 64).
            normalize : Should the gray values be normalized between [0.0, 1.0]. Defaults to True.

        Returns:
            The loaded and filtered data set entries in the form: (images, labels).
        """

        imgs, labels = [], []

        print("Loading all data set files (" + data_set.value + "_x) from: " + os.path.join(self.path, data_set.value) + "...", flush=True)

        #regex to check if file is valid
        reg = re.compile((data_set.value + r".*_\d+"))

        #get all ETL files in the directory
        data_set_files = [f for f in os.listdir(os.path.join(self.path, data_set.value)) if not (reg.match(f) is None)]
        print(data_set_files)

        for cnt, file in enumerate(data_set_files, start=1):

            _imgs, _labels = self.read_dataset_file(file, data_set, include, resize=resize, normalize=normalize)

            #make sure that data was loaded and not empty arrays get appended 
            if(len(_imgs) > 0 and len(_labels) > 0):
                imgs.append(_imgs)
                labels.append(_labels)

        #only concatenate if there were arrays loaded
        if(len(imgs) > 0 and len(labels) > 0):
            imgs, labels = np.concatenate(imgs), np.concatenate(labels)
        else:
            imgs, labels = np.empty(shape=0), np.empty(shape=0)

        return imgs, labels

    def __read_dataset_part_parallel(self, data_set : ETLDataNames,
                            include : List[ETLCharacterGroups] = [ETLCharacterGroups.all],
                            processes : int = 1,
                            resize : Tuple[int, int] = (64, 64),
                            normalize : bool = True) -> Tuple[np.array, np.array]:
        """Read, process and filter one part (ex.: ETL1) of the ETL data set in parallel.

        This method is the actual parallel implementation of the 'read_dataset_part' method.
        It is run in 'processes' many subprocesses.

        Note:
            The loaded images will be a numpy array with dtype=float16.
            This method should only be called through the 'read_dataset_part' method.

        Warning:
            Will throw an error if not all parts of the data set can be found in 'self.path\data_set'.
            Also if the images do not get resized to the same size.

        Args:
            data_set  : The data set part which should be loaded.
            include   : All character types (Kanji, Hiragana, Symbols, stc.) which should be included.
            processes : The number of processes which should be used for loading the data.
                        Every process will run on a separate CPU core.
                        Therefore it is recommended to not use more than (virtual) processor cores are available.
            resize    : The size the image should be resized (if resize < 1 the images will not be resized). Defaults to (64, 64).
            normalize : Should the gray values be normalized between [0.0, 1.0]. Defaults to True.

        Returns:
            The loaded and filtered data set entries in the form: (images, labels).
        """

        imgs, labels = [], []

        print("Loading all data set files (" + data_set.value + "_x) from: " + os.path.join(self.path, data_set.value) + "...", flush=True)

        #regex to check if file is valid
        reg = re.compile((data_set.value + r".*_\d+"))

        #get all ETL files in the directory
        data_set_files = [f for f in os.listdir(os.path.join(self.path, data_set.value)) if not (reg.match(f) is None)]

        # get the arguments for all processes
        arguments = []
        for cnt, file in enumerate(data_set_files, start=1):
            arguments.append([file, data_set, include, resize, normalize, False])

        # run the function in all processes
        return_values = []
        with mp.Pool(processes=processes) as pool:
            return_values = pool.starmap(self.read_dataset_file, tqdm(arguments, total=len(arguments)))

        # separate the labels and images
        imgs, labels = [], []
        for img, label in return_values:
            # only append when images were loaded
            if(len(img) > 0):
                imgs.append(img)
            # only append when labels were loaded
            if(len(label) > 0):
                labels.append(label)
        
        #only concatenate if there were arrays loaded
        if(len(imgs) > 0 and len(labels) > 0):
            imgs, labels = np.concatenate(imgs), np.concatenate(labels)
        else:
            imgs, labels = np.empty(shape=0), np.empty(shape=0)

        return imgs, labels


    def read_dataset_whole(self, include : List[ETLCharacterGroups] = [ETLCharacterGroups.all],
                            processes : int = 1,
                            resize : Tuple[int, int] = (64, 64),
                            normalize : bool = True,
                            save_to : str = "") -> Tuple[np.array, np.array]:
        """ Read, process and filter the whole ETL data set (ETL1 - ETL9G).

        Note:
            The loaded images will be a numpy array with dtype=float16.

        Caution:
            Reading the whole dataset with all available entries will use up a lot of memory.

        Warning:
            Will throw an error if not all parts and files of the data set can be found in 'self.path'.
            Also if the images do not get resized to the same size.
            Throws an FileNotFoundError if the path to save the images to is not valid. 

        Arguments:
            include   : All character types (Kanji, Hiragana, Symbols, stc.) which should be included.
            processes : The number of processes which should be used for loading the data.
                        Every process will run on a separate CPU core.
                        Therefore it is recommended to not use more than (virtual) processor cores are available.
            resize    : The size the image should be resized (if resize < 1 the images will not be resized). Defaults to (64, 64).
            normalize : Should the gray values be normalized between [0.0, 1.0]. Defaults to True.
            save_to   : If set to a path to a directory all images will be saved there as a jpg image.

        Returns:
            The loaded and filtered data set entries in the form: (images, labels).
        """
        
        if(processes == 1):
            x, y = self.__read_dataset_whole_sequential(include, resize, normalize)
        elif(processes > 1):
            x, y = self.__read_dataset_whole_parallel(include, processes, resize, normalize)
        else:
            print(processes + "is not a valid amount of processes.")
            print("Loading in sequential mode...")

            x, y = self.__read_dataset_whole_sequential(include, resize, normalize)
        
        self.save_to_file(x, y, save_to)

        return x, y

    def __read_dataset_whole_sequential(self, include : List[ETLCharacterGroups] = [ETLCharacterGroups.all],
                            resize : Tuple[int, int] = (64, 64),
                            normalize : bool = True) -> Tuple[np.array, np.array]:
        """ Read, process and filter the whole ETL data set (ETL1 - ETL9G) sequentially.
        
        This method is the actual parallel implementation of the 'read_dataset_part' method.
        It is run in completely in the main process.

        Note:
            The loaded images will be a numpy array with dtype=float16.
            This method should only be called through the 'read_dataset_whole' method.

        Caution:
            Reading the whole dataset with all available entries will use up a lot of memory.

        Warning:
            Will throw an error if not all parts and files of the data set can be found in 'self.path'.
            Also if the images do not get resized to the same size.

        Arguments:
            include   : All character types (Kanji, Hiragana, Symbols, stc.) which should be included.
            processes : The number of processes which should be used for loading the data.
                        Every process will run on a separate CPU core.
                        Therefore it is recommended to not use more than (virtual) processor cores are available.
            resize    : The size the image should be resized (if resize < 1 the images will not be resized). Defaults to (64, 64).
            normalize : Should the gray values be normalized between [0.0, 1.0]. Defaults to True.

        Returns:
            The loaded and filtered data set entries in the form: (images, labels).
        """
        
        imgs, labels = [], []

        #iterate over all available data_set parts
        for _type in ETLDataNames:

            #read all parts
            _imgs, _labels = self.read_dataset_part(_type, include, resize=resize, normalize=normalize)

            #make sure the loaded data is not an empty array
            if(len(_imgs) > 0 and len(_labels) > 0):
                imgs.append(_imgs)
                labels.append(_labels)
        
        #only concatenate if there were arrays loaded
        if(len(imgs) > 0 and len(labels) > 0):
            imgs, labels = np.concatenate(imgs), np.concatenate(labels)

        return imgs, labels

    def __read_dataset_whole_parallel(self, include : List[ETLCharacterGroups] = [ETLCharacterGroups.all],
                            processes : int = 1,
                            resize : Tuple[int, int] = (64, 64),
                            normalize : bool = True) -> Tuple[np.array, np.array]:
        """ Read, process and filter the whole ETL data set (ETL1 - ETL9G) in multiple processes.
        
        This method is the actual parallel implementation of the 'read_dataset_whole' method.
        It is run in 'processes' many subprocesses.

        Note:
            The loaded images will be a numpy array with dtype=float16.
            This method should only be called through the 'read_dataset_whole' method.

        Caution:
            Reading the whole dataset with all available entries will use up a lot of memory.

        Warning:
            Will throw an error if not all parts and files of the data set can be found in 'self.path'.
            Also if the images do not get resized to the same size.

        Arguments:
            include   : All character types (Kanji, Hiragana, Symbols, stc.) which should be included.
            processes : The number of processes which should be used for loading the data.
                        Every process will run on a separate CPU core.
                        Therefore it is recommended to not use more than (virtual) processor cores are available.
            resize    : The size the image should be resized (if resize < 1 the images will not be resized). Defaults to (64, 64).
            normalize : Should the gray values be normalized between [0.0, 1.0]. Defaults to True.

        Returns:
            The loaded and filtered data set entries in the form: (images, labels).
        """

        imgs, labels = [], []

        #iterate over all available data_set parts
        arguments = []
        for _type in ETLDataNames:

            #regex to check if file is valid
            reg = re.compile((_type.value + r"_\d+"))

            #get all ETL files in the directory
            _type_files = [f for f in os.listdir(os.path.join(self.path, _type.value)) if not (reg.match(f) is None)]

            # get a list of arguments for all processes
            for cnt, file in enumerate(_type_files, start=1):
                arguments.append([file, _type, include, resize, normalize, False])

        # run the function in all processes
        return_values = []
        with mp.Pool(processes=processes) as pool:
            return_values = pool.starmap(self.read_dataset_file, tqdm(arguments, total=len(arguments)))

        #only concatenate if there were arrays loaded
        for _imgs, _labels in return_values: 
            if(len(_imgs) > 0 and len(_labels) > 0):
                imgs.append(_imgs)
                labels.append(_labels)

        return np.concatenate(imgs), np.concatenate(labels)


    def process_image(self, imageF : Image.Image,
                            img_size : Tuple[int, int],
                            img_depth : int) -> np.array:
        """ Processes the given ETL-image.

        The image will be resized to 'img_size' and the color channel depth will be normalized to its 'img_depth'.

        Args:
            imageF    : The image which should be processed.
            img_size  : The size which the image should be resized to (no resizing if any component < 1).
            img_depth : The gray scale depth of the image (no normalization when set to < 1).

        Returns:
            The processed image.
        """

        #convert to 8-bit
        img = imageF.convert('P')

        #resize the image
        if(img_size[0] > 1 and img_size[1] > 1):
            img = img.resize(size=(img_size[1], img_size[0]), resample=Image.ANTIALIAS)

        img = np.array(img)

        #normalize between 0 and 1
        if(img_depth > 1):
            normalization_factor = (2.0 ** img_depth - 1)
            img = img / normalization_factor

        #reshape to separate the color channel
        img = img.reshape(len(img), len(img[0]), 1)

        return img

    def select_entries(self, label : str, include : List[ETLCharacterGroups] = [ETLCharacterGroups.all]) -> bool:
        """ Checks if the given entry given by 'label' should be included in the loaded data set.

        Args:
            label    : The label which should be checked if it should be included.
            include : All character types which should be included.

        Returns:
            bool: True if the entry should be included, False otherwise.
        """

        #if the parameter is unset load everything
        if(not include):
            include = [ETLCharacterGroups.all]

        #list of regex's for filtering the different groups
        regex = "|".join([i.value for i in include])

        #match with regex if label should be included
        reg = re.compile(regex)
        should_include = reg.match(label) 

        return should_include

    def save_to_file(self, x : np.ndarray, y : np.ndarray, save_to : str, name : int = 1):
        """
        Saves all images and labels to file.

        Creates a folder structure in which all images for one label are
        stored in a folder. The names of these folders are the labels encoded
        as an int.
        Additionally a file "encoding.txt" is saved. This file contains a string 
        representaiton of a dict to convert from the int encoding to the matching
        string label. It can be restored with loading the string from disk and than 
        calling `eval()` or `ast.literal_eval()` on this string.

        Warning:
            Throws an FileNotFoundError if the path to save the images to is not valid.

        Args:
            x       : a numpy array containing all images.
            y       : a numpy array containing all labels.
            save_to : the path to the folder where the image and labels should be saved
            name    : an integer from which the names should start (Defaults to 1).
        """
    
        if(save_to != ""):
            if(os.path.isdir(save_to)):

                # create folders for all labels
                unique_labels = np.unique(y)
                class_dict = {}
                for cnt, i in enumerate(unique_labels):
                    cnt += name
                    if(not os.path.isdir(os.path.join(save_to, str(cnt)))):
                        os.mkdir(os.path.join(save_to, str(cnt)))

                    # start counting every class from 0
                    class_dict[i] = [str(cnt), 0]

                # save all images to the matching folders
                with tqdm(total=len(x)) as pbar:
                    for cnt, img in enumerate(x):
                        # image was normalized between (range: [0, 1])
                        if(img.max() <= 1):
                            p_img = ((img * 255).astype(np.uint8)).reshape(img.shape[0], img.shape[1])
                        # image was not normalized (range: [0, 255])
                        else:
                            p_img = (img.astype(np.uint8)).reshape(img.shape[0], img.shape[1])

                        p_img = Image.fromarray(p_img, mode="L")

                        # save to file
                        label = class_dict[y[cnt]][0]
                        label_count = str(class_dict[y[cnt]][1])
                        p_img.save(os.path.join(save_to, label, label_count + ".jpg"))

                        class_dict[y[cnt]][1] += 1

                        pbar.update(1)

                # save the int -> label, count to a file
                with open(os.path.join(save_to, "encoding.txt"), "w+", encoding="utf-8") as f:
                    f.write(str(class_dict).replace("],", "],\n"))


            else:
                raise FileNotFoundError("The given path:", save_to, "is not a valid directory.")
