#!/usr/bin/python

import os, os.path, time, hashlib, sys, shutil

#src_path = "/Volumes/hfs/backups/camera/Reorganized Movies/Newer/"
src_path = sys.argv[1]
tgt_path = "/Volumes/hfs/backups/camera/py2/"
extensions = ['.mov', '.mp4', '.avi']
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
    print("Moving %s to %s" % (f, new_path))
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
    else:
      if (os.path.isdir(full_path) and recursive):
        file_list = file_list + get_file_list(full_path, True)

  return file_list



def get_new_filename( src_filename , with_digest=True):
  file_ctime = time.localtime(os.path.getmtime(src_filename))
  digest=''
  if (with_digest):
    digest = hashlib.md5(open(src_filename, 'rb').read()).hexdigest()

  new_prefix = time.strftime(filename_prefix_format, file_ctime)
  new_path = "/".join(
      [tgt_path, 
        time.strftime(path_format, file_ctime), 
        ".".join(
          [new_prefix, digest[:8], os.path.splitext(src_filename)[1][1:].lower()])])
#            os.path.basename(src_filename)])])
  return new_path


#f = get_file_list(src_path)
f = move_files(get_file_list(os.path.abspath(src_path)), dry_run=False)
