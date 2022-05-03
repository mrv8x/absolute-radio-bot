import datetime
import glob
import os
from datetime import datetime
from datetime import timedelta
from time import sleep

# Tray Icon
import pystray
from PIL import Image, ImageDraw
from pystray import Icon as icon
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

# ABSOLUT  RADIO
global interval_min
interval_min = 1  # Numeric in minutes
global processNum_1_fileNum_1
global processNum_2_fileNum_1
global processNum_2_fileNum_2
global env
global driver

URL1 = 'http://radiofeeds.co.uk/mp3.asp'
URL2 = 'http://lsn.to/ABS'
URL3 = 'https://www.mysqueezebox.com/index/Home'

CredentialUsername = 'realradio@gmail.com'
CredentialPass = '96transam'

dest_dir = os.path.expandvars('%userprofile%\Downloads')

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options.log.level = "trace"
'''options.add_argument("-devtools")'''


# options.add_argument("--headless")

# This code open the downloaded file and grab the URL in within then ir returns that url to main code.
def GrabStringFromFile(latest_file):
    with open(latest_file) as my_file:
        for a in my_file:
            sdato = a.split('\n')
            for s in sdato:
                if s.find('File1=') != -1:
                    return (s.split('File1='))[1]


# this code look for the files required by customer
def maincode():
    env = os.environ['USERPROFILE']
    driver = webdriver.Firefox(executable_path=r'' + env + '\AppData\Local\SeleniumBasic\geckodriver.exe',
                               options=options)
    try:
        driver.get(URL1)
    except:
        icon.icon = image = Image.new('RGB', (64, 64), 'red')
    sleep(5)
    lista = driver.find_elements(by=By.TAG_NAME, value='a')
    for a in lista:
        dato = a.get_attribute('href')
        floatnl = False
        try:
            if dato.find('absoluteradio-mp3') != -1 and floatnl is False:
                processNum_1_fileNum_1 = a.get_attribute('href')
                floatnl = False
                a.click()
                list_of_files = glob.glob(dest_dir + '\*.pls')  # * means all if need specific format then *.csv
                latest_file = max(list_of_files, key=os.path.getctime)
                processNum_1_fileNum_1 = GrabStringFromFile(latest_file)
                break
        except:
            pass

    driver.get(URL2)
    driver.implicitly_wait(10)
    sleep(5)
    try:
        # loops thru all a.href in page but only grabs those called "absoluteradiohigh" and "absoluteradio-mp3"
        lista = driver.find_elements(by=By.TAG_NAME, value='a')
        for a in lista:
            dato = a.get_attribute('href')
            floatnl1 = False
            if dato.find('absoluteradiohigh-aac') != -1 and floatnl1 is False:
                processNum_2_fileNum_1 = a.get_attribute('href')
                Flgctrl1 = True
                a.click()
                list_of_files = glob.glob(dest_dir + '\*.pls')  # * means all if need specific format then *.csv
                latest_file = max(list_of_files, key=os.path.getctime)
                processNum_2_fileNum_1 = GrabStringFromFile(latest_file)

            floatnl2 = False
            if dato.find('absoluteradio-mp3') != -1 and floatnl2 is False:
                processNum_2_fileNum_2 = a.get_attribute('href')
                a.click()
                floatnl2 = True
                list_of_files = glob.glob(dest_dir + '\*.pls')  # * means all if need specific format then *.csv
                latest_file = max(list_of_files, key=os.path.getctime)
                processNum_2_fileNum_2 = GrabStringFromFile(latest_file)
    except:
        icon.icon = image = Image.new('RGB', (64, 64), 'red')

    # Final process - Impact three files at the end
    try:
        # iNSERT FILE NAMES IN FIELDS
        driver.get(URL3)
        driver.implicitly_wait(10)
        driver.find_element(by=By.CSS_SELECTOR, value='#header_right > a:nth-child(1)').click()
        # fill input username
        elementInput = driver.find_element(by=By.XPATH, value='//*[@id="email"]')
        elementInput.click()
        elementInput.send_keys(CredentialUsername)

        # fill input password
        elementInput = driver.find_element(by=By.XPATH, value='//*[@id="password"]')
        elementInput.click()
        elementInput.send_keys(CredentialPass)

        # Press login
        a = driver.find_element(by=By.XPATH, value='//*[@id="ext-gen3"]')
        a.click()
        a = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/a[5]')
        a.click()
        sleep(5)
        # Click on edit in all buttons by one shoot
        driver.find_element(by=By.CSS_SELECTOR,
                            value='#draggable_15028611 > span:nth-child(4) > a:nth-child(1)').click()
        driver.find_element(by=By.CSS_SELECTOR,
                            value='#draggable_137179541 > span:nth-child(4) > a:nth-child(1)').click()
        driver.find_element(by=By.CSS_SELECTOR,
                            value='#draggable_137185361 > span:nth-child(4) > a:nth-child(1)').click()

        # FILE NUM1 --Input data and save it
        # b = ActionChains(driver)
        # click on first cell
        try:
            driver.find_element(by=By.CSS_SELECTOR, value='#edit_title_15028611').click()
            driver.find_element(by=By.CSS_SELECTOR, value='#edit_title_15028611').send_keys(Keys.TAB)
            driver.find_element(by=By.CSS_SELECTOR, value='#edit_url_15028611').send_keys(Keys.DELETE)
            driver.find_element(by=By.CSS_SELECTOR, value='#edit_url_15028611').send_keys(processNum_1_fileNum_1)
            # driver.find_element(by=By.CSS_SELECTOR, value='#draggable_15028611 > form:nth-child(1) > input:nth-child(4)').click()
        except:
            icon.icon = image = Image.new('RGB', (64, 64), 'red')

        # FILE NUM2 --
        try:
            driver.find_element(by=By.CSS_SELECTOR, value='#edit_url_137185361').click()
            driver.find_element(by=By.CSS_SELECTOR, value='#edit_title_137185361').send_keys(Keys.TAB)
            driver.find_element(by=By.CSS_SELECTOR, value='#edit_url_137185361').send_keys(Keys.DELETE)
            driver.find_element(by=By.CSS_SELECTOR, value='#edit_url_137185361').send_keys(processNum_2_fileNum_1)
            # driver.find_element(by=By.CSS_SELECTOR, value='#draggable_137185361 > form:nth-child(1) > input:nth-child(4)').click()
        except:
            icon.icon = image = Image.new('RGB', (64, 64), 'red')

        # FILE NUM3--
        try:
            driver.find_element(by=By.CSS_SELECTOR, value='#edit_url_137179541').click()
            driver.find_element(by=By.CSS_SELECTOR, value='#edit_title_137179541').send_keys(Keys.TAB)
            driver.find_element(by=By.CSS_SELECTOR, value='#edit_title_137179541').send_keys(Keys.DELETE)
            driver.find_element(by=By.CSS_SELECTOR, value='#edit_url_137179541').send_keys(processNum_2_fileNum_2)
            # driver.find_element(by=By.CSS_SELECTOR, value='#draggable_137179541 > form:nth-child(1) > input:nth-child(4)').click()
        except:
            icon.icon = image = Image.new('RGB', (64, 64), 'red')

        sleep(20)
    except:
        icon.icon = image = Image.new('RGB', (64, 64), 'red')
        pass

    driver.close()


# This will call maincode() every five minutes
def loop():
    # time information prepared to be published by the icon at systray
    b = datetime.today()
    c = datetime.today() + timedelta(minutes=5)
    c.strftime("%d/%m/%Y %H:%M")
    icon.icon = image = Image.new('RGB', (64, 64), 'grey')
    # Five minutes interval
    sleep(interval_min * 60)
    icon.icon = image = Image.new('RGB', (64, 64), 'green')
    maincode()


# Icon systray code
def create_image(width, height, color1, color2):
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image


icon = pystray.Icon('test name', icon=create_image(64, 64, 'green', 'grey'))
icon.run_detached()
sleep(5)

# Main Loop everything is being triggered from here!!! Never ends!!! since flag will always be true
flag = True
while flag is True:
    b = datetime.today()
    c = datetime.today() + timedelta(minutes=interval_min)
    print('The scraping will start at: ' + c.strftime("%d/%m/%Y %H:%M"))
    print('If you wish to change the time interval, go to the top and change the variable "interval_min" ')
    loop()
