"""
------------------------------------------------------------------------------------------------------------------------
Zdrojovy kod v adresari /backend/face_reenactment/ je prevzaty z: https://github.com/sky24h/Face_Animation_Real_Time
Povodny autor kodu: sky24h
------------------------------------------------------------------------------------------------------------------------
Upraveny bol iba subor: /backend/face_reenactment/camera_local.py
Tieto zmeny su oznacene blokovym komentarom
------------------------------------------------------------------------------------------------------------------------
"""

import cv2
import time
import numpy as np
import os
import subprocess

from argparse import ArgumentParser
from demo_utils import FaceAnimationClass


class VideoCamera(object):
    def __init__(self, video_path=0, CameraSize=(640, 480)):
        self.video_path = video_path
        self.video = cv2.VideoCapture(video_path) if video_path != 0 else cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, CameraSize[0])
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, CameraSize[1])
        self.video.set(cv2.CAP_PROP_FPS, 24)
        if video_path == 0 and not self.video.isOpened():
            raise Exception("Camera not found")
        elif video_path != 0 and not self.video.isOpened():
            raise Exception("Video file not found")

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        image = cv2.flip(image, 1) if self.video_path == 0 else image
        return image


def process_frame(image, ScreenSize=512):
    face, result = faceanimation.inference(image)
    if face.shape[1] != ScreenSize or face.shape[0] != ScreenSize:
        face = cv2.resize(face, (ScreenSize, ScreenSize))
    if result.shape[0] != ScreenSize or result.shape[1] != ScreenSize:
        result = cv2.resize(result, (ScreenSize, ScreenSize))
    return result


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--source_image", default="./assets/source.jpg", help="path to source image")
    parser.add_argument("--driving_video", default=None, help="path to driving video")
    parser.add_argument("--result_video", default="./result_video.mp4", help="path to output")
    parser.add_argument("--output_size", default=512, type=int, help="size of the output video")
    parser.add_argument("--restore_face", default=False, type=str, help="restore face")
    args = parser.parse_args()

    """
    ------------------------------------------------------------------------------------------------------------------------
    Zaciatok upravy c.1
    Author: Adrian Bobola
    ------------------------------------------------------------------------------------------------------------------------
    """
    # restore_face = True if args.restore_face == 'True' else False if args.restore_face == 'False' else exit('restore_face must be True or False')
    #
    # if args.driving_video is None:
    #     video_path = 0
    #     print("Using webcam")
    #     # create window for displaying results
    #     cv2.namedWindow("Face Animation", cv2.WINDOW_NORMAL)
    # else:
    #     video_path = args.driving_video
    #     print("Using driving video: {}".format(video_path))

    # Vytvorenie cesty k suborom
    source_image_directory = os.path.dirname(args.source_image)
    source_image_name = os.path.splitext(os.path.basename(args.source_image))[0]
    driving_video_path_mp4 = f"{source_image_directory}/{source_image_name}_driving.mp4"
    driving_video_path_webm = f"{source_image_directory}/{source_image_name}_driving.webm"

    # Kontrola existencie video suboru vo formate .mp4 alebo .webm
    if os.path.exists(driving_video_path_mp4):
        video_path = driving_video_path_mp4
    elif os.path.exists(driving_video_path_webm):
        video_path = driving_video_path_webm
    else:
        # Pokus o konverziu suboru .MOV, .avi, .mkv alebo .quicktime na subor .mp4
        video_files = [f for f in os.listdir(source_image_directory) if
                       f.startswith(source_image_name + "_driving")
                       and
                       f.endswith(('.MOV', '.avi', '.mkv', '.quicktime'))]
        if video_files:
            # Konvertuj video pomocou ffmpeg skriptu
            source_video_path = os.path.join(source_image_directory, video_files[0])
            video_path = driving_video_path_mp4
            command = f"ffmpeg -i {source_video_path} -vcodec h264 -acodec aac {video_path}"
            try:
                subprocess.run(command, shell=True, check=True)
                print(f"Converted {source_video_path} to {video_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error converting video: {str(e)}")
                exit(1)
        else:
            print(f"Error: No video found. Video name: {source_image_name}")
            exit(1)

    # camera = VideoCamera(video_path=video_path)
    # faceanimation = FaceAnimationClass(source_image_path=args.source_image, use_sr=restore_face)
    # frames = [] if args.result_video is not None else None

    camera = VideoCamera(video_path=video_path)
    faceanimation = FaceAnimationClass(source_image_path=args.source_image, use_sr=False)
    output_video_path = f"{source_image_directory}/{source_image_name}.mp4"
    frames = [] if output_video_path is not None else None

    """
    ------------------------------------------------------------------------------------------------------------------------
    Koniec upravy c.1
    ------------------------------------------------------------------------------------------------------------------------
    """

    frame_count = 0
    times = []
    while True:
        time_start = time.time()
        image = camera.get_frame()
        if image is None and frame_count != 0:
            print("Video ended")
            break
        try:
            res = process_frame(image, ScreenSize=args.output_size)
            frame_count += 1
            times.append(time.time() - time_start)
            if frame_count % 100 == 0:
                print("FPS: {:.2f}".format(1 / np.mean(times)))
                times = []
            frames.append(res) if output_video_path is not None else None

            """
            ------------------------------------------------------------------------------------------------------------
            Zaciatok upravy c.2
            Author: Adrian Bobola
            ------------------------------------------------------------------------------------------------------------
            """
        #         # display results if using webcam
        #         if args.driving_video is None:
        #             cv2.imshow("Face Animation", res)
        #             if cv2.waitKey(1) & 0xFF == ord("q"):
        #                 break
        #     except Exception as e:
        #         print(e)
        #         raise e

        except Exception as e:
            print(e)
            raise e
        """
        ------------------------------------------------------------------------------------------------------------------------
        Koniec upravy c.2
        ------------------------------------------------------------------------------------------------------------------------
        """

    """
    ------------------------------------------------------------------------------------------------------------
    Zaciatok upravy c.3
    Author: Adrian Bobola
    ------------------------------------------------------------------------------------------------------------
    """
    # if args.result_video is not None:
    #     import imageio
    #     from tqdm import tqdm
    #
    #     writer = imageio.get_writer(args.result_video, fps=24, quality=9, macro_block_size=1, codec="libx264", pixelformat="yuv420p")
    #     for frame in tqdm(frames):
    #         writer.append_data(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    #     writer.close()
    #     print("Video saved to {}".format(args.result_video))

    if output_video_path is not None:
        import imageio
        from tqdm import tqdm

        writer = imageio.get_writer(output_video_path, fps=24, quality=9, macro_block_size=1, codec="libx264",
                                    pixelformat="yuv420p")
        for frame in tqdm(frames):
            writer.append_data(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        writer.close()
        print("Video saved to {}".format(output_video_path))
    """
    ------------------------------------------------------------------------------------------------------------
    Koniec upravy c.3
    ------------------------------------------------------------------------------------------------------------
    """
