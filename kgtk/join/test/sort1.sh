#! /bin/sh
{
    # grab the header and print it untouched
    IFS= read -r header
    echo "$header"
    # now process the rest of the input
    sort
} 
