import sys
import string
import re
import requests
import pickle
import zipfile
import bz2
import xmlrpclib
import calendar
import urllib
import difflib
import gzip
import os
import base64
import array
import wave
import zlib
from datetime import date
from cStringIO import StringIO
from PIL import Image, ImageDraw, ImageSequence


"""
Passwords
Level  0: 274877906944
level  1: ocr
level  2: equality
level  3: linkedlist
level  4: peak.html
level  5: channel
level  6: hockey (oxygen)
level  7: integrity
level  8: huge, file
level  9: bull
level 10: 5808
level 11: evil
level 12: disproportional (keep for later: Bert is evil)
level 13: italy
level 14: uzi
level 15: mozart
level 16: romance
level 17: balloons
level 18: un: butter, pw: fly
level 19: idiot (really idiot2)
level 20: produces zip file for level 21
level 21: copper
"""


def main():
    level22()


def level22():
    white = get_url_contents("white.gif",
                             "hex",
                             auth=("butter", "fly"))
    img = Image.open(StringIO(white))

    i = 1
    for frame in ImageSequence.Iterator(img):
        frame.save("frame%d.gif" % i)
        i += 1


def level21():
    zip_data = get_url_contents("unreal.jpg",
                                "hex",
                                auth=("butter", "fly"),
                                headers={"Range": "bytes=%d-" % 1152983631})

    zip_file = zipfile.ZipFile(StringIO(zip_data))
    zip_file.setpassword("invader"[::-1])
    data = zip_file.read("package.pack")
    log = []

    while True:
        if data[-2:][::-1] == 'x\x9c':
            log.append("\n")
            data = data[::-1]
        elif data[0:4] == 'BZh9':
            log.append("#")
            data = bz2.decompress(data)
        elif data[0:2] == 'x\x9c':
            log.append(" ")
            data = zlib.decompress(data)
        else:
            print data[::-1]
            print "".join(log)
            return


def level20():
    def fencing(proc_func, seed=None):
        item = "unreal.jpg"
        sub = "hex"
        auth = ("butter", "fly")
        byterange = re.compile("bytes (\d+)-(\d+)/(\d+)").search

        if seed is None:
            r = get_url(item, sub, auth=auth)
        else:
            r = get_url(item, sub, auth=auth,
                        headers={"Range": "bytes=%d-" % seed})

        while True:
            if r.status_code == 206:
                print r.content

            m = byterange(r.headers.get("content-range", ""))
            if m is None:
                return old_m

            rtn = proc_func(r, m)
            if rtn is False:
                return old_m

            old_m = m
            r = get_url(item, sub, auth=auth,
                        headers={"Range": "bytes=%d-" % rtn})

    def forward(req, match):
        return long(match.group(2)) + 1

    def reverse(req, match):
        return long(match.group(1)) - 1

    last_match = fencing(forward)
    seed = long(last_match.group(3))
    fencing(reverse, seed)

    r = get_url("unreal.jpg",
                "hex",
                auth=("butter", "fly"),
                headers={"Range": "bytes=%d-" % 1152983631})

    write_contents("final", r.content)


def level19():
    data = get_page_comments("bin.html", "hex", auth=("butter", "fly"))

    boundary = re.search("boundary=\"(.+)\"", data).group(1)

    r = "--%s(.+)--%s--" % (boundary, boundary)
    b64 = re.search(r, data, re.DOTALL).group(1)

    b64data = re.search("base64(.+)", b64, re.DOTALL).group(1)
    b64data = b64data.strip(" " + os.linesep)

    raw = base64.standard_b64decode(b64data)

    orig = wave.open(StringIO(raw), "rb")

    rev = wave.open("rev.wav", "wb")
    rev.setparams(orig.getparams())
    frames = array.array("H", orig.readframes(orig.getnframes()))
    frames.byteswap()
    rev.writeframes(frames.tostring())
    rev.close


def level18():
    t = get_url_contents("deltas.gz", "return", auth=("huge", "file"))
    raw = gzip.GzipFile(fileobj=StringIO(t))

    left, right = [], []

    for line in raw:
        l = line.strip()
        left.append(l[:53])
        right.append(l[56:])

    diff = list(difflib.ndiff(left, right))
    out = ["", "", ""]
    for line in diff:
        cmd = line[0]
        data = "".join([chr(int(c, 16)) for c in line[2:].split()])
        if cmd == "-":
            out[0] += data
        elif cmd == "+":
            out[1] += data
        else:
            out[2] += data

    for i in range(3):
        open("18_%i.png" % i, "wb").write(out[i])


def level17():
    current_id = "12345"
    count = 0
    busynothing = re.compile("and the next busynothing is (\d+)").search
    divide = re.compile("Yes. Divide by two and keep going.").search
    cookie = ""

    while True:
        print ".",
        count += 1

        if count > 450:
            print "too many evolutions"
            break

        r = get_url("linkedlist.php", params={"busynothing": current_id})
        t = r.content
        cookie += urllib.unquote_plus(r.cookies["info"])

        if divide(t):
            current_id = str(int(current_id)/2)
            continue

        match = busynothing(t)
        if match is None:
            print t
            break

        current_id = match.group(1)

    print "cookie is ", bz2.decompress(cookie)

    proxy = xmlrpclib.ServerProxy("http://www.pythonchallenge.com/pc/phonebook.php")
    print proxy.phone("Leopold")

    print get_url_contents("violin.php", "stuff", auth=("huge", "file"), cookies={"info":"the flowers are on their way"})


def level16():
    t = get_url_contents("mozart.gif", "return", auth=("huge", "file"))
    i = Image.open(StringIO(t))
    w, h = i.size
    new = Image.new(i.mode, i.size)

    for y in range(h):
        line = [i.getpixel((x,y)) for x in range(w)]
        pivot = line.index(195)
        line = line[pivot:] + line[:pivot]
        [new.putpixel((x, y), line[x]) for x in range(w)]

    new.show()


def level15():
    for i in range(99, 1, -1):
        y = int("1%i6" % i)
        d = date(y, 1, 26)
        if d.weekday() == 0 and calendar.isleap(y):
            print d


def level14():
    def spiral(lx, ly, ux, uy, step):
        x, y, dx, dy, level, d = lx, ly, step, 0, 0, 1

        mx = ux - lx
        if lx == 0:
            mx += 1

        my = uy - ly
        if ly == 0:
            my += 1

        total = mx * my

        for i in range(total):
            yield x, y

            if d == 1 and (x + dx) > (ux - level):
                dx, dy, d = 0, step, 2
            elif d == 2 and (y + dy) > (uy - level):
                dx, dy, d = -step, 0, 3
            elif d == 3 and (x + dx) < level:
                dx, dy, d = 0, -step, 4
                level += 1
            elif d == 4 and (y + dy) < level:
                dx, dy, d = step, 0, 1

            x, y = x + dx, y + dy


    t = get_url_contents("wire.png", "return", auth=("huge", "file"))
    i = Image.open(StringIO(t))
    im = Image.new(i.mode, (100,100))
    data = list(i.getdata())
    px = spiral(0, 0, 99, 99, 1)

    for pt in data:
        im.putpixel(px.next(), pt)

    im.show()


def level13():
    proxy = xmlrpclib.ServerProxy("http://www.pythonchallenge.com/pc/phonebook.php")
    print proxy.phone("Bert")


def level12():
    t = get_url_contents("evil2.gfx", "return", auth=("huge", "file"))

    for x in range(5):
        d = t[x::5]
        im = Image.open(StringIO(d))

        with open("image%i.%s" % (x, im.format.lower()), "wb") as f:
            f.write(d)


def level11():
    t = get_url_contents("cave.jpg", "return", auth=("huge", "file"))
    i = Image.open(StringIO(t))
    data = list(i.getdata())
    odd = data[1::2]
    even = data[::2]

    o_im = Image.new("RGB", i.size)
    o_im.putdata(odd)

    e_im = Image.new("RGB", i.size)
    e_im.putdata(even)

    o_im.show()
    e_im.show()


def level10():
    def las(s):
        output = ""
        cnt = 0
        old = s[0]
        for ch in s:
            if old == ch:
                cnt += 1
            else:
                output += "%i%s" % (cnt, old)
                cnt = 1
                old = ch
        output += "%i%s" % (cnt, old)
        return output

    cur = ["1"]
    for x in xrange(1, 31, 1):
        cur.append(las(cur[-1]))

    print len(cur[30])


def level9():
    i = Image.new("RGB", (640, 480))
    line1 = [146,399,163,403,170,393,169,391,166,386,170,381,170,371,170,355,169,346,167,335,170,329,170,320,170,310,171,301,173,290,178,289,182,287,188,286,190,286,192,291,194,296,195,305,194,307,191,312,190,316,190,321,192,331,193,338,196,341,197,346,199,352,198,360,197,366,197,373,196,380,197,383,196,387,192,389,191,392,190,396,189,400,194,401,201,402,208,403,213,402,216,401,219,397,219,393,216,390,215,385,215,379,213,373,213,365,212,360,210,353,210,347,212,338,213,329,214,319,215,311,215,306,216,296,218,290,221,283,225,282,233,284,238,287,243,290,250,291,255,294,261,293,265,291,271,291,273,289,278,287,279,285,281,280,284,278,284,276,287,277,289,283,291,286,294,291,296,295,299,300,301,304,304,320,305,327,306,332,307,341,306,349,303,354,301,364,301,371,297,375,292,384,291,386,302,393,324,391,333,387,328,375,329,367,329,353,330,341,331,328,336,319,338,310,341,304,341,285,341,278,343,269,344,262,346,259,346,251,349,259,349,264,349,273,349,280,349,288,349,295,349,298,354,293,356,286,354,279,352,268,352,257,351,249,350,234,351,211,352,197,354,185,353,171,351,154,348,147,342,137,339,132,330,122,327,120,314,116,304,117,293,118,284,118,281,122,275,128,265,129,257,131,244,133,239,134,228,136,221,137,214,138,209,135,201,132,192,130,184,131,175,129,170,131,159,134,157,134,160,130,170,125,176,114,176,102,173,103,172,108,171,111,163,115,156,116,149,117,142,116,136,115,129,115,124,115,120,115,115,117,113,120,109,122,102,122,100,121,95,121,89,115,87,110,82,109,84,118,89,123,93,129,100,130,108,132,110,133,110,136,107,138,105,140,95,138,86,141,79,149,77,155,81,162,90,165,97,167,99,171,109,171,107,161,111,156,113,170,115,185,118,208,117,223,121,239,128,251,133,259,136,266,139,276,143,290,148,310,151,332,155,348,156,353,153,366,149,379,147,394,146,399]
    line2 = [156,141,165,135,169,131,176,130,187,134,191,140,191,146,186,150,179,155,175,157,168,157,163,157,159,157,158,164,159,175,159,181,157,191,154,197,153,205,153,210,152,212,147,215,146,218,143,220,132,220,125,217,119,209,116,196,115,185,114,172,114,167,112,161,109,165,107,170,99,171,97,167,89,164,81,162,77,155,81,148,87,140,96,138,105,141,110,136,111,126,113,129,118,117,128,114,137,115,146,114,155,115,158,121,157,128,156,134,157,136,156,136]

    draw = ImageDraw.Draw(i)
    draw.line(line1, fill="#FF0000", width=1)
    draw.line(line2, fill="#0000FF", width=1)

    i.show()


def level8():
    def decode(cypher):
        return bz2.decompress(cypher)

    un = 'BZh91AY&SYA\xaf\x82\r\x00\x00\x01\x01\x80\x02\xc0\x02\x00 \x00!\x9ah3M\x07<]\xc9\x14\xe1BA\x06\xbe\x084'
    pw = 'BZh91AY&SY\x94$|\x0e\x00\x00\x00\x81\x00\x03$ \x00!\x9ah3M\x13<]\xc9\x14\xe1BBP\x91\xf08'

    print decode(un)
    print decode(pw)


def level7():
    t = get_url_contents("oxygen.png")
    i = Image.open(StringIO(t))

    w, h = i.size
    h /= 2
    pixels = [i.getpixel((x, h)) for x in xrange(0, w, 7)]
    chars = [chr(r) for r, g, b, a in pixels if r == g == b]
    data = "".join(chars)

    print data
    digits = re.compile("(\d+)")
    print "".join([chr(int(c)) for c in digits.findall(data)])


def level6():
    comments = ""
    t = get_url_contents("channel.zip")
    z = zipfile.ZipFile(StringIO(t))
    nothing = re.compile("nothing is (\d+)").search
    divide = re.compile("[dD]ivide").search
    current_id = "90052"

    while True:
        print "trying %s" % current_id

        f = z.open(current_id + ".txt")
        fi = z.getinfo(current_id + ".txt")

        d = f.read()
        comments += fi.comment

        if divide(d):
            print "divide"
            current_id = str(int(current_id)/2)
            continue

        match = nothing(d)
        if match is None:
            print d
            print comments
            break

        current_id = match.group(1)


def level5():
    p = pickle.loads(get_url_contents("banner.p"))
    for l in p:
        print "".join([c * n for c, n in l])


def level4():
    current_id = "12345"
    count = 0
    nothing = re.compile("and the next nothing is (\d+)").search
    divide = re.compile("Yes. Divide by two and keep going.").search

    while True:

        print "trying %s" % current_id
        count += 1

        if count > 450:
            print "too many evolutions"
            break

        t = get_url_contents("linkedlist.php", params={"nothing": current_id})

        if divide(t):
            print "divide"
            current_id = str(int(current_id)/2)
            continue

        match = nothing(t)
        if match is None:
            print t
            break

        current_id = match.group(1)


def level3():
    data = get_page_comments("equality.html")
    print "".join(re.findall("[a-z][A-Z]{3}([a-z])[A-Z]{3}[a-z]", data))


def level2():
    data = get_page_comments("ocr.html")
    data = re.search("<!--(.+)", data, re.DOTALL).group(1).strip(" " + os.linesep)
    print "".join(re.findall("[a-zA-Z]", data))


def level1():

    def convert(crypt):
        trans = string.maketrans(
            string.ascii_lowercase,
            string.ascii_lowercase[2:] + string.ascii_lowercase[:2])
        return string.translate(crypt, trans)

    crypt1 = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."
    crypt2 = "map"

    print convert(crypt1)
    print convert(crypt2)


def level0():
    print 2**38


def write_contents(name, s):
    with open(name, "wb") as f:
        f.write(s)


def get_file_contents(filename):
    return "".join(line for line in open(filename, "r"))


def get_url_contents(url, suburl="def", **request_args):
    r = get_url(url, suburl, **request_args)
    return r.content


def get_url(url, suburl="def", **request_args):
    base = "http://www.pythonchallenge.com/pc/%s/" % suburl
    r = requests.get(base + url, **request_args)
    return r


def get_page_comments(url, suburl="def", **request_args):
    r = get_url(url, suburl, **request_args)

    match = re.search("<!--(.+)-->", r.content, re.DOTALL)
    if match is None:
        return ""

    return match.group(1)


if __name__ == "__main__":
    sys.exit(main())