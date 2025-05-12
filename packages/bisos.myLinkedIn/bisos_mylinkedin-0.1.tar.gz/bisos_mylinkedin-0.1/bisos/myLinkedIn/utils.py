import csv
import os

from pathlib import Path
import zipfile


class VCardUtils:
    """
    Utility functions for handling vCards and LinkedIn data files.
    """

    @staticmethod
    def get_linkedin_id(url):
        """
        Extract the LinkedIn ID from the profile URL.
        """
        return url.split('/')[-2]

    @staticmethod
    def read_csv(file_path):
        """
        Read a CSV file and return the rows as a list of dictionaries.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} does not exist.")

        with open(file_path, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))

    @staticmethod
    def write_vcard(vcard, vcard_path):
        """
        Write the vCard object to a file.
        """
        with open(vcard_path, 'w', encoding='utf-8') as vcard_file:
            vcard_file.write(vcard.serialize())

    @staticmethod
    def read_vcard(vcard_path):
        """
        Read a vCard from a file and return the vCard object.
        """
        with open(vcard_path, 'r', encoding='utf-8') as vcard_file:
            return vobject.readOne(vcard_file.read())

    @staticmethod
    def find_vcard(vcard_dir, uid):
        """
        Find the vCard file corresponding to the LinkedIn ID (UID) in the directory.
        """
        vcard_path = os.path.join(vcard_dir, f"{uid}.vcf")
        if os.path.exists(vcard_path):
            return vcard_path
        return None

    
class LinkedinBaseUtils:

    @staticmethod
    def unzip_file(zip_path: Path, extract_to: Path) -> None:
        """Unzips a .zip file to the specified directory using pathlib.
        Use it like so: unzip_file(Path("LinkedInDataExport.zip"), Path("unzipped"))
        """
        extract_to.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
