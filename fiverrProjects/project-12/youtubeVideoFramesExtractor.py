#--IMPORTING THE REQUIRED LIBRARIES--#
from pytube import YouTube

# misc
import os
import shutil
import math
import datetime
import csv

# plots
# import matplotlib.pyplot as plt
#%matplotlib inline

# image operation
import cv2


#--FrameExtractor CLASS - TO EXTRACT THE IMAGE FRAMES--#
class FrameExtractor():
    '''
    Class used for extracting frames from a video file.
    '''
    def __init__(self, video_path):
        self.video_path = video_path
        self.vid_cap = cv2.VideoCapture(video_path)
        self.n_frames = int(self.vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.vid_cap.get(cv2.CAP_PROP_FPS))
        
    def get_video_duration(self):
        '''Method for printing the video's duration'''
        duration = self.n_frames/self.fps
        print(f'Duration: {datetime.timedelta(seconds=duration)}')
        
    def get_n_images(self, every_x_frame):
        '''
        Method for calculating the expected number of images to save given 
        we save every x-th frame
        
        Parameters
        ----------
        
        every_x_frame : int
            Indicates we want to look at every x-th frame
        '''
        n_images = math.floor(self.n_frames / every_x_frame) + 1
        print(f'Extracting every {every_x_frame} (nd/rd/th) frame would result in {n_images} images.')
        
    def extract_frames(self, every_x_frame, img_name, dest_path=None, img_ext = '.jpg'):
        '''
        Method used for extracting the frames from images
        
        Parameters
        ----------
        
        every_x_frame : int
            Indicates we want to extract every x-th frame
        img_name : str
            The image name, numbers will be appended (after an underscore) at the end
        dest_path : str
            The path where to store the images. Default (None) saves the images to current directory.
        img_ext : str
            Indicates the desired extension of the image. Default is JPG
        '''
        if not self.vid_cap.isOpened():
            self.vid_cap = cv2.VideoCapture(self.video_path)
        
        if dest_path is None:
            dest_path = os.getcwd()
        else:
            if not os.path.isdir(dest_path):
                os.mkdir(dest_path)
                print(f'Created the following directory: {dest_path}')
        
        frame_cnt = 0
        img_cnt = 0

        while self.vid_cap.isOpened():
            
            success,image = self.vid_cap.read() 
            
            if not success:
                break
            
            if frame_cnt % every_x_frame == 0:
                img_path = os.path.join(dest_path, ''.join([img_name, '_', str(img_cnt), img_ext]))
                cv2.imwrite(img_path, image)  
                img_cnt += 1
                
            frame_cnt += 1
        
        self.vid_cap.release()
        cv2.destroyAllWindows()


#--DOWNLOADING THE VIDEO FILE--#

# Reading the input csv file
url_list = []
frame_list = []
op_dir_start_cnt = int(input("Enter the Output Directory starting count: "))

with open('inputUrls.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  for index,urls in enumerate(csv_reader):
    # if index == 1:
    #   op_dir_start_cnt = int(urls[2])
    if index != 0:
      url_list.append(urls[0])
      frame_list.append(urls[1])

for url,frame in zip(url_list, frame_list):
  # create the instance of the YouTube class
  video = YouTube(url)

  # print a summary of the selected video
  print('Summary:')
  print(f'Title: {video.title}')
  print(f'Duration: {video.length / 60:.2f} minutes')
  print(f'Rating: {video.rating:.2f}')
  print(f'# of views: {video.views}')
  print("\n\n")

  # display all streams
  # video.streams.all()

  # display only the streams with the selected file format 
  # video.streams.filter(file_extension = "mp4").all()

  # download the selected video
  videoPath = video.streams.get_by_itag(18).download("videoDownloads")

  # instantiate the class using the downloaded video
  fe = FrameExtractor(videoPath)

  # print the number of frames in the video
  # fe.n_frames

  # print the video's duration
  # fe.get_video_duration()

  # calculate the potential number of frames 
  fe.get_n_images(every_x_frame=int(frame))

  # extract every 1000th frame
  fe.extract_frames(every_x_frame=int(frame), 
                    img_name='img', 
                    dest_path=f'out/out{op_dir_start_cnt}')
  
  op_dir_start_cnt += 1