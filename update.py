import sys
import requests
import re
import time
import az0

def scode(url):
    return requests.get(url).status_code

def determine_canon(url):
    if scode(url) == 404:
        return -1

    response = requests.get(url)
    content = str(response.content)
    synloc = content.find("a synonym of")

    if synloc != -1: #case of non-canon tag
        content = content[synloc:synloc+200]
        spanpair = re.search('g" href="/t.*?>', str(response.content)[synloc:synloc+200]).span()
        canon_url_ending = content[spanpair[0]+9:spanpair[1]-2]
        canon_url = f"https://archiveofourown.org{canon_url_ending}"
    else: #case of canon tag
        canon_url = url

    return canon_url

def guess():
    name1 = sys.argv[1]
    name2 = sys.argv[2]

    url_1 = f"https://archiveofourown.org/tags/{name1}*s*{name2}%20(Genshin%20Impact)"
    url_2 = f"https://archiveofourown.org/tags/{name2}*s*{name1}%20(Genshin%20Impact)"

    print("current process: determining canon url... (1/2) [108]")
    canon_url = determine_canon(url_1)

    if canon_url == -1:
        print("url_1 failed. attempting to use url_2... [109]")
        print("current process: determining canon url... (2/2) [110]")
        time.sleep(7)
        canon_url = determine_canon(url_2)

    if canon_url == -1:
        print("canon url determination failed. reverting to manual input... [111]")
        raise Exception(0)

    

    final_url = f"{canon_url}/works"
    canon_identifier = f"{name1}/{name2}"
    
    print(f"url: {final_url}\ncanon identifier: {canon_identifier}  [106]")
    print("Warning! Does this set of data look correct? Reply with (y/n) necessary before proceeding. [107]")

    if input() == "y":
        print("Generated url has been deemed correct. Proceeding to data extraction.")
        return {"url":final_url, "canon_identifier":canon_identifier}
    else:
        print("Exception: generated url incorrect. Proceeding to manual input.")
        raise Exception(0)
    

def specify():
    print("URL:")
    url = input()

    print("Canon Identifier:")
    canon_identifier = input()

    return {"url":url, "canon_identifier":canon_identifier}


def run():
    print("current process: setting up...")
    try:
        if sys.argv[1] != "--m":
            rv = guess()
        else:
            print("Manual input requested. Proceeding to input.")
            rv = specify()
    except:
        print("Lookup failed. Please manually enter URL and canon identifier here instead.")
        rv = specify()
    
    url = rv['url']
    canon_identifier = rv['canon_identifier']

    PrimaryDB = az0.TagDB("tag-histories.csv")
    tag = az0.Tag(
        url=url,
        canon_identifier=canon_identifier
        )

    PrimaryDB.addtag_DB(tag)



run()

    