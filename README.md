# Zebra label printer webapp

I made this little python webapp to help people in lab to make labels.  The program generates ZPL for a Zebra GX430t printer and sends it to a CUPS printer. It is nothing special, but it is potentially of use to someone out there.

Other things you will need.  Some sort of small server to run this program.  It
could be a Raspberry Pi or a VM or a Mac.  The printer should be set up with CUPS.  The printer may need a little bit of TLC if you switched to new labels.  Particularly it should probably go through a full calibration to make sure it doesn't goof up too bad
The server should also have a webserver on it.  I used Apache 2, but anything
capable of serving a CGI program should work.
[![Analytics](https://ga-beacon.appspot.com/UA-110461825-1/zebra?pixel)](https://github.com/jhart99/zebra)
