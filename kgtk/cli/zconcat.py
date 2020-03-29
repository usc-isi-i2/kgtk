#!/usr/bin/env python

############################# BEGIN LICENSE BLOCK ############################
#                                                                            #
# Copyright (C) 2020                                                         #
# UNIVERSITY OF SOUTHERN CALIFORNIA, INFORMATION SCIENCES INSTITUTE          #
# 4676 Admiralty Way, Marina Del Rey, California 90292, U.S.A.               #
#                                                                            #
# Permission is hereby granted, free of charge, to any person obtaining      #
# a copy of this software and associated documentation files (the            #
# "Software"), to deal in the Software without restriction, including        #
# without limitation the rights to use, copy, modify, merge, publish,        #
# distribute, sublicense, and/or sell copies of the Software, and to         #
# permit persons to whom the Software is furnished to do so, subject to      #
# the following conditions:                                                  #
#                                                                            #
# The above copyright notice and this permission notice shall be             #
# included in all copies or substantial portions of the Software.            #
#                                                                            #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,            #
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF         #
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND                      #
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE     #
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION     #
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION      #
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.            #
#                                                                            #
############################# END LICENSE BLOCK ##############################

from   __future__ import print_function
import sys
import os
import os.path
import argparse
import sh
import tempfile


def parser():
    return {
        'help': 'Concatenate any mixture of plain or gzip/bzip2/xz-compressed files'
    }


scriptName = os.path.basename((len(sys.argv) > 0 and sys.argv[0]) or '')
runsAsScript = scriptName.find('.py') >= 0

def add_arguments(parser):
    parser.add_argument('-o', '--out', default=None, dest='output', help='output file to write to, otherwise output goes to stdout')
    parser.add_argument('--gz', '--gzip', action='store_true', dest='gz', help='compress result with gzip')
    parser.add_argument('--bz2', '--bzip2', action='store_true', dest='bz2', help='compress result with bzip2')
    parser.add_argument('--xz', action='store_true', dest='xz', help='compress result with xz')
    parser.add_argument("inputs", nargs="?", action="store", help='files to process')

def determineFileType(file):
    fileType = sh.file('--brief', file).stdout.split()[0].lower()
    return (file, fileType)

def run(output, gz, bz2, xz, inputs):

    # import modules locally
    import socket
    if isinstance(output, str):
        output = open(output, "wb")
    compress = None
    if gz:
        compress = sh.gzip
    elif bz2:
        compress = sh.bzip2
    elif xz:
        compress = sh.xz

    print(inputs)
    if inputs:
        for inp in inputs:
            catcmd = sh.cat
            file, fileType = determineFileType(inp)
            if fileType == 'gzip':
                catcmd = sh.zcat
            elif fileType == 'bzip2':
                catcmd = sh.bzcat
            elif fileType == 'xz':
                catcmd = sh.xzcat
            try:
                if compress is not None:
                    compress(catcmd(file, _piped=True, _out=output), '-c', _out=output, _tty_out=False)
                else:
                    catcmd(file, _out=output)
            except sh.SignalException_SIGPIPE:
                break
    else:
        print('here')
        try:
            if compress is not None:
                print('compressing')
                compress('-c', _in=sys.stdin, _out=output, _tty_out=False)
                print('compressing done')
            else:
                sh.cat(_in=sys.stdin, _piped=True, _out=output)
        except sh.SignalException_SIGPIPE:
            pass

    # cleanup in case we piped and terminated prematurely:
    try:
        output.flush()
        sys.stdout.flush()
    except:
        pass
