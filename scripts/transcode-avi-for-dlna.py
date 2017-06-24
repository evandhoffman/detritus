#!/usr/bin/python

# Transcode files to DLNA-compatible x264/AAC and retain original file's timestamp

import os, os.path, time, hashlib, sys, shutil, re, time, subprocess, datetime

src_path = sys.argv[1]
tgt_path = sys.argv[2]

extensions = ['.avi','.mpg']
path_format = "Transcodes/%Y/%Y-%m/"
filename_prefix_format = "%Y-%m-%d_%H%M%S"




def transcode_files( file_list, dry_run=True, delete_identical_files=True):
  i = 0
  error_count = 0
  success_count = 0
  identical_file_count = 0

  total_start = datetime.datetime.now()

  for f in file_list:

    new_path = get_new_filename(os.path.normpath(f))
    if (not dry_run):
      dir_name = os.path.dirname(new_path)
      if (not os.path.exists(dir_name)):
        os.makedirs(dir_name)
      if (os.path.exists(new_path)):
        print "WARN: File already exists: %s" % new_path
        error_count = error_count + 1
      else:
        try:
           original_file_modtime = os.path.getmtime(f)
           ffmpeg_command = ['/usr/bin/ffmpeg', '-i', f, '-codec:v','libx264','-crf','18','-pix_fmt','yuv420p','-codec:a','libfdk_aac','-b:a','256k',new_path]
           s = datetime.datetime.now()
           output = subprocess.check_output(ffmpeg_command, stderr=subprocess.STDOUT)           
           os.utime(new_path, (original_file_modtime, original_file_modtime ))
           e = datetime.datetime.now()

           old_size = os.path.getsize(f)
           new_size = os.path.getsize(new_path)
           ratio = (new_size * 1.0 / old_size) * 100

           print("Transcode %s ---TO---> %s took %s. Old: %0.1f MB New: %0.1f MB Compression: %0.1f %%" % (f, new_path, str(e - s), old_size / 1e6, new_size / 1e6, ratio  ))
           success_count = success_count + 1
           
#          shutil.move(f, new_path)
	except NameError as ne:
		print "NameError: %s" % ne
        except Exception as e:
          print "Unable to transcode %s: %s" % (f, str(e))
      i = i+1

  total_end = datetime.datetime.now()
  total_elapsed = total_end - total_start
  print "Files transcoded: %d. Errors: %d.  Identical files: %d. Total time elapsed: %s" % (success_count, error_count, identical_file_count, str(total_elapsed))

def files_are_identical (a, b):
  size_a = os.path.getsize(a)
  size_b = os.path.getsize(b)
  if (size_a != size_b):
    return False

  digest_a = hashlib.md5(open(a, 'rb').read()).hexdigest()
  digest_b = hashlib.md5(open(b, 'rb').read()).hexdigest()

  if (digest_a != digest_b):
    return False

  return True


def get_file_list( src_path, recursive=True ):
  dir_list = os.listdir( src_path )
  file_list = []
  for f in dir_list:
    full_path = "/".join([src_path, f])
    if (os.path.isfile(full_path)):
      for e in extensions:
        if (full_path.lower().endswith(e)):
          file_list.append(full_path)
#          print "Considering %s" % full_path
    else:
      if (os.path.isdir(full_path) and recursive):
        file_list = file_list + get_file_list(full_path, True)

  print "Found %d files to transcode" % len(file_list)
  return file_list



def get_new_filename( src_filename ):

  new_path = None

#    print "%s NOT A JPEG" % src_filename
  file_ctime = time.localtime(os.path.getmtime(src_filename))
#  new_prefix = time.strftime(filename_prefix_format, file_ctime)
  new_prefix = os.path.splitext(os.path.split(src_filename)[1])[0]
  new_filename = ".".join([new_prefix, 'converted.mp4'])

  new_path = "/".join([
    tgt_path, 
    time.strftime(path_format, file_ctime), 
    new_filename
    ])

  return new_path


#f = get_file_list(src_path)
f = transcode_files(sorted(get_file_list(os.path.abspath(src_path))), dry_run=False)
