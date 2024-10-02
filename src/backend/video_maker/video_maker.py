"""
Project: Aplikace pro oziveni fotek
Author: Adrian Bobola
Email: xbobol00@stud.fit.vutbr.cz
University: FIT VUT Brno
Created on: 2024-05-09
"""

import cv2
import json
import sys
import os

data_list = []
number_of_parts = 0
processed_parts = 0


def load_initial_data(args):
    """
     Spracuvava vstupne parametre a nacitava potrebne subory pre dalsie spracuvanie
     """
    if len(args) < 3:
        print("No command-line parameters provided.")
        sys.exit(1)

    command_line_arguments = args[1:]
    number_of_all_parts = len(command_line_arguments[0].split(' '))
    media_root = command_line_arguments[1]
    img_path = os.path.join(media_root, 'input.jpg')
    json_file = os.path.join(media_root, 'coordinates.json')
    filename_to_find = command_line_arguments[0].split(' ')[0]
    filename_to_find += ".png"
    video_part = command_line_arguments[0].split(' ')[0]
    final_video_name = os.path.join(media_root, f"{video_part}.mp4")

    return (command_line_arguments, number_of_all_parts, media_root, img_path,
            json_file, filename_to_find, final_video_name)


def process_video(command_line_arguments, number_of_parts, media_root, img_path, json_file_path, name_to_find,
                  result_video_name):
    """
     Vytvara video z povodneho obrazku nahradenim jednotlivych bouding-boxov videom.
     Pre nahradenie dalsej oblasti su nacitane snimky z predchazajuceho vytvoreneho videa.
     """

    global processed_parts

    # Kontrola ze dany video subor existuje
    if not os.path.exists(result_video_name):
        print(f"The video file '{result_video_name}' does not exist.")
        sys.exit()

    # Nacitanie suboru so suradnicami bouding-boxov
    with open(json_file_path, 'r') as json_file:
        data_list = json.load(json_file)

    # Hladanie suradnic bouding-boxu pre vybranu cast
    found_item = next((item for item in data_list if item['filename'] == name_to_find), None)

    if found_item:
        # Najdene suradnice bouding-boxov pre pozadovanu cast
        original_image_name = found_item['filename']
        head_top = found_item['head_top']
        head_bottom = found_item['head_bottom']
        head_left = found_item['head_left']
        head_right = found_item['head_right']

        # Pomocny vypis suradnic do logovacieho suboru
        print("Coordinates for", original_image_name, "are:")
        print("Head Top:", head_top)
        print("Head Bottom:", head_bottom)
        print("Head Left:", head_left)
        print("Head Right:", head_right)
    else:
        print("Coordinates not found for ", name_to_find)
        exit(1)

    # Nacitanie rozpohybovaneho videa a zistenie jeho frekvencie snimok vo videu
    animated_part_cap = cv2.VideoCapture(result_video_name)
    fps = animated_part_cap.get(cv2.CAP_PROP_FPS)
    print(f"Frames per second (FPS): {fps}")

    # Nacitanie povodneho obrazku do ktoreho sa ma nahradit cast s videom
    original_image = cv2.imread(img_path)
    output_path = os.path.join(media_root, 'output.mp4')
    output_video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps,
                                   (original_image.shape[1], original_image.shape[0]))

    while True:
        success, animated_part = animated_part_cap.read()
        if not success:
            break

        # Uprava suradnic pre neziaduce stavy a nastavenie velkosti oblasti pre video s pohybom
        region_width = head_right - head_left
        if region_width <= 0:
            region_width = 1
        region_height = head_bottom - head_top
        if region_height <= 0:
            region_height = 1
        animated_part_resized = cv2.resize(animated_part, (region_width, region_height))

        # Zistovanie suradnic pre vlozenu cast vida do obrazka
        region_top = head_top
        region_bottom = head_top + animated_part_resized.shape[0]
        region_left = head_left
        region_right = head_left + animated_part_resized.shape[1]

        # Vlozenie videa do pozadovanej casti obrazka
        result = original_image.copy()
        result[region_top:region_bottom, region_left:region_right] = animated_part_resized
        output_video.write(result)

        # Ukoncenie behu programu uzivatelskym vstupom
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Zatvaranie suborov a nastavovanie parametrov
    animated_part_cap.release()
    output_video.release()
    processed_parts += 1
    cv2.destroyAllWindows()
    previous_frame = None

    while processed_parts < number_of_parts:
        # Je viac nez jedna oblast v obrazku, ktoru treba nahradit videom

        # nacitaj parametre predchadzajuceho vytvoreneho videa, do ktoreho sa bude vkladat dalsie video
        video_path = os.path.join(media_root, 'output.mp4')
        input_video = cv2.VideoCapture(video_path)
        fps = int(input_video.get(cv2.CAP_PROP_FPS))
        frame_size = (int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output2_path = os.path.join(media_root, 'output2.mp4')
        output_video = cv2.VideoWriter(output2_path, fourcc, fps, frame_size)
        video_part = command_line_arguments[0].split(' ')[processed_parts]
        result_video_name = os.path.join(media_root, f"{video_part}.mp4")
        if not os.path.exists(result_video_name):
            print(f"The video file '{result_video_name}' does not exist.")
            sys.exit()

        # Hladanie suradnic bouding-boxu pre pozadovanu cast
        name_to_find = command_line_arguments[0].split(' ')[processed_parts]
        name_to_find += ".png"
        found_item = next((item for item in data_list if item['filename'] == name_to_find), None)

        if found_item:
            # Najdene suradnice bouding-boxov pre pozadovanu cast
            original_image_name = found_item['filename']
            head_top = found_item['head_top']
            head_bottom = found_item['head_bottom']
            head_left = found_item['head_left']
            head_right = found_item['head_right']

            # Pomocny vypis suradnic do logovacieho suboru
            print("Coordinates for", original_image_name, "are:")
            print("Head Top:", head_top)
            print("Head Bottom:", head_bottom)
            print("Head Left:", head_left)
            print("Head Right:", head_right)
        else:
            print("Coordinates not found for", name_to_find)
            exit(1)

        animated_part_cap = cv2.VideoCapture(result_video_name)
        while True:
            success, animated_part = animated_part_cap.read()
            ret, frame = input_video.read()
            if not success:
                break

            # Uprava suradnic pre neziaduce stavy a nastavenie velkosti oblasti pre video s pohybom
            region_width = head_right - head_left
            if region_width <= 0:
                region_width = 1
            region_height = head_bottom - head_top
            if region_height <= 0:
                region_height = 1
            animated_part_resized = cv2.resize(animated_part, (region_width, region_height))

            # Zistovanie suradnic pre vlozenu cast vida do obrazka
            region_top = head_top
            region_bottom = head_top + animated_part_resized.shape[0]
            region_left = head_left
            region_right = head_left + animated_part_resized.shape[1]

            if frame is None:
                if previous_frame is not None:
                    result = previous_frame.copy()
                    # Nahradenie vypocitanej oblasti v snimku s novym videom
                    result[region_top:region_bottom, region_left:region_right] = animated_part_resized
                    output_video.write(result)
                break
            else:
                result = frame.copy()
                # Nahradenie vypocitanej oblasti v snimku s novym videom
                result[region_top:region_bottom, region_left:region_right] = animated_part_resized
                output_video.write(result)
            previous_frame = frame.copy()

            # Ukoncenie behu programu uzivatelskym vstupom
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Zatvaranie suborov a nastavovanie parametrov, je nutne odstranit povodne video output.mp4
        # Je potrebne potom premenovat ouput2.mp4 na output.mp4
        animated_part_cap.release()
        output_video.release()
        original_file_path = os.path.join(media_root, 'output.mp4')
        new_file_path = os.path.join(media_root, 'output2.mp4')
        os.remove(original_file_path)
        os.rename(new_file_path, original_file_path)
        processed_parts += 1


if __name__ == "__main__":
    cmd_args, num_parts, root, image_path, json_file_path, name_to_find, result_video_name = load_initial_data(sys.argv)
    process_video(cmd_args, num_parts, root, image_path, json_file_path, name_to_find, result_video_name)
