"""
------------------------------------------------------------------------------------------------------------------------
Zdrojovy kod v adresari /backend/face_reenactment/ je prevzaty z: https://github.com/sky24h/Face_Animation_Real_Time
Povodny autor kodu: sky24h
------------------------------------------------------------------------------------------------------------------------
Upraveny bol iba subor: /backend/face_reenactment/camera_local.py
------------------------------------------------------------------------------------------------------------------------
"""

"""
@paper: GAN Prior Embedded Network for Blind Face Restoration in the Wild (CVPR2021)
@author: yangxy (yangtao9009@gmail.com)
"""
import os
import cv2
import glob
import time
import argparse
import numpy as np
from PIL import Image
from skimage import transform as tf

import GPEN.__init_paths as init_paths
from GPEN.retinaface.retinaface_detection import RetinaFaceDetection
from GPEN.face_model.face_gan import FaceGAN
from GPEN.sr_model.real_esrnet import RealESRNet
from GPEN.align_faces import warp_and_crop_face, get_reference_facial_points

def check_ckpts(model, sr_model):
    # check if checkpoints are downloaded
    try:
        ckpts_folder = os.path.join(os.path.dirname(__file__), "weights")
        if not os.path.exists(ckpts_folder):
            print("Downloading checkpoints...")
            from gdown import download_folder
            file_id = "1epln5c8HW1QXfVz6444Fe0hG-vRNavi6"
            download_folder(id=file_id, output=ckpts_folder, quiet=False, use_cookies=False)
        else:
            print("Checkpoints already downloaded, skipping...")
    except Exception as e:
        print(e)
        raise Exception("Error while downloading checkpoints")


class FaceEnhancement(object):
    def __init__(self, base_dir=os.path.dirname(__file__), size=512, model=None, use_sr=True, sr_model=None, channel_multiplier=2, narrow=1, use_facegan=True):
        check_ckpts(model, sr_model)

        self.facedetector = RetinaFaceDetection(base_dir)
        self.facegan = FaceGAN(base_dir, size, model, channel_multiplier, narrow)
        self.srmodel = RealESRNet(base_dir, sr_model)
        self.use_sr = use_sr
        self.size = size
        self.threshold = 0.9
        self.use_facegan = use_facegan

        # the mask for pasting restored faces back
        self.mask = np.zeros((512, 512), np.float32)
        cv2.rectangle(self.mask, (26, 26), (486, 486), (1, 1, 1), -1, cv2.LINE_AA)
        self.mask = cv2.GaussianBlur(self.mask, (101, 101), 11)
        self.mask = cv2.GaussianBlur(self.mask, (101, 101), 11)

        self.kernel = np.array(([0.0625, 0.125, 0.0625], [0.125, 0.25, 0.125], [0.0625, 0.125, 0.0625]), dtype="float32")

        # get the reference 5 landmarks position in the crop settings
        default_square = True
        inner_padding_factor = 0.25
        outer_padding = (0, 0)
        self.reference_5pts = get_reference_facial_points((self.size, self.size), inner_padding_factor, outer_padding, default_square)

    def process(self, img):
        if self.use_sr:
            img_sr = self.srmodel.process(img)
            if img_sr is not None:
                img = cv2.resize(img, img_sr.shape[:2][::-1])

        facebs, landms = self.facedetector.detect(img)

        orig_faces, enhanced_faces = [], []
        height, width = img.shape[:2]
        full_mask = np.zeros((height, width), dtype=np.float32)
        full_img = np.zeros(img.shape, dtype=np.uint8)

        for i, (faceb, facial5points) in enumerate(zip(facebs, landms)):
            if faceb[4] < self.threshold:
                continue
            fh, fw = (faceb[3] - faceb[1]), (faceb[2] - faceb[0])

            facial5points = np.reshape(facial5points, (2, 5))

            of, tfm_inv = warp_and_crop_face(img, facial5points, reference_pts=self.reference_5pts, crop_size=(self.size, self.size))

            # enhance the face
            ef = self.facegan.process(of) if self.use_facegan else of

            orig_faces.append(of)
            enhanced_faces.append(ef)

            tmp_mask = self.mask
            tmp_mask = cv2.resize(tmp_mask, ef.shape[:2])
            tmp_mask = cv2.warpAffine(tmp_mask, tfm_inv, (width, height), flags=3)

            if min(fh, fw) < 100:  # gaussian filter for small faces
                ef = cv2.filter2D(ef, -1, self.kernel)

            tmp_img = cv2.warpAffine(ef, tfm_inv, (width, height), flags=3)

            mask = tmp_mask - full_mask
            full_mask[np.where(mask > 0)] = tmp_mask[np.where(mask > 0)]
            full_img[np.where(mask > 0)] = tmp_img[np.where(mask > 0)]

        full_mask = full_mask[:, :, np.newaxis]
        if self.use_sr and img_sr is not None:
            img = cv2.convertScaleAbs(img_sr * (1 - full_mask) + full_img * full_mask)
        else:
            img = cv2.convertScaleAbs(img * (1 - full_mask) + full_img * full_mask)

        return img, orig_faces, enhanced_faces


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="GPEN-BFR-512", help="GPEN model")
    parser.add_argument("--size", type=int, default=512, help="resolution of GPEN")
    parser.add_argument("--channel_multiplier", type=int, default=2, help="channel multiplier of GPEN")
    parser.add_argument("--narrow", type=float, default=1, help="channel narrow scale")
    parser.add_argument("--use_sr", action="store_true", help="use sr or not")
    parser.add_argument("--sr_model", type=str, default="realesrnet_x2", help="SR model")
    parser.add_argument("--sr_scale", type=int, default=2, help="SR scale")
    parser.add_argument("--indir", type=str, default="examples/imgs", help="input folder")
    parser.add_argument("--outdir", type=str, default="results/outs-BFR", help="output folder")
    args = parser.parse_args()

    # model = {'name':'GPEN-BFR-512', 'size':512, 'channel_multiplier':2, 'narrow':1}
    # model = {'name':'GPEN-BFR-256', 'size':256, 'channel_multiplier':1, 'narrow':0.5}

    os.makedirs(args.outdir, exist_ok=True)

    faceenhancer = FaceEnhancement(
        size=args.size,
        model=args.model,
        use_sr=args.use_sr,
        sr_model=args.sr_model,
        channel_multiplier=args.channel_multiplier,
        narrow=args.narrow,
    )

    files = sorted(glob.glob(os.path.join(args.indir, "*.*g")))
    for n, file in enumerate(files[:]):
        filename = os.path.basename(file)

        im = cv2.imread(file, cv2.IMREAD_COLOR)  # BGR
        if not isinstance(im, np.ndarray):
            print(filename, "error")
            continue
        # im = cv2.resize(im, (0,0), fx=2, fy=2) # optional

        img, orig_faces, enhanced_faces = faceenhancer.process(im)

        im = cv2.resize(im, img.shape[:2][::-1])
        cv2.imwrite(os.path.join(args.outdir, ".".join(filename.split(".")[:-1]) + "_COMP.jpg"), np.hstack((im, img)))
        cv2.imwrite(os.path.join(args.outdir, ".".join(filename.split(".")[:-1]) + "_GPEN.jpg"), img)

        for m, (ef, of) in enumerate(zip(enhanced_faces, orig_faces)):
            of = cv2.resize(of, ef.shape[:2])
            cv2.imwrite(os.path.join(args.outdir, ".".join(filename.split(".")[:-1]) + "_face%02d" % m + ".jpg"), np.hstack((of, ef)))

        if n % 10 == 0:
            print(n, filename)
