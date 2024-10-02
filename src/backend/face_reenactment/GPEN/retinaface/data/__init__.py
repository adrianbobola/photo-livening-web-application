"""
------------------------------------------------------------------------------------------------------------------------
Zdrojovy kod v adresari /backend/face_reenactment/ je prevzaty z: https://github.com/sky24h/Face_Animation_Real_Time
Povodny autor kodu: sky24h
------------------------------------------------------------------------------------------------------------------------
Upraveny bol iba subor: /backend/face_reenactment/camera_local.py
------------------------------------------------------------------------------------------------------------------------
"""

from .wider_face import WiderFaceDetection, detection_collate
from .data_augment import *
from .config import *
