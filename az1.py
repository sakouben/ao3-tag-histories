import requests
import re
import time
import pandas as pd
from datetime import datetime

today_strf_Ymd = pd.Timestamp(datetime.today().strftime('%Y-%m-%d'))

class Tag:
    def __init__(self, url, canon_identifier, pages_of_content="Unloaded", dt_list="Unloaded"):
        self.url = url
        self.canon_identifier = canon_identifier
        self.pages_of_content = pages_of_content
        self.dt_list = dt_list
        
        
def tagdf_init(startdate, enddate=today_strf_Ymd):
    start = pd.Timestamp(startdate)
    end = pd.Timestamp(enddate)
    
    days = pd.date_range(start=start, end=end)
    super_df = pd.DataFrame(index=days)
        
    return super_df


def addcolumn(df, Tag): #as Ship object;
    df[Tag.canon_identifier] = 0 #creates empty column
    
    try:
        for timestamp in Tag.dt_list:
            df.at[timestamp.strftime("%Y-%m-%d"), Tag.canon_identifier] += 1
    except:
        Tag.load_values()
        for timestamp in Tag.dt_list:
            df.at[timestamp.strftime("%Y-%m-%d"), Tag.canon_identifier] += 1
            
    return df


class TagDB:
    def __init__(self, filename, startdate=None, enddate=None):
        self.filename = filename
        self.startdate = startdate
        self.enddate = enddate
    
    def setup_DB(self):
        df = tagdf_init(self.startdate, self.enddate)
        df.to_csv(self.filename)
        
    def read_DB(self):
        df = pd.read_csv(self.filename, index_col=0)
        return df
    
    def addtag_DB(self, tag):
        df = self.read_DB()
        df = addcolumn(df, tag)
        df.to_csv(self.filename)
        
    def tags(self):
        df = self.read_DB()
        return df.columns.values.tolist()
