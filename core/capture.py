#! /usr/bin/env python3
import os
import cv2			#pip3 install opencv-python
				# If there would be "numpy.core.multiarray" problem of numpy
				#Do 'pip3 uninstall numpy' few times until all numpy version will be removed.
				# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
from .subtitle import bake_caption
import requests
from .logger import *
import shutil

IMG_FORMAT = '.jpg'
FONT_FILE = 'NanumGothic.ttf'

class download_thumbnail():
    def __init__(self, v_info, arg_add_nosub=False, bake_title=False):
        self.__title = v_info['title']
        self.__thumbnail_url = v_info['thumbnail']
        self.__fontsize = v_info['font_size']
        self.__bg_opacity = v_info['bg_opacity']
        self.__imgpath = os.path.join(v_info['file_path'], 'imgs', 'frame_0' + IMG_FORMAT)
        v_info['frame_infos'][0]['img_path'] = self.__imgpath

        succeed = self.__download_thumbnail()
        if succeed and arg_add_nosub:
            self.__imgpath_nosub = os.path.join(v_info['file_path'], 'imgs', 'nosub', 'frame_0' + IMG_FORMAT)
            shutil.copyfile(self.__imgpath, self.__imgpath_nosub)
        if succeed and bake_title:
            self.__imgsize = self.__get_img_size(self.__imgpath)
            self.__bake_title()

    def __download_thumbnail(self):
        url = self.__thumbnail_url
        r = requests.get(url, stream = True)

        if r.status_code == 200:
            with open(self.__imgpath, 'wb') as f:
                f.write(r.content)
            return True
        else:
            logger.info('Error: fail to download thrumbnail img. (status code: %d, url: %s)' %(r.status_code, self.__thumbnail_url))
            return False

    def __get_img_size(self, fpath):
        if not os.path.exists(fpath):
            return None
        im = cv2.imread(fpath)
        height, width, _ = im.shape
        return (height, width)

    def __bake_title(self):
        if not self.__imgsize:
            return
        path = self.__imgpath
        text = self.__title
        font_size = int(self.__imgsize[1] / 25) # width / radio
        background_opacity = self.__bg_opacity
        bake_caption(path, text, FONT_FILE, font_size, background_opacity)

class capture_by_subs():
    def __init__(self, v_info, arg_add_nosub=False):
        self.__save_args(v_info, arg_add_nosub)
        self.__mkdir_imgs()
        self.__capture_video()

    def __save_args(self, dic, arg_add_nosub=False):
        self.img_path = os.path.join(dic['file_path'], 'imgs')
        self.vid_path = os.path.join(dic['file_path'], dic['file_name'] + '.mp4')
        self.vid_info = dic
        self.frm_info = dic['frame_infos']
        self.add_nosub = False
        if arg_add_nosub:
            self.add_nosub = True
            self.img_path_nosub = os.path.join(dic['file_path'], 'imgs', 'nosub')

    def __mkdir_imgs(self):
        os.makedirs(self.img_path)
        if self.add_nosub:
            os.makedirs(self.img_path_nosub)

    def __capture_video(self):
        cap = cv2.VideoCapture(self.vid_path)
        self.__capture(cap)
        cap.release()
        cv2.destroyAllWindows()

    def __capture(self, cap):
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        f_total= len(self.frm_info)
        f_cnt = 0
        cap_cnt = 1 # image number start with 1

        #for idx, f_dic in enumerate(self.frm_info):
        #TODO: if no frame set last frame
        while(cap_cnt < f_total):
            ret, frame = cap.read()
            duration = float(f_cnt) / float(fps)

            if duration > self.frm_info[cap_cnt]['time_info']: # the capture moment
                self.__save_frame(frame, cap_cnt)
                self.__bake_caption(cap_cnt)
                cap_cnt += 1

            f_cnt += 1

    def __save_frame(self, frame, idx):
        save_path, save_path_nosub = self.__make_frm_path(idx)
        self.frm_info[idx]['img_path'] = save_path
        self.__cv_save_image(frame, save_path)
        if self.add_nosub:
            self.__cv_save_image(frame, save_path_nosub)

    def __make_frm_path(self, idx):
        sub = os.path.join(self.img_path, self.__numbering('frame', idx) + IMG_FORMAT)
        nosub = None
        if self.add_nosub:
            nosub = os.path.join(self.img_path_nosub, self.__numbering('frame', idx) + IMG_FORMAT)
        return sub, nosub

    def __numbering(self, name, num):
        return '%s_%s' %(name, num)

    def __cv_save_image(self, frame, path):
        '''
        rate = '%d/%d  %fs' %(__cnt, (__tot_frame - 1), __duration)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        fs = round(__font_size * font_scale)
        pos = (10, fs + 10)
        color = (255, 255, 0) #(B,G,R)
        thickness = 1
        linetype = cv2.LINE_AA
        cv2.putText(__frame, rate, pos, font, font_scale, color, thickness, linetype)
        '''
        cv2.imwrite(path, frame)

    def __bake_caption(self, idx):
        path = self.frm_info[idx]['img_path']
        text = self.frm_info[idx]['script']
        font_size = self.vid_info['font_size']
        background_opacity = self.vid_info['bg_opacity']
        bake_caption(path, text, FONT_FILE, font_size, background_opacity)

def main():
    pass

if __name__ == "__main__":
	main()
