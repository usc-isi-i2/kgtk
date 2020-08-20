#! /bin/sh

# The printf used below is safer than echo "$header", in case the header
# starts with a dash than echo will interpret as an option.
{ IFS= read -r header ; printf "%s\n" "$header" ; sort ;  } 
