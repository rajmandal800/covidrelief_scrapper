import selenium as selenium
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os
from selenium.webdriver.chrome.options import Options
import json
class CovidRelief:

    def __init__(self):
        url = 'https://covidrelief.glideapp.io/'
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
        options = Options()
        options.add_argument("--headless")
        options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
        self.driver = webdriver.Chrome(options=options,executable_path = DRIVER_BIN)
        self.vcities = []
        self.hospitalNames = []


    def loopCities(self):
        cities = self.driver.find_elements_by_class_name('ReactVirtualized__Grid__innerScrollContainer')[0]        
        childs = cities.find_elements_by_xpath("./child::*")
        length = len(childs)
        for index,info in enumerate(childs):
            x = info.find_elements_by_class_name("textStyle")[0].get_attribute('innerHTML')
            y = info.find_elements_by_class_name("textDetailStyle")[0].get_attribute('innerHTML')
            self.vcities.append({"name":x,"beds":y.splitlines()})
            # self.hospitalNames.append(x)
            
            if index==length-1:
                self.driver.execute_script("arguments[0].scrollIntoView();", info)
                

            
            
        
    
    def saveData(self,data):
        f = open(self.filename+".txt", "w")
        f.write(json.dumps(data))
        f.close()
        
    def getScroll(self):
        #url =   "https://covidrelief.glideapp.io/dl/ewAiAHQAIgA6ADAALAAiAHMAIgA6ACIAbQBlAG4AdQAtADIAMQBlADcANgA4ADkANwAtAGQANgBiADYALQA0ADQANgAzAC0AOABmAGMAMQAtADcAMwA1ADAAOQAxADgAMABlADgAZgA2AC0AZAA5AGUAMwBlADUAMwAwADgAYgBlAGUAYgBhAGQAZAA5ADUAOAAwADEAMABmAGIAMgAwADgANAAzADcAMgAzACIALAAiAHIAIgA6ACIAWgAzAHMAUwBnAGQASQBzAFEATQB5AGgAUgA1AFkALgBFAHMAbQBqAG0AQQAiACwAIgBuACIAOgAiAEEAaABtAGUAZABhAGIAYQBkACIAfQA%3D"
        #self.driver.get(url)
        #time.sleep(2)
        scrollView = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div/div[2]')
        scrollHeight = self.driver.execute_script("return arguments[0].scrollHeight",scrollView)
        # scrollTop = self.driver.execute_script("return arguments[0].scrollTop",scrollView)
        # clientHeight = self.driver.execute_script("return arguments[0].clientHeight",scrollView)
        return scrollHeight
        
    def readUrls(self):
        file1 = open('urls.txt', 'r')
        Lines = file1.readlines()
        count = 0
        # Strips the newline character
        for line in Lines:
            count += 1
            yield line.strip()

    def getDirectVacantBeds(self):
    
        for url in self.readUrls():
            self.driver.get(url)
            time.sleep(4)
            self.filename = self.driver.find_elements_by_class_name("summary-title")[0].get_attribute('innerHTML')
            for i in range(16):
                if i==0:
                    self.scrollHeight = self.getScroll()
                if i >2:
                    scrollHeight = self.getScroll()
                    if scrollHeight==self.scrollHeight:
                        break
                    else:
                        self.scrollHeight = scrollHeight
                        self.loopCities()
                        time.sleep(0.5)
                else:
                    self.loopCities()
                    time.sleep(0.5)
            self.vcities = [i for n, i in enumerate(self.vcities) if i not in self.vcities[n + 1:]]
            self.saveData(self.vcities)
            self.vcities = []
            
        #input('Press ENTER to close the automated browser')
        
        self.driver.quit()
    
cr = CovidRelief()
cr.getDirectVacantBeds()




#cr.checkScroll()