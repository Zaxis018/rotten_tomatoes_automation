from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from qrlib.QRComponent import QRComponent

class Scrape(QRComponent):
    def __init__(self, browser):
        self.browser = browser 

    def search_match(self, title, url,db):
        # input movie into search bar and press Enter
        self.browser.go_to(url)
        xpath = '//*[@id="header-main"]/search-algolia'

        # self.browser.wait_until_page_contains_element('//*[@id="header-main"]/search-algolia/search-algolia-controls/input',timeout=30)
        # self.browser.input_text(xpath,title['Movie'])
        # self.browser.press_keys(xpath,Keys.ENTER)

        # initialize variables
        movie_title = title.strip()
        movie_index = None
        Latest_movie_date = None

        # dictionary to store scraped data
        movie_info = {}
        movie_info['Name'] = movie_title

        # find number of movies resulted in search 
        Rows=self.browser.get_element_count('//*[@id="search-results"]/search-page-result[1]/ul/search-page-media-row')
        try:
            # Search all movies with corresponding xpath and choose latest movie
            for i in range(1, Rows + 1):

                # for each row get necessary data
                try:
                    self.browser.scroll_element_into_view(f'//*[@id="search-results"]/search-page-result[1]/ul/search-page-media-row[{i}]/a[2]')
                    Movie_name = self.browser.get_text(f'//*[@id="search-results"]/search-page-result[1]/ul/search-page-media-row[{i}]/a[2]')
                    element = self.browser.find_element(f'//*[@id="search-results"]/search-page-result[1]/ul/search-page-media-row[{i}]')
                    release_date = int(element.get_attribute("releaseyear"))
                    if Movie_name == movie_title:
                        if Latest_movie_date is None or (release_date is not None and release_date > Latest_movie_date):
                            Latest_movie_date = release_date
                            movie_index = i
            
                except StaleElementReferenceException:
                    self.browser.scroll_element_into_view(f'//*[@id="search-results"]/search-page-result[1]/ul/search-page-media-row[{i}]/a[2]')
    
            # CLick the Link for the given movie with its index and see details
            if movie_index is not None:
                try:
                    self.browser.scroll_element_into_view(f'//*[@id="search-results"]/search-page-result[1]/ul/search-page-media-row[{movie_index}]/a[2]')
                    self.browser.wait_until_element_is_visible(f'//*[@id="search-results"]/search-page-result[1]/ul/search-page-media-row[{movie_index}]/a[2]',timeout=10)

                    # click movie link
                    self.browser.click_element(f'//*[@id="search-results"]/search-page-result[1]/ul/search-page-media-row[{movie_index}]/a[2]')
                except StaleElementReferenceException:
                    self.browser.click_element(f'//*[@id="search-results"]/search-page-result[1]/ul/search-page-media-row[{movie_index}]/a[2]')


            # get tomato and audience score
            try:
                tomato_score = self.browser.get_text('//*[@id="modules-wrap"]/div[1]/media-scorecard/rt-button[1]/rt-text')
                audience_score =self.browser.get_text('//*[@id="modules-wrap"]/div[1]/media-scorecard/rt-button[2]/rt-text')
            except:
                tomato_score = 'NA'
                audience_score = 'NA'


            # get storyline
            storyline = self.browser.get_text('//*[@id="modules-wrap"]/div[1]/media-scorecard/drawer-more/rt-text')
            

            # rating and genres are inside rt-text elements. 
            rt_text_rows=self.browser.get_element_count('//*[@id="hero-wrap"]/div/media-hero/rt-text')  # number of rt_text elements
            # print('rt_text_rows: ', rt_text_rows)

            rating ='NA'
            genre_list=[]
            for i in range(1,rt_text_rows+1):

                slot_value = self.browser.get_element_attribute(f'//*[@id="hero-wrap"]/div/media-hero/rt-text[{i}]', 'slot')
                if slot_value == 'genre':
                    genre_list.append(self.browser.get_text(f'//*[@id="hero-wrap"]/div/media-hero/rt-text[{i}]'))

                elif slot_value == 'ratingsCode':
                    rating = self.browser.get_text(f'//*[@id="hero-wrap"]/div/media-hero/rt-text[{i}]')


            # fill dictionary with extracted values
            movie_info['Tomato Score'] = tomato_score
            movie_info['Audience Score'] = audience_score
            movie_info['Storyline'] = storyline
            movie_info['Rating'] = rating
            movie_info['Genres'] = genre_list


            # for critic review , need to click differnet link
            critic_review_status=self.browser.is_element_visible('//*[@id="critics-consensus"]/a')
            if critic_review_status:
                self.browser.scroll_element_into_view('//*[@id="critics-consensus"]/a')
                self.browser.click_element('//*[@id="critics-consensus"]/a')
                # click top critics button again
                self.browser.wait_until_element_is_visible('//*[@id="reviews"]/nav/ul/li[2]/a')
                self.browser.click_element('//*[@id="reviews"]/nav/ul/li[2]/a')

            # Create list to append all reviews
            review_list=[]

            review_rows = self.browser.get_element_count('//*[@id="reviews"]/div[1]/div') # number of reviews resulted
            # print ('Review rows: ' , review_rows)

            for i in range(1,review_rows+1):
                review_list.append(self.browser.get_text(f'//*[@id="reviews"]/div[1]/div[{i}]/div[2]/p[1]'))
                if i==5: # only 5 reviews needed
                    break          

            # Append Null if No review exists
            while len(review_list) < 5:
                review_list.append('Null')

            # fill dictionary with reviews and status
            movie_info['Reviews'] = review_list
            movie_info['Status'] = 'Success'

        except:
            movie_info['Status'] = 'Not Found'

        # if movie not found append null to all
        if movie_info['Status'] == 'Not Found':
            movie_info['Audience Score'] = 'Null'
            movie_info['Tomato Score'] = 'Null'
            movie_info['Storyline'] = 'Null'
            movie_info['Rating'] = 'Null'
            movie_info['Genres'] = 'Null'
            movie_info['Reviews'] =["Null", "Null","Null", "Null","Null"]


        # print(movie_info)
        # print('review1: ', movie_info['Reviews'][0])

        genres = "".join(movie_info['Genres']) # make a single string from list of genres
        # print('genres: ' ,genres)

        db.insert_to_database(movie_info['Name'],movie_info['Tomato Score'],movie_info['Audience Score'],movie_info['Storyline'],movie_info['Rating'],genres,movie_info['Reviews'][0],movie_info['Reviews'][1],movie_info['Reviews'][2],movie_info['Reviews'][3],movie_info['Reviews'][4],movie_info['Status'])
        
    def movie_info(self, title):
        pass