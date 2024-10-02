"""
Project: Aplikace pro oziveni fotek
Author: Adrian Bobola
Email: xbobol00@stud.fit.vutbr.cz
University: FIT VUT Brno
Created on: 2024-05-09
"""

import cv2
import sys
import json


def custom_image_cropping(image_location, output_image_named, x1, y1, width1, height1):
    """
    Orezava obrazok podla poskytnutych suradnic a upravuje subor so suradnicami orezanych oblasti

    Parameters:
        image_location (str) -  Cesta k obrazku
        output_image_named (str) -  Nazov pre exportovanie orezaneho obrazku
        x1, y1, width1, height1 (int) - Suradnice bounding-boxu pre orezanie obrazku

    Returns:
        0 - Orez prebehol bez problemov
        1 - Nie je mozne nacitat obrazok v zadanej ceste
    """
    img = cv2.imread(image_location)

    if img is not None:
        x1, y1, width1, height1 = map(int, [x1, y1, width1, height1])

        # Vypocet suradnic pre orezanie obrazku a jeho orez
        x2 = x1 + width1
        y2 = y1 + height1
        cropped_img = img[y1:y2, x1:x2]

        # Ulozenie orezaneho obrazku do adresara s povodnym suborom pod nazvom poskytnutom z argumentu sputenia
        filename = output_image_named + '.png'
        image_path2 = image_location.replace('input.jpg', filename)
        cv2.imwrite(image_path2, cropped_img)

        # Ziskanie cesty pre existujuci subor so suradnicami a nacitanie dat z neho do pomocnej premennej
        json_file_path = image_location.replace('/input.jpg', '/coordinates.json')
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        # Pridanie novych dat z orezaneho obrazku do pomocnej premennej
        new_data = {
            'filename': filename,
            'head_top': y1,
            'head_bottom': y1 + height1,
            'head_left': x1,
            'head_right': x1 + width1,
        }
        data.append(new_data)

        # Ulozenie vsetkych povodnych a novo pridanych dat naspat do suboru coordinates.json
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)

    else:
        print(f"Error: Unable to open the image at {image_location}")
        return 1

    cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python custom_image_cropping.py <image_path> <output_image_name> <x> <y> <width> <height>")
        sys.exit(1)

    # Spracuvanie argumentov zadanych v prikazovom riadku
    image_path = sys.argv[1]
    output_image_name = sys.argv[2]
    x = int(float(sys.argv[3]))
    y = int(float(sys.argv[4]))
    width = int(float(sys.argv[5]))
    height = int(float(sys.argv[6]))
    custom_image_cropping(image_path, output_image_name, x, y, width, height)
