#!/usr/bin/env python3
"""Tell Bing, Yandex, Seznam and other IndexNow engines about new or changed URLs.
Usage: python3 tools/indexnow.py https://www.example.ae/insights/new-post/ [more URLs]
       python3 tools/indexnow.py --all     (submit every URL in dist/sitemap.xml)"""
import sys, json, re, os, urllib.request
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
import config as C
urls = sys.argv[1:]
if urls == ["--all"]:
    sm = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dist/sitemap.xml")).read()
    urls = re.findall(r"<loc>(.*?)</loc>", sm)
host = C.SITE_URL.split("//")[1]
body = json.dumps({"host": host, "key": C.INDEXNOW_KEY, "keyLocation": f"{C.SITE_URL}/{C.INDEXNOW_KEY}.txt", "urlList": urls[:10000]}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
try:
    r = urllib.request.urlopen(req, timeout=30); print("IndexNow", r.status, len(urls), "URLs")
except Exception as e:
    print("IndexNow failed:", e)
