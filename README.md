# ao3-tag-histories
detailed day-by-day histories of numbers of works under a specific tag on ao3.

---

TODO:

reorganization

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

## Additional Notes

Due to technical constraints that I do not understand, the script necessary for updating the database (`az0`) and the one that exists to support the running of the Streamlit app (`az1`) must be separated, despite the latter being in essence a subset of the former. 

###The general structure of the database updating process is as follows:

1. the creation of a `TagDB` object by passing the path to the csv database file to the `az0.TagDB` constructor;
1. the specification of a new `Tag` object to be added, via passing the ao3 url and a "canon identifier" (an arbitrary name that will be used as the column name in the internal DataFrame) to the `az0.Tag` constructor;
1. the addition of this `Tag` object to the previously constructed `TagDB` object via its `addtag_DB` method, specifying as the sole argument the `Tag` object. It is worth noting that this step is by far the most time consuming, as it may require hundreds of HTTP requests being made, which *must* be spaced out with a minimum of 7s between them. it is a combination of two substeps;
    1. the substep involving the HTTP requests being made, the data gathered being processed, and the internal DataFrame being updated accordingly;
    1. the substep that updates the csv *file* originally supplied in the path in the argument for the `az0.TagDB` constructor. This is done automatically, and is not reversible with any method supplied in `TagDB`. It is not possible to halt the process before this occurs by supplying an argument to the `TagDB.add_tag()` method.
