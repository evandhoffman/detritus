#!/usr/bin/python

import os, os.path, time, glob

src_path = "/Users/evan/testdir"
tgt_path = "/Users/evan/dstdir"
extensions = ['jpg', 'txt']
path_format = "%Y/%Y-%m/%Y-%m-%d"
filename_prefix_format = "%Y-%m-%d"

def move_files( file_list):
  for f in file_list:
    new_path = get_new_filename(os.path.normpath(f))
    print("Moving %s to %s" % (f, new_path))

def get_file_list( src_path, recursive=True ):
  dir_list = os.listdir( src_path )
  file_list = []
  for f in dir_list:
    full_path = "/".join([src_path, f])
    if (os.path.isfile(full_path)):
      for e in extensions:
        if (full_path.endswith(e)):
          file_list.append(full_path)
    else:
      if (os.path.isdir(full_path) and recursive):
        file_list = file_list + get_file_list(full_path, True)

  return file_list



def get_new_filename( src_filename ):
  file_ctime = time.localtime(os.path.getctime(src_filename))
  new_prefix = time.strftime(filename_prefix_format, file_ctime)
  new_path = "/".join(
      [tgt_path, 
        time.strftime(path_format, file_ctime), 
        ".".join(
          [new_prefix, 
            os.path.basename(src_filename)])])
  return new_path


#f = get_file_list(src_path)
f = move_files(get_file_list(os.path.abspath(src_path)))

print f
