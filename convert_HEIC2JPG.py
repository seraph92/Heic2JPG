import datetime
import logging
# from logging import info as INFO, error as ERROR, debug as DEBUG
from Logging import info as INFO, error as ERROR, debug as DEBUG
from posixpath import basename
from PIL import Image
from PIL.ExifTags import TAGS
# from pillow_heif import register_heif_opener
import os
import pyheif
import piexif
import exifread

logger = logging.getLogger(__name__)

# register_heif_opener()
def read_exif(file_path):
     with open(heic_file_path, "rb") as f:
        tags = exifread.process_file(f)
        return tags
   

def convert_heic_to_jpg(heic_file_path, output_folder=None, quality=85):
    # get save folder
    if not output_folder :
        output_folder = os.path.dirname(heic_file_path)
    INFO(output_folder)

    try :
        heic_image = pyheif.read(heic_file_path)
    except ValueError as e:
        ERROR(f"{e=}")
        return False

    exif_tags = read_exif(heic_file_path)
    for tag, value in exif_tags.items():
        DEBUG(f"{tag}:{value}")
        if 'DateTimeOriginal' in tag:
            DEBUG(f"DateTimeOriginal : {value}")

    # Convert HEIC to RGB mode
    rgb_image = Image.frombytes(
        heic_image.mode, 
        heic_image.size, 
        heic_image.data,
        "raw",
        heic_image.mode,
        heic_image.stride,
    )

    exif_dict = piexif.load(heic_image.metadata[0]['data'])
    exif_bytes = piexif.dump(exif_dict)

    # Get the filename without extension
    filename = os.path.splitext(os.path.basename(heic_file_path))[0]
    
    # Save the RGB image as JPG
    output_path = os.path.join(output_folder, f"{filename}.jpg")

    rgb_image.save(output_path, format="JPEG", quality=quality, exif=exif_bytes)
    
    INFO(f"Converted {heic_file_path} to {output_path}")


if __name__ == "__main__":
    import sys

    INFO('Started')

    if len(sys.argv) < 2:
        ERROR(f"Usage: {basename(sys.argv[0])} [heic_files]")
        exit(-1)

    for heic_file_path in sys.argv[1:]:
        convert_heic_to_jpg(heic_file_path, quality=50)

    INFO('Finished')
