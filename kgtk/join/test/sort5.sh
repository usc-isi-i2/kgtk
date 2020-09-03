#! /bin/sh

# The printf used below is safer than echo "$header", in case the header
# starts with a dash than echo will interpret as an option.

# The first printf sends the header to stderr, the second printf sends it
# to stdout.  The header sent to stderr should be flushed by the newline at
# the end.
#
# The first printf and the second read use file descriptors which are passed
# through envars FS1 and FS2.  In the Python, use:
#
# os.pipe() to create two file descriptor pairs
# 
# sh(..., _env={}) to set the envars
#
# sh(..., _pass_fds=set()) to pass the pip FDs into the subprocess
#
# Of course, it might be easier to avoid messing with envars by just
# editing the script before executing it.
#
# https://amoffat.github.io/sh/sections/special_arguments.html
#
{ IFS= read -r header ; { printf "%s\n" "$header" >&${FS1} ; } ; IFS= read -r -u${FS2} options; printf "%s\n" "$header" ; sort $options ;  } 
