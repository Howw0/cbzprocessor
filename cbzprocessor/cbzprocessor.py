import os
import xml.etree.ElementTree as ET
from zipfile import ZipFile

class Parser:
    def __init__(self):
        pass


    def get_metadata(self, file: str):
        metadata_filename = 'ComicInfo.xml'
        metadata = {}
        with ZipFile(file, 'r') as myzip:
            files = myzip.namelist()
            try:
                os.mkdir(file)
                pass
            except OSError:
                pass
            if metadata_filename in files:
                with myzip.open(metadata_filename) as metadata_file:
                    tree = ET.parse(metadata_file)
                    root = tree.getroot()
                    metadata = {root.tag: {}}
                    for child in root:
                        metadata[root.tag][child.tag] = child.text
        return metadata


    def parse_cbz(self, file: str, output_dir: str):
        '''
        This function should be called with path to cbz as argument. It will extract images from the cbz and will write them in a folder
        '''
        file_name = os.path.basename(file)
        file_stem = os.path.splitext(file_name)[0]
        folder = os.path.join(output_dir, file_stem) 
        with ZipFile(file, 'r') as myzip:
            files = myzip.namelist()
            try:
                os.mkdir(folder)
                pass
            except OSError:
                pass
            for tmp_file in files:
                file_to_add = os.path.join(folder, tmp_file)
                with open(file_to_add, 'wb') as tmp_img:
                    tmp_img.write(myzip.read(tmp_file))
        return folder


    def parse_dir(self, folder: str, output_dir: str):
        '''
        This function should be called with path to folder as argument. It will extract images from the folder with NO recursivity and will add the images inside a cbz archive
        '''
        folder_name = os.path.basename(folder)
        # opening cbz and parsing folder to find images
        file = os.path.join(output_dir, folder_name + '.cbz')
        # Adding all images in the output cbz
        with ZipFile(file, 'w') as myzip:
            for f in sorted(os.listdir(folder)):
                ext = f[-3:].lower()
                if ext in f:
                    file_to_add = os.path.join(folder, f)
                    myzip.write(file_to_add, arcname=f)
        return file


