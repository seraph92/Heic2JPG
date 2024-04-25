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


    # image = Image.open(heic_file_path)
    # exif_data = image._exif
    # print(exif_data)
    # if exif_data:
    #     for tag, value in exif_data.items():
    #         tag_name = TAGS.get(tag, tag)
    #         if tag_name == 'DateTimeOriginal':
    #             print(value)

    # metadata = heic_image.metadata
    # for item in metadata or []:
    #     if 'Exif' in item['type']:
    #         exif_data = item['data']
            # print(exif_data)
            #exif_dict = pyheif.exif_read_dict(exif_data)
            # exif_dict = pyheif.l
            # if 'DateTimeOriginal' in exif_dict:
            #     date_str = exif_dict['DateTimeOriginal']
            #     print(datetime.strptime(date_str.decode(), '%Y:%m:%d %H:%M:%S'))
    
    # Convert HEIC to RGB mode
    rgb_image = Image.frombytes(
        heic_image.mode, 
        heic_image.size, 
        heic_image.data,
        "raw",
        heic_image.mode,
        heic_image.stride,
    )

    # img_info = rgb_image._getexif()
    # for tag_id in img_info:
    #     tag = TAGS.get(tag_id, tag_id)
    #     data = img_info.get(tag_id)
    #     print(f'{tag} : {data}')

    # Get metadata from the HEIC file
    # print(heic_image.metadata)
    # exif_dict = piexif.load(heic_image.metadata['Exif'])
    exif_dict = piexif.load(heic_image.metadata[0]['data'])
    # print(exif_dict)
    # exif_dict = piexif.load(heic_file_path)
    exif_bytes = piexif.dump(exif_dict)
    # print(exif_bytes)

    # Get metadata from the HEIC file
    # heic_metadata = dict(heic_image.metadata or {})

    # Get the filename without extension
    filename = os.path.splitext(os.path.basename(heic_file_path))[0]
    
    # Save the RGB image as JPG
    output_path = os.path.join(output_folder, f"{filename}.jpg")
    # rgb_image.save(output_path, format="JPEG")
    # rgb_image.save(output_path, format="JPEG", quality=quality)
    # rgb_image.save(output_path, format="JPEG", quality=quality, exif=heic_metadata.get('Exif', b''))
    # rgb_image.save(output_path, format="JPEG", quality=quality, exif=heic_metadata.get('data', b''))
    rgb_image.save(output_path, format="JPEG", quality=quality, exif=exif_bytes)
    
    INFO(f"Converted {heic_file_path} to {output_path}")


if __name__ == "__main__":
    import sys

    # LOG_DIR="./log"
    # LOG_FILE="running.log"
    # LOG_PATH=os.path.join(LOG_DIR, LOG_FILE)
    # if not os.path.exists(LOG_DIR):
    #     os.makedirs(LOG_DIR)
    # logging.basicConfig(filename=f"{LOG_PATH}", level=logging.WARNING)
    # logging.basicConfig(filename=f"{LOG_PATH}", level=logging.DEBUG)
    # logging.basicConfig(format='(%(asctime)s) %(levelname)s:%(message)s', datefmt ='%m/%d %I:%M:%S %p', level=logging.DEBUG)
    INFO('Started')

    if len(sys.argv) < 2:
        ERROR(f"Usage: {basename(sys.argv[0])} [heic_files]")
        exit(-1)

    # basedir_name = sys.argv[1]
    # base_name = basename(basedir_name)
    # file_name = sys.argv[2]

    # Example usage
    # heic_file_path = "example.heic"  # Replace with your HEIC file path
    # output_folder = "output"          # Replace with your desired output folder
    # convert_heic_to_jpg(heic_file_path)

    for heic_file_path in sys.argv[1:]:
        # print(heic_file_path)
        convert_heic_to_jpg(heic_file_path, quality=50)

    INFO('Finished')
    # if not os.path.exists(output_folder):
    #     os.makedirs(output_folder)
