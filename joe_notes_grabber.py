from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import re
import os
import base64

user = "comp4017"
passwd = "24001157"
html_url = "http://cslinux0.comp.hkbu.edu.hk/~comp4017/2015-16/?page_id=8"
grab_url = "http://cslinux0.comp.hkbu.edu.hk/~comp4017/2015-16/notes/"


def readURL(req):
	return urlopen(req, timeout = 12).read()

def main():
	auth_str = user + ":" + passwd
	encoded_auth = base64.b64encode(auth_str.encode("utf8")).decode("utf8")
	html = readURL(html_url)
	limit = SoupStrainer("td")
	soup = BeautifulSoup(html, "html.parser", parse_only=limit)
	pdfs = re.findall(r'href=[\'"]?([^\'" >]+)', soup.prettify())
	for pdf in pdfs:
		print("Grab " + os.path.basename(pdf))
		r = urllib.request.Request(grab_url + os.path.basename(pdf))
		if user != "" and passwd != "":
			r.add_header("Authorization", "Basic " + encoded_auth)
		open(os.path.basename(pdf), "wb").write(readURL(r))

if __name__ == "__main__":
	main()