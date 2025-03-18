import os
import zipfile



name_mapping = {
    "ETL1"  : "ETL1",
    "ETL2"  : "ETL2",
    "ETL3"  : "ETL3",
    "ETL4"  : "ETL4",
    "ETL5"  : "ETL5",
    "ETL6"  : "ETL6",
    "ETL7"  : "ETL7",
    "ETL8B" : "ETL8",
    "ETL8G" : "ETL9",
    "ETL9B" : "ETL10",
    "ETL9G" : "ETL11",
}

def extract_etlcdb(path : str):
    """ Extracts and pre-processes the etlcdb download for use with this package.
    """

    zips = [z for z in os.listdir(path) if z.endswith(".zip")]

    for z in zips:
        zp = os.path.join(path, z)
        with zipfile.ZipFile(zp, 'r') as zip_ref:
            name = os.path.basename(os.path.normpath(zp))[:-4]

            if(name.startswith("ETL")):
                uzp = os.path.join(path, name_mapping[name])
                zip_ref.extractall(path)
                os.rename(os.path.join(path, name), uzp)

                for file in os.listdir(uzp):
                    os.rename(
                        os.path.join(uzp, file),
                        os.path.join(uzp, file.replace(name, name_mapping[name]))
                    )

    with zipfile.ZipFile(os.path.join(path, "unpack.zip"), 'r') as zip_ref:
        zip_ref.extractall(path)

if __name__ == "__main__":
    extract_etlcdb("/mnt/raid0/data_sets/etlcdb")