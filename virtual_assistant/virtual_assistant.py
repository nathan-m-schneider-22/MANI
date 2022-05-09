import imp
from random import choice

from numpy import short
from .shortcuts import check_shortcut
from .outsourced_assistant import call_outsourced_API
from display.display import Display
from bs4 import BeautifulSoup
import time
# A virtual assistant class to handle VA functionality

class VirtualAssistant:
    def __init__(self, display: Display, mock_va: bool = False):
        self.display_instance = display
        self.mock_va = mock_va

    def get_result(self, input: str):
        print("Checking shortcut")
        shortcut = check_shortcut(input)
        self.display_instance.display_loading()

        if shortcut != None:
            print("Found: ", shortcut)
            input = shortcut

        self.display_instance.display_state("send", {"input": input})
        if self.mock_va:
            time.sleep(3)
            file_names = ['weather_response.html', 'calendar.html', 'kilometers_to_miles_response.html','mothers_day_date.html']
            html_file = open(choice(file_names), 'r')

            html_result = html_file.read()
            html_result = self.clean_html(html_result)
            print("Using mock VA response")
            return html_result
        else:
            html_result = call_outsourced_API(input)
            html_result = self.clean_html(html_result)

            print("HTML Results:", html_result)
            # print("Text Result: ", text_result)
            # text_result = text_result[0].upper() + text_result[1:]
            # return text_result, html_result
            return html_result

    def clean_html(self, html_result):
        soup = BeautifulSoup(html_result, features="html.parser")
        for tag in soup.findAll(attrs={'id':'popout'}):
            tag['style'] = 'position: absolute; height:100%; width:100%;'
            
        for tag in soup.findAll(attrs={'class':'popout-content'}):
            tag['style'] = 'position: absolute; left: 50%; top: 50%; -webkit-transform: translate(-50%, -50%); transform: translate(-50%, -50%);'
        
        for div in soup.findAll('div', 'assistant-bar-content'):
            div.extract()

        for div in soup.findAll('div', 'popout-shadow'):
            div.extract()  
        
        for div in soup.findAll('div', attrs={'id':'initial-focus'}):
            div.extract()       

        html_result = str(soup)
        return html_result

    def teardown(self):
        pass
