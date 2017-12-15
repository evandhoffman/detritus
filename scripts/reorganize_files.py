#!/usr/bin/python

import os, os.path, time, hashlib, sys, shutil, re, time
import exifread

#src_path = "/Volumes/hfs/backups/camera/Reorganized Movies/Newer/"
src_path = sys.argv[1]
#tgt_path = "/Volumes/hfs/backups/camera/Reorganized Media"
tgt_path = sys.argv[2]
#tgt_path = "/Users/evan/temp"

photo_extensions = ['jpg', 'jpeg', '.bmp']
video_extensions = ['.mov', '.mp4', '.avi', '.m4v' ]

extensions = photo_extensions + video_extensions

photo_path_format = "Photos/%Y/%Y-%m"
video_path_format = "Videos/%Y/%Y-%m"

filename_prefix_format = "%Y-%m-%d_%H%M%S"
#filename_prefix_format = "%Y-%m-%d_%H%M%S.lisa"

def is_photo ( file_name ):
  for ext in photo_extensions:
    if file_name.lower().endswith(ext):
      return True
  return False

def is_video ( file_name ):
  for ext in video_extensions:
    if file_name.lower().endswith(ext):
      return True
  return False

def is_jpg( file_name ):
  for ext in [ 'jpg', 'jpeg' ]:
    if file_name.lower().endswith(ext):
      return True
  return False

def has_exiftags( file_name):
  tags = get_exiftags( file_name )
  if (tags == None):
    return False

  has_tags = True
  for t in ['EXIF DateTimeOriginal', 'Image Model']:
    if t not in tags:
      has_tags = False

  return has_tags

def get_exiftags( file_name ):
  if not is_jpg( file_name ):
    return None

  f = open(file_name, 'rb')
  print "getting tags for %s" % file_name
  tags = exifread.process_file(f, details=False)
  return tags

def get_new_filename_jpg( src_filename, with_digest = True, digest = None):
  tags = get_exiftags(src_filename)
  jpg_date = time.strptime(str(tags['EXIF DateTimeOriginal']), '%Y:%m:%d %H:%M:%S')
  jpg_cameramodel = re.sub(r'[^\w]+', '_', str(tags['Image Model']).lower())

  new_prefix = time.strftime(filename_prefix_format, jpg_date)
  new_filename = ".".join([new_prefix, jpg_cameramodel, digest[:8], os.path.splitext(src_filename)[1][1:].lower()])

  new_path = "/".join([
    tgt_path, 
    time.strftime(photo_path_format, jpg_date), 
    new_filename
    ])

#  print "New path: %s" % new_path
  return new_path



def move_files( file_list, dry_run=True, delete_identical_files=True):
  i = 0
  error_count = 0
  identical_file_count = 0
  for f in file_list:
    #    if (i > 5):
#      print "did 5"
#      return
    new_path = get_new_filename(os.path.normpath(f))
    print("%s => %s" % (f, new_path))
    if (not dry_run):
      dir_name = os.path.dirname(new_path)
      if (not os.path.exists(dir_name)):
        os.makedirs(dir_name)
      if (os.path.exists(new_path)):
        print "WARN: File already exists: %s" % new_path
        error_count = error_count + 1
        if (files_are_identical(f, new_path)):
          print "INFO: Source and target files are identical"
          identical_file_count = identical_file_count + 1
          if (delete_identical_files):
            print "INFO: Deleting file %s" % f
            os.remove(f)
      else:
        try:
          shutil.move(f, new_path)
        except Exception as e:
          print "Unable to move %s: %s" % (f, e.strerror)
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



def get_new_filename( src_filename , with_digest=True):
  digest=''
  if (with_digest):
    try:
      digest = hashlib.md5(open(src_filename, 'rb').read()).hexdigest()
    except IOError as e:
      print "Unable to calculate MD5 for %s: %s" % (src_filename, e.strerror)

  new_path = None

  if has_exiftags(src_filename):
    new_path = get_new_filename_jpg( src_filename, with_digest, digest )
  else:
#    print "%s NOT A JPEG" % src_filename
    file_ctime = time.localtime(os.path.getmtime(src_filename))
    new_prefix = time.strftime(filename_prefix_format, file_ctime)
    new_filename = ".".join([new_prefix, digest[:8], os.path.splitext(src_filename)[1][1:].lower()])

    if (is_video(new_filename)):
      pathformat = video_path_format
    else:
      pathformat = photo_path_format

    new_path = "/".join([
      tgt_path, 
      time.strftime(pathformat, file_ctime), 
      new_filename
      ])

  return new_path


#f = get_file_list(src_path)
f = move_files(get_file_list(os.path.abspath(src_path)), dry_run=False)
