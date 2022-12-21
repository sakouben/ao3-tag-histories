# ao3-tag-histories
detailed day-by-day histories of works under a specific tag on ao3.

---

TODO:

data visualization (further options)

documentation

---
## Example: Setup

```
from az0 import *

taglist = [
    Tag(
        url="https://archiveofourown.org/tags/Albedo*s*Tighnari%20(Genshin%20Impact)/works", 
        canon_identifier="Albedo/Tighnari"
    ),
    
    Tag(
        url="https://archiveofourown.org/tags/Gorou*s*Scaramouche%20(Genshin%20Impact)/works",
        canon_identifier="Gorou/Scaramouche"
    ),
    
    Tag(
        url="https://archiveofourown.org/tags/Bennett*s*Chongyun%20(Genshin%20Impact)/works",
        canon_identifier="Bennett/Chongyun"
    ),
    
    Tag(
        url="https://archiveofourown.org/tags/Kaedehara%20Kazuha*s*Xiao%20%7C%20Alatus/works",
        canon_identifier="Kazuha/Xiao"
    )
]

PrimaryDB = TagDB("tag-histories.csv", "1 Jan 2019", "1 Jan 2023")

PrimaryDB.setup_DB()
PrimaryDB.addtag_DB(taglist[0])
PrimaryDB.addtag_DB(taglist[1])
PrimaryDB.addtag_DB(taglist[2])
PrimaryDB.addtag_DB(taglist[3])

df = PrimaryDB.read_DB()
```

## Example: Updating

```
from az0 import *

PrimaryDB = TagDB("tag-histories.csv")
tag = Tag(url="https://archiveofourown.org/tags/Venti*s*Xiao%20%7C%20Alatus%20(Genshin%20Impact)/works", canon_identifier="Venti/Xiao")

PrimaryDB.addtag_DB(tag)
```
