#! /usr/bin/env python3
# download youtube video using Pytube3
# and save the informations

import os, sys
from pytube import YouTube
from .make_cap_data import *
from .logger import *

class youtube():
    def __init__(self, url):
        self.vinfo = cap_data()
        self.info = YouTube(url)
        self.save_video_info(self.vinfo, url)
        self.cap = self.get_captions()

    def get_streams(self):
        if self.info:
            return self.info.streams
        return None

    def get_streams_itag(self, itag):
        if self.info:
            return self.get_streams().get_by_itag(itag)
        return None

    def save_video_info(self, vi, url):
        vi['url'] = url
        vi['title'] = self.info.title
        vi['video_id'] = self.info.video_id
        vi['thumbnail'] = self.info.thumbnail_url

    def download_video(self, fpath, fname=None, itag='18'):
        st = self.get_streams_itag(itag) #FIXME: best way to select itag
        if fname == None:
           fname = self.vinfo['video_id']
        st.download(output_path=fpath, filename=fname)
        result = os.path.join(fpath, fname + '.mp4')
        logger.info('The video is downloaded in "%s" ' %result)
        return result

    def get_captions(self):
        return self.info.captions

    def __save_caption_code(self, code):
        self.vinfo['lang'] = code

    def is_lang_available(self, lang):
        try:
            if self.cap[lang].code == lang:
                return True
            return False
        except(KeyError):
            return False

    def get_available_langs(self, cap):
        ret = []
        for key, val in self.cap.lang_code_index.items():
            ret.append(val.name)
        return ret

    def __convert_lang_name_to_code(self, langname):
        for key, val in self.cap.lang_code_index.items():
            if langname == val.name:
                return val.code
        return langname

    def __save_caption_file(self, cap, fpath, fname):
        if fname == None:
            fname = self.vinfo['video_id']
        tgt = os.path.join(fpath, fname + '.srt')
        with open(tgt, 'w', encoding='utf8') as fp:
            fp.write(cap.generate_srt_captions())
        return tgt

    def download_caption(self, fpath, fname=None, lang='English'):
        langcode=self.__convert_lang_name_to_code(lang)
        if not self.is_lang_available(langcode):
            alternative_langs = self.get_available_langs(self.cap)
            logger.critical('The caption language "%s" is not exist, try to choose another language in: \n%s' %(langcode, alternative_langs))
            raise SystemExit

        # TODO here: get langcode from en to real code(en_GB or somethings)

        self.__save_caption_code(langcode)
        caption = self.cap[langcode]
        result = self.__save_caption_file(caption, fpath, fname)
        logger.info('The caption is downloaded in %s' %result)
        return result


def example():
    pass

if __name__ == '__main__':
    example()
