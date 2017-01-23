#!/usr/bin/python

# Transcode files to DLNA-compatible x264/AAC and retain original file's timestamp

import os, os.path, time, hashlib, sys, shutil, re, time, subprocess

src_path = sys.argv[1]
tgt_path = sys.argv[2]

extensions = ['.avi']
path_format = "%Y/%Y-%m/%Y-%m-%d"
filename_prefix_format = "%Y-%m-%d_%H%M%S"




def move_files( file_list, dry_run=True, delete_identical_files=True):
  i = 0
  error_count = 0
  identical_file_count = 0
  for f in file_list:
    #    if (i > 5):
#      print "did 5"
#      return

    

    new_path = get_new_filename(os.path.normpath(f))
    print("Transcode %s ---TO---> %s" % (f, new_path))
    if (not dry_run):
      dir_name = os.path.dirname(new_path)
      if (not os.path.exists(dir_name)):
        os.makedirs(dir_name)
      if (os.path.exists(new_path)):
        print "WARN: File already exists: %s" % new_path
        error_count = error_count + 1
#        if (files_are_identical(f, new_path)):
#          print "INFO: Source and target files are identical"
#          identical_file_count = identical_file_count + 1
#          if (delete_identical_files):
#            print "INFO: Deleting file %s" % f
#            os.remove(f)
      else:
        try:
           original_file_modtime = os.path.getmtime(f)
           ffmpeg_command = ['/usr/bin/ffmpeg', '-i', f, '-codec:v','libx264','-crf','22','-pix_fmt','yuv420p','-codec:a','libfdk_aac','-b:a','256k',new_path]
           output = subprocess.check_output(ffmpeg_command, stderr=subprocess.STDOUT)           
           os.utime(new_path, (original_file_modtime, original_file_modtime ))
           
#          shutil.move(f, new_path)
	except NameError as ne:
		print "NameError: %s" % ne
        except Exception as e:
          print "Unable to transcode %s: Code %s, Output %s" % (f, e.returncode, e.output)
      i = i+1
  print "Errors: %d.  Identical files: %d." % (error_count, identical_file_count)

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

  return file_list



def get_new_filename( src_filename ):

  new_path = None

#    print "%s NOT A JPEG" % src_filename
  file_ctime = time.localtime(os.path.getmtime(src_filename))
#  new_prefix = time.strftime(filename_prefix_format, file_ctime)
  new_prefix = os.path.splitext(os.path.split(src_filename)[1])[0]
  new_filename = ".".join([new_prefix, 'm4v'])

  new_path = "/".join([
    tgt_path, 
    time.strftime(path_format, file_ctime), 
    new_filename
    ])

  return new_path


#f = get_file_list(src_path)
f = move_files(get_file_list(os.path.abspath(src_path)), dry_run=False)
