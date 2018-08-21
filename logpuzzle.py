#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1;
en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""

import os
import re
import sys
import urllib
import argparse


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    # Searches the file for any urls containing "puzzle", removing duplicates
    # and then sorting them by the word before .jpg
    with open(filename) as f:
        urls = set(re.split(r'(\S+)', f.read()))
        urls = filter(lambda url: "puzzle" in url, urls)
        server = re.split('_', filename)[1]
        for i, url in enumerate(urls):
            urls[i] = 'https://' + server + '/' + url
        return sorted(urls, key=lambda x: re.findall(r'(\w+).jpg', x))


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    if not os.path.exists(dest_dir):
        # If the directory doesn't exist, create it
        os.mkdir(dest_dir)
    count = 0
    img_string = ''
    # Copies each file from the url provided to the directory provided
    for file in img_urls:
        new_filename = '{}/img{}.jpg'.format(dest_dir, count)
        print "Retrieving {}".format(file)
        urllib.urlretrieve(file, new_filename)
        img_string += "<img src = 'img{}.jpg'>".format(count)
        count += 1
    print "Retrieved {} files".format(count)
    # Creates an html file to display the completed image
    with open('{}/index.html'.format(dest_dir), 'w') as f:
        f.write(
            '<html>\n<body>\n{}\n</body>\n</html>'.format(img_string)
            )
    pass


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
