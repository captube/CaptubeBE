#! /usr/bin/env python3
import os
import cv2			#pip3 install opencv-python
				# If there would be "numpy.core.multiarray" problem of numpy
				#Do 'pip3 uninstall numpy' few times until all numpy version will be removed.
				# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
from .subtitle import bake_caption

IMG_FORMAT = '.jpg'
FONT_FILE = 'NanumGothic.ttf'

class capture_by_subs():
    def __init__(self, v_info):
        self.__save_args(v_info)
        self.__mkdir_imgs()
        self.__capture_video()

    def __save_args(self, dic):
        self.img_path = os.path.join(dic['file_path'], 'imgs')
        self.vid_path = os.path.join(dic['file_path'], dic['file_name'] + '.mp4')
        self.vid_info = dic
        self.frm_info = dic['frame_infos']

    def __mkdir_imgs(self):
        os.makedirs(self.img_path)

    def __capture_video(self):
        cap = cv2.VideoCapture(self.vid_path)
        self.__capture(cap)
        cap.release()
        cv2.destroyAllWindows()

    def __capture(self, cap):
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        f_total= len(self.frm_info)
        f_cnt = cap_cnt = 0

        #for idx, f_dic in enumerate(self.frm_info):
        while(cap_cnt < f_total):
            ret, frame = cap.read()
            duration = float(f_cnt) / float(fps)

            if duration > self.frm_info[cap_cnt]['time_info']: # the capture moment
                self.__save_frame(frame, cap_cnt)
                self.__bake_caption(cap_cnt)
                cap_cnt += 1

            f_cnt += 1

    def __save_frame(self, frame, idx):
        save_path = self.__make_frm_path(idx)
        self.frm_info[idx]['img_path'] = save_path
        self.__cv_save_image(frame, save_path)

    def __make_frm_path(self, idx):
        ret = os.path.join(self.img_path, self.__numbering('frame', idx) + IMG_FORMAT)
        return ret

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