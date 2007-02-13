#!/usr/bin/python
""" vagueurl.py -- regular expression to match informal URLs in plain text.

    This doesn't do and exact job (it doesn't parse the complete syntax
    of URLs) but it should find URLs that at least start right.
    It looks for the start of an address then gobbles up as many legal URL
    characters as it can find.

    Original version - Glyn Webster <glyn@ninz.org.nz> 1999-04-27
    Fishbot plugin - Nell Hardcastle <chizu@spicious.com> 2006-03-14
"""

import re, fishapi

pattern = r"""
( ( \w | - | % )+ @	 #	email address prefix (e.g. "glyn@")
| \w+ ://			 #	or protocol prefix (e.g. "http://")
| news:				 #	or "news:" prefix (special case: no "//")
| mailto:			 #
| www \.			 #	lazy typists leave off common prefixes
| ftp \.
)					 #	then
[^\\{}|[\]^<>"'\s]*	 #	the rest are any characters allowed in a URL.
[^\\{}|[\]^<>"'\s.,;?:!]
#  it mustn't end in a punctuation mark or this would
#  match this wrong: "Www.w3.org, ftp.simtel.net."
"""
#"
regex = re.compile(pattern, re.IGNORECASE | re.VERBOSE)

def regular(url):
	""" Add an appropiate prefix to an informal URL.
	"""
	if re.match(r"\w+:", url):			 #Has prefix already, leave it alone.
		return url
	else:
		if re.match(r"(\w|-|%)+@", url):   #Starts like an email address.
			return "mailto:" + url
		elif url[:3] == 'ftp':			   #Starts like an FTP address.
			return "ftp://" + url
		else:							   #Assume it's a WWW address.
			return "http://" + url

def getText(nodelist):
	rc = ""
	for node in nodelist:
		if node.nodeType == node.TEXT_NODE:
			rc = rc + node.data
	return rc

def urlmatcher(self, event):
	"""The magic of URL parsing."""
	import re,urllib,string
	import xml.dom.minidom, xml.parsers.expat

	m = regex.search(event.arguments)
	respond = self.respond_to(event.source, event.target)
	if m:
		try:
			resource = urllib.urlopen(regular(m.group()))
		except:
			return
		if not (resource.info().getheader('Content-Type').split(';')[0] in ["application/xhtml+xml", "text/html"]):
			if resource.info().getheader('Content-Type').split(';')[0] in ["application/x-bittorrent"]:
				torrent = resource.readlines()
				result = re.search("name[0-9]*?:(.*?)12:",torrent[0])
				if hasattr(result, "group"):
					event.server.say(respond, "Torrent Name: " + result.group(1))
			else:
				event.server.say(respond, "Content Type: " + (resource.info().getheader('Content-Type') or "b0rked webserver"))
			resource.close()
			return
		try:
			xhtml = resource.readlines()
			dom = xml.dom.minidom.parseString(string.join(xhtml))
			event.server.say(respond, "XHTML, Title: " + getText(dom.getElementsByTagName("title")[0].childNodes))
		except xml.parsers.expat.ExpatError:
			for each in xhtml:
				if re.compile("\<title.*\>(.*)\<\/title\>",re.I).search(each):
					match = re.search("\<title.*\>(.*)\<\/title\>",each,re.I)
					event.server.say(respond, "Malformed XML, Title: " + match.group(1))

		if len(regular(m.group())) > 40:
			# Creates a tinyurl out of a long url
			url = "http://tinyurl.com/create.php?url=" + regular(m.group())
			tiny = fishapi.http_grep(url, """<blockquote>.*?href="(http://tinyurl.com/[^\"]+)""")
			event.server.say(respond, "Your tiny URL is: " + tiny[0])
			
		resource.close()
		return

expression = (regex, urlmatcher)
