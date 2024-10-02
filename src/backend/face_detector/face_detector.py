"""
Project: Aplikace pro oziveni fotek
Author: Adrian Bobola
Email: xbobol00@stud.fit.vutbr.cz
University: FIT VUT Brno
Created on: 2024-05-09
"""

import cv2
import os
import sys
import json

all_cropped_images_coordinates = []
face_counter = 0


def process_image(input_image_path):
    """
    Automaticky deteguje tvare na fotografii. Nasledne vytvori bounding-boxy okolo jednotlivych tvari a oreze vstupnu
    fotografiu na obrazky jednotlivych tvari osob.

    Parameters:
        input_image_path (str) - Cesta k obrazku

    Returns:
        0 - Detekcia aj orez prebehlo bez problemov
        1 - Nie je mozne nacitat obrazok v zadanej ceste
    """
    global face_counter
    global all_cropped_images_coordinates
    img = cv2.imread(input_image_path)

    if img is not None:
        face_counter = 0
        max_height, max_width = img.shape[:2]

        # Detektor tvari na fotografii
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

        # iteracia cez detegovane suradnice vsetkych tvari
        for (x, y, w, h) in faces:
            # Uprava suradnic pre zvacsenie bounding-boxu okolo celej tvare vratane vlasov
            head_left = int(x - int(0.5 * w))
            head_top = int(y - int(0.5 * h))
            head_right = int(x + w + int(0.5 * w))
            head_bottom = int(y + int(2 * h))

            # Uprava suradnic bounding-boxu ak nejaka presahuje mimo fotografiu
            if head_left < 0:
                head_left = 0
            if head_top < 0:
                head_top = 0
            if head_right > max_width - 1:
                head_right = max_width - 1
            if head_bottom > max_height - 1:
                head_bottom = max_height - 1

            # Orezanie fotografie podla suradnic bounding-boxu
            cropped_img = img[head_top:head_bottom, head_left:head_right]
            cropped_img_coords = [str(face_counter) + '.png', head_top, head_bottom, head_left, head_right]
            all_cropped_images_coordinates.append(cropped_img_coords)

            # Ulozenie orezanej fotografie
            filename = str(face_counter) + '.png'
            directory_path = os.path.dirname(input_image_path)
            output_path = os.path.join(directory_path, filename)
            cv2.imwrite(output_path, cropped_img)
            face_counter += 1

        return 0
    else:
        print(f"Error: Unable to open the image at {input_image_path}")
        return 1


def create_coordinates_file(input_image_path):
    """
    Vytvara subor coordinates.json pre kazdu z orezanych oblasti na obrazku v adresari s povodnym obrazkom.
    Subor obsahuje nazov vytvoreneho obrazku a jeho suradnice v povodnom obrazku.

    Parameters:
        input_image_path (str) -  Cesta k obrazku

    Returns:
        face_counter (int) - Pocet orezanych fotografii
    """
    global face_counter
    global all_cropped_images_coordinates
    json_data = []

    # iteracia cez suradnice vsetkych orezanych fotografii a priprava dat pre JSON format
    for i in range(len(all_cropped_images_coordinates)):
        json_data.append({
            'filename': all_cropped_images_coordinates[i][0],
            'head_top': all_cropped_images_coordinates[i][1],
            'head_bottom': all_cropped_images_coordinates[i][2],
            'head_left': all_cropped_images_coordinates[i][3],
            'head_right': all_cropped_images_coordinates[i][4],
        })

    # Zistenie adresara pre ulozenie suradnic a ulozenie suradnic do suboru coordinates.json
    json_file_path = input_image_path.replace('/input.jpg', '/coordinates.json')
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)

    cv2.destroyAllWindows()
    return face_counter


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python face_detector.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    if process_image(image_path) == 0:
        output = create_coordinates_file(image_path)
        print(output)
    else:
        print("Unable to open the image")
        sys.exit(1)
