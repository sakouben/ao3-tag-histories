import requests
from bs4 import BeautifulSoup
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
        
    def ao3_extract_no_pages_of_content(self, url, FLAG_verbose=True):
        #resource accessed. OBEY 7-SECONDS!
        time.sleep(7)
        
        if FLAG_verbose == True:
            print(f"current process: page number extraction for {self.canon_identifier}... (1/2)")
        else:
            pass
        
        maxchar_cut_int = 10000 #arbitrary. increases search speed by truncating initial Soup li-string
        
        s = requests.get(url)
        soup = BeautifulSoup(s.content, 'html.parser')

        li_str = str(soup.findAll("li"))
        k = re.search("<!--title", li_str[:maxchar_cut_int])
        trunc_li_str = li_str[:k.start()]
        page_numbers = re.findall("\d+(?=<\/a)", trunc_li_str)
        
        try:
            pages_of_content = page_numbers[-1]
        except:
            pages_of_content = 1
        
        return pages_of_content
        
    def ao3_extract_dt_list(self, url, FLAG_verbose=True):
        #resource intensive. OBEY 7-SECONDS!
        
        if FLAG_verbose == True:
            print("current process: date-time list extraction... (2/2)")
        else:
            pass
        
        dt_list_return = []
        
        current_page_number = 1
        max_page_number = int(self.pages_of_content)
        
        #add try-except

        
        while current_page_number < max_page_number + 1:
            time.sleep(7)
            
            r = requests.get(str(url + "?page=" + str(current_page_number)))
            soup = BeautifulSoup(r.content, 'html.parser')
            datetime_list = soup.findAll("p", class_="datetime")
            formatted_dt_list = [str(x)[20:31] for x in datetime_list]
            dt_list_return += formatted_dt_list
            
            if FLAG_verbose == True:
                print(str("on page: " + str(current_page_number) + "/" + str(max_page_number)))
            else:
                pass
            
            current_page_number += 1
        
        
        dt_list = [pd.Timestamp(x) for x in dt_list_return]
        
        print("finished loading values")
        
        return dt_list
    
    def load_values(self):
        self.pages_of_content = self.ao3_extract_no_pages_of_content(self.url)
        self.dt_list = self.ao3_extract_dt_list(self.url)
        
        
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
