import requests, re
from bs4 import BeautifulSoup, element

class Parser:
    def __init__(self, id):
        self.url = "https://info.braude.ac.il/yedion/fireflyweb.aspx"\
                    "?APPNAME=&PRGNAME=S_LOOK_FOR_NOSE&ARGUMENTS=SubjectCode&"\
                    "SubjectCode=" + str(id)
        self.html = self.get_html()
        self.types_list = self.get_types()
        self.data_list = self.get_data()

    def get_html(self):
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.Timeout:
            raise ValueError(f"Request timed out while fetching course data")
        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch course data: {e}")
    
    def get_name(self):
        topic_string = self.html.find("h2", class_="TextAlignCenter")
        name = str(topic_string.text.split("שנה")[0].split("קורס")[1])
        return name[1:len(name) - 1]

    def get_types(self):
        types_list = self.html.find_all(string=re.compile("קורס מסוג"))
        for index, type_string in enumerate(types_list):
            types_list[index] = re.sub(r'\s+', '', type_string).replace("קורסמסוג",'')
        return types_list
    
    def get_about(self):
        elements = self.html.find("p").children
        about_list = []
        for index, str in enumerate(elements):
            if isinstance(str, element.Tag) or index == 0:
                continue
            about_list.append(str)
        return about_list

    def get_data(self):
        # Find all potential lesson data containers
        all_data_divs = self.html.find_all('div', class_='Table container ncontainer WithSearch')
        
        # Filter to only include divs with exactly 2 rows (header + data)
        valid_data_list = []
        for div in all_data_divs:
            rows = div.find_all("div", class_="row")
            if len(rows) == 2:
                valid_data_list.append(div)
        
        return valid_data_list