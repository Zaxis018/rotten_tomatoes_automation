from app.connect_database import DatabaseOperation
from app.ExcelReader import ExcelReader
from app.browser import Browser
from app.scrape import Scrape
import app.constants as constants
from RPA.Excel.Files import Files
from RPA.Browser.Selenium import Selenium
from app.connect_database import DatabaseOperation as database

class Process:
    def __init__(self) -> None:
        self.browser = Selenium()

    def before_run_process(self):
        # open browser
        self.browser.open_available_browser("https://www.rottentomatoes.com/")  
        
    def run_process(self):
        Scraper = Scrape(self.browser)

        file = 'files/movies.xlsx'
        excel = Files()
        excel.open_workbook(file)
        data = excel.read_worksheet(header = True)

        db = database()
        db.create_table()

        excel.close_workbook()
        
        for row in data:
            Scraper.search_match(row,db)

        db.close_connection()
    
    def after_run_process(self):
        self.browser.close_browser()
