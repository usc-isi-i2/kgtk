#! /bin/sh

# The printf used below is safer than echo "$header", in case the header
# starts with a dash than echo will interpret as an option.

# The first printf sends the header to stderr, the second printf sends it
# to stdout.  The header sent to stderr should be flushed by the newline at
# the end.
{ IFS= read -r header ; { printf "%s\n" "$header" >&2 ; } ; printf "%s\n" "$header" ; sort ;  } 
