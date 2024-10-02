"""
------------------------------------------------------------------------------------------------------------------------
Zdrojovy kod v adresari /backend/face_reenactment/ je prevzaty z: https://github.com/sky24h/Face_Animation_Real_Time
Povodny autor kodu: sky24h
------------------------------------------------------------------------------------------------------------------------
Upraveny bol iba subor: /backend/face_reenactment/camera_local.py
------------------------------------------------------------------------------------------------------------------------
"""

'''
@paper: GAN Prior Embedded Network for Blind Face Restoration in the Wild (CVPR2021)
@author: yangxy (yangtao9009@gmail.com)
'''
import os.path as osp
import sys

def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)

this_dir = osp.dirname(__file__)

path = osp.join(this_dir, 'retinaface')
add_path(path)

path = osp.join(this_dir, 'face_model')
add_path(path)

path = osp.join(this_dir, 'sr_model')
add_path(path)