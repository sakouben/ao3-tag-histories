import sys
import requests
import re
import time
import az0

def guess():
    name1 = sys.argv[1]
    name2 = sys.argv[2]

    url_1 = f"https://archiveofourown.org/tags/{name1}*s*{name2}%20(Genshin%20Impact)"
    url_2 = f"https://archiveofourown.org/tags/{name2}*s*{name1}%20(Genshin%20Impact)"

    print("current process: url guessing... (1/2)")
    if requests.get(url_1) != 404:
        intermediary_url = url_1
        print("current process: url successfully determined, proceeding to next step (2/2)")
    else:
        print("current process: url1 failed, trying url2... (1/2)")

    time.sleep(7)

    print("current process: url guessing... (2/2)")
    if requests.get(url_2) != 404:
        intermediary_url = url_2
        print("current process: url successfully determined, proceeding to next step (2/2)")
    else:
        print("Exception: url not generated. Proceeding to manual input.")
        raise Exception(0)
        
    
    s = requests.get(intermediary_url)
    content = str(s.content)[10000:]
    fms = re.search('s\/.*?\/w', content)
    rstring = str(fms.group()[2:len(fms.group())-2])
    
    final_url = f"https://archiveofourown.org/tags/{rstring}/works"
    canon_identifier = f"{name1}/{name2}"
    
    print(f"url: {final_url},\ncanon identifier: {canon_identifier}")
    print("Warning! Does this set of data look correct? Reply with (y/n) necessary before proceeding.")

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

    