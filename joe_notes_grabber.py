#!/usr/bin/python3
import os
import urllib
import re
import base64
from argparse import ArgumentParser
from urllib.request import urlopen
from urllib.parse import urljoin


def grab(url, user="", passwd="", file_exts=[]):
    auth_str = user + ":" + passwd
    encoded_auth = base64.b64encode(auth_str.encode("utf8")).decode("utf8")
    url_comps = urllib.parse.urlparse(url)
    base_url = url_comps.scheme + "://" + url_comps.netloc + url_comps.path
    html = urlopen(url, timeout=6).read().decode("utf-8")
    # grab all hyper links
    matches = re.findall(r'href=[\'"]?([^\'" >]+)', html)

    for m in matches:
        if os.path.splitext(m)[-1] in file_exts:
            m_comps = urllib.parse.urlparse(m)
            print(base_url)
            print(m_comps)
            link = m if m_comps.scheme != "" else urljoin(base_url, m_comps.path, m_comps.query)
            r = urllib.request.Request(link)
            if user != "" and passwd != "":
                r.add_header("Authorization", "Basic " + encoded_auth)
            print("Grab " + os.path.basename(m))
            print("    " + link)
            open(os.path.basename(m), "wb").write(urlopen(r, timeout=6).read())

if __name__ == "__main__":
    argparser = ArgumentParser(description="Hyperlink grabber")
    argparser.add_argument("--url", metavar="url", type=str, required=True, help="Webpage to grab from")
    argparser.add_argument("-u", "--user", type=str, metavar="username", default="", help="Username for basic auth")
    argparser.add_argument("-p", "--password", type=str, metavar="password", default="", help="Password for basic auth")
    argparser.add_argument("-e", "--extension", type=str, metavar="exts", nargs="*", default=[".pdf", ".ppt", ".doc", ".docx"], help="File extension to grab. Default: .pdf .ppt .doc .docx")

    args = argparser.parse_args()

    grab(url=args.url, user=args.user, passwd=args.password, file_exts=args.extension)
