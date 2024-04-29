from RPA.Browser.Selenium import Selenium
from selenium.webdriver.common.keys import Keys
import app.constants as constants

class Browser:
    def __init__(self, browser_lib=Selenium) -> None:
        self.browser = browser_lib()
    
    def navigate(self, title) -> None:
        self.browser.open_available_browser(title)
        
    def close_browser(self) -> None:
        self.browser.close_all_browsers()

    def find_element_by_xpath(self,xpath):
        return self.browser.find_element(xpath)

    def input_text(self,xpath,title):
        self.browser.input_text(xpath,title['Movie'])
        self.browser.press_keys(xpath,Keys.ENTER)

    def find_elements(self,tag):
        return self.browser.find_elements(tag)
    
    def wait_until_page_contains_element(self,element):
        self.browser.wait_until_page_contains_element(element)

    def getText(self,element,css):
        return self.browser.get_text(element,css)

    def get_webelements(self ,xpath):
        return self.browser.get_webelement(xpath)
    def get_element_count(self,element):
        return self.browser.get_element_count(element)
  


    
