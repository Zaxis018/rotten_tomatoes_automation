import time
from qrlib.QRProcess import QRProcess
from qrlib.QRDecorators import run_item
from qrlib.QRRunItem import QRRunItem
from DefaultComponent import DefaultComponent
from robot.libraries.BuiltIn import BuiltIn
from qrlib.QREnv import QREnv


from RPA.Browser.Selenium import Selenium
from urllib.parse import quote
from app.scrape import Scrape
from RPA.Excel.Files import Files
from app.connect_database import DatabaseOperation as database

class DefaultProcess(QRProcess):

    def __init__(self):
        super().__init__()
        self.default_component = DefaultComponent()
        self.register(self.default_component)
        self.data = []
        
        self.movie_vault = None
        file = 'app/movies.xlsx'
        excel = Files()
        excel.open_workbook(file)
        self.data = excel.read_worksheet(header = True)
        self.db = database()
        excel.close_workbook()
        self.browser = Selenium()
        self.Scraper = Scrape(self.browser)
        BuiltIn().log_to_console("constructor initialized")

    # @run_item(is_ticket=False)
    def before_run(self, *args, **kwargs):
        # open browser

        self.movie_vault = QREnv.VAULTS["movie"]
        self.browser.open_available_browser(url=self.movie_vault["url"])

        # self.browser.maximize_browser_window()
        BuiltIn().log_to_console("Initializing database")
        self.db.create_table()
        BuiltIn().log_to_console("Database initialized")

    # @run_item(is_ticket=False, post_success=False)
    def before_run_item(self, *args, **kwargs):
        pass

    # @run_item(is_ticket=True)
    def execute_run_item(self, *args, **kwargs):
        row =args[0]
        formatted_movie_name = quote(row['Movie'])
        title = row['Movie']
        url = 'https://www.rottentomatoes.com/search?search=' + formatted_movie_name
        self.Scraper.search_match(title,url ,self.db)

    # @run_item(is_ticket=False, post_success=False)
    
    def after_run_item(self, *args, **kwargs):
        pass

    def after_run(self, *args, **kwargs):
        self.db.close_connection()
        self.browser.close_browser()
 
    def execute_run(self):
        for row in self.data:
            self.before_run_item(row)
            self.execute_run_item(row)
            self.after_run_item(row)

