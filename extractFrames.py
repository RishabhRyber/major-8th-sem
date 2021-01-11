import os
import cv2
import shutil
import sys

def getFrame(video_path = None, frame_path = None, myFPS = 1):
   video_obj = cv2.VideoCapture(video_path)
   count = 0
   success, image = video_obj.read()
   (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
   if int(major_ver)  < 3 :
      fps = round(video_obj.get(cv2.cv.CV_CAP_PROP_FPS))
      total_frames = video_obj.get(cv2.cv.CAP_PROP_FRAME_COUNT)
   else:
      fps = round(video_obj.get(cv2.CAP_PROP_FPS))
      total_frames = video_obj.get(cv2.CAP_PROP_FRAME_COUNT)
   length = int(total_frames / fps)
   fps = int(fps * myFPS)
   print('length: ' + str(int(total_frames / fps)), end = ' ')
   while success:
      if count % fps == 0:
         cv2.imwrite(frame_path + '%d.jpg' %count, image)
      count = count + 1
      success, image = video_obj.read()
   sys.stdout.write(u'\u2713' + '\n')
   sys.stdout.flush()
   video_obj.release()

def getFrames(videos_path = None, frames_path = None):
   folders = os.listdir(videos_path)
   for folder in folders:
      videos = os.listdir(videos_path + '/' + folder)
      vp = videos_path + '/' + folder + '/'
      fp = frames_path + '/' + folder + '/'
      try:
         os.mkdir(os.path.join(os.getcwd() + '/frames/', folder))
      except Exception as e:
         print('Directory Frame error: ' + str(e))
      finally:
         for video in videos:
            print(video[:min(30, len(video))] + '...', end = ' ')
            getFrame(vp + video, fp)

videos_path = os.getcwd() + '/videos'
frames_path = os.getcwd() + '/frames'
try:
   os.mkdir(os.path.join(os.getcwd() + '/', 'frames'))
except Exception as e:
   print('Directory error: ' + str(e))
getFrames(videos_path, frames_path)




