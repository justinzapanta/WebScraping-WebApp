import requests
from bs4 import BeautifulSoup

class Request_Data():
    def __init__ (self, link , request):
        self.html = requests.get(link).text
        self.request = request

class Soup():
    def __init__(self, html, method):
        self.soup = BeautifulSoup(html, method)

    def get(self, tag, type_, name, get):
        try:
            if type_ != 'none':
                if get == 'all':
                    if type_ == 'class':
                        return self.soup.find_all(tag, {type_: name})
                    
                elif get == 'text':
                    return self.get_text(self.soup.find_all(tag, {type_: name}))
                
                else:
                    return self.get_attribute(self.soup.find_all(tag, {type_: name}), get)
                
                return self.soup.find(tag, {type_: name})
            else:
                if get == 'all':
                    return self.soup.find_all(tag)
                
                elif get == 'text':
                    return self.get_text(self.soup.find_all(tag))
                
                else:
                    return self.get_attribute(self.soup.find_all(tag), get)
        except:
            return ['No Item']
                
    def get_text(self, soup):
        temp_list = []
        for data in soup:
            temp_list.append(data.text)
        return temp_list


    def get_attribute(self, soup, get):
        temp_list = []
        for data in soup:
            if data.get(get):
                temp_list.append(data.get(get))
        return temp_list
    


#clean the code im just trying to test if what im thinking is correct after this i'l clean my code
class Filter_soup():
    def __init__(self, soup_result):
        self.soup_result = soup_result

    def filter_get(self):
        try:
            return self.get_text(self.soup_result)
        except:
            return ['No Item']
    
    def filter_attribute(self, get):
        try:
            temp_list = []
            for data in self.soup_result:
                temp_list.append(data[get])
            return temp_list
        except:
            return ['No Item']
 
    def filter_tag_NoClassAndID(self, find_tag):
        try:
            temp_list = []
            for data in self.soup_result:
                if data.find(find_tag):
                    temp_list.append(data.find(find_tag))
            return temp_list
        except:
            return ['No Item']

    def filter_tag_wClassOrID(self, find_tag, class_or_id, type_value):
        try:
            if class_or_id == 'filter-class':
                temp_list = []
                for data in self.soup_result:
                    if data.find(find_tag, class_=type_value):
                        temp_list.append(data.find(find_tag, class_=type_value))
                return temp_list
        except:
            return ['No Item']


    def get_text(self, soup_result):
        temp_list = []
        for data in soup_result:
            temp_list.append(data.text)
        return temp_list
    
        