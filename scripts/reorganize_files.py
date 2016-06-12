#!/usr/bin/python

import os, os.path, time, glob

src_path = "/Users/evan/testdir"
tgt_path = "/Users/evan/dstdir"
extensions = ['jpg', 'txt']
path_format = "%Y/%Y-%m/%Y-%m-%d"
filename_prefix_format = "%Y-%m-%d"


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
      if (recursive):
        file_list = file_list + get_file_list(full_path, True)

  return file_list



def get_new_filename( src_filename ):
  file_ctime = time.ctime(os.path.getctime(src_filename))
  new_prefix = time.strftime(filename_prefix_format, file_ctime)
  new_path = "/".join(tgt_path, time.strftime(path_format, file_ctime, ".".join(new_prefix, src_filename)))
  return new_path


f = get_file_list(src_path)

print f
