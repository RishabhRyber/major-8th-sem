from pytube import YouTube
import shutil
import sys

#SAVE_PATH = "/media/kaiser/Elements/Major/YT/"
path = "/media/kaiser/Elements/Major/YT/"
link = 'https://www.youtube.com/watch?v=0zD6rWU06fo'

file_size = 0;
prev = 0

total = 0
cur = 0
successful = 0

def display_progress_bar(bytes_received = None, filesize = None, ch = "█", scale = 0.55):
    columns = shutil.get_terminal_size().columns
    max_width = int(columns * scale)

    filled = int(round(max_width * bytes_received / float(filesize)))
    remaining = max_width - filled
    progress_bar = ch * filled + " " * remaining
    percent = round(100.0 * bytes_received / float(filesize), 1)
    text = f" |{progress_bar}| {percent}%\r"
    if bytes_received == filesize:
        text = f" |{progress_bar}| {percent}%  " + u'\u2713' + f"  \n"
    sys.stdout.write(text)
    sys.stdout.flush()

def on_my_progress(stream = None, chunk = None, bytes_remaining = None):  # pylint: disable=W0613
    filesize = stream.filesize
    bytes_received = filesize - bytes_remaining
    display_progress_bar(bytes_received, filesize)

def download(url):
   global cur
   cur = cur + 1 
   try:
      yt = YouTube(url, on_progress_callback = on_my_progress)
      #streams = yt.streams.filter(file_extension = 'mp4', type = 'video')
      #stream = streams[int(len(streams) / 2)]
      stream = yt.streams.filter(file_extension = 'mp4', type = 'video').first()
      size = ' B'
      mem = stream.filesize
      if mem > 1023:
         mem = mem / 1024
         size = ' kB'
      if mem > 1023:
         mem = mem / 1024
         size = ' MB'
      if mem > 1023:
         mem = mem / 1024
         size = ' GB'
      if mem > 1023:
         mem = mem / 1024
         size = ' TB'
     
      print('↳ ' + stream.title[:min(len(str(stream.title)) - 1, 30)] + '...\t(' + str(cur) + '/' + str(total) + ') ' + str(f'{mem:9.2f}') + size)
      stream.download(output_path = path + stream.title, filename = stream.default_filename + str(stream.filesize))
#      for stream in streams:
#         global file_size
#         global prev
#         prev = 0
#         file_size = stream.filesize
#         print('↳ ' + stream.title[:min(len(stream.title) - 1, 30)] + '...')
#         stream.download(output_path = path + stream.title, filename = stream.default_filename + str(stream.filesize))
   except Exception as e:
      if str(e) ==  '<urlopen error [Errno -2] Name or service not known>':
         print('Check Internet connection')
         exit(0)
      print('Video Error: ' + str(e))

def download_from_file(myfile = None, ch = '-', scale = 0.55):
   myfile = 'links.txt'
   try:
      f = open(myfile, 'r')
      links = f.read().split('\n')
      global total
      total = len(links) - 1
      for link in links[:-1]:
         download(link)
   except Exception as e:
      print('File Error: ' + str(e) + ' ' + myfile)
   finally:
      f.close()

download_from_file("links.txt")
