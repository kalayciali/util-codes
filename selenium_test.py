from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import unittest


chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome('./chromedriver', options=chrome_options)
driver.get('http://pythonscraping.com/pages/files/form.html')

firstname = driver.find_element_by_name('firstname')
lastname = driver.find_element_by_name('lastname')
submitButton = driver.find_element_by_id('submit')

# Method1
# firstname.send_keys('Ali')
# lastname.send_keys('Kalayci')
# submitButton.click()

# Method2
actions = ActionChains(driver).click(firstname).send_keys('Ali').click(lastname).send_keys('Kalayci').send_keys(Keys.RETURN)
actions.perform()

print(driver.find_element_by_tag_name('body').text)

# drag and drop thing
class TestDragAndDrop(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Chrome('./chromedriver', options=chrome_options)
        url = 'http://pythonscraping.com/pages/javascript/draggableDemo.html'
        self.driver.get(url)

    def tearDown(self):
        print('FİNİSHED')

    def test_drag(self):
        elem = self.driver.find_element_by_id('draggable')
        target = self.driver.find_element_by_id('div2')
        actions = ActionChains(self.driver)
        actions.drag_and_drop(elem, target).perform()
        driver.get_screenshot_as_file('tmp/pythonscraping.png')
        self.assertEqual('You are definitely not a bot!',
                         self.driver.find_element_by_id('message').text)

if __name__ == '__main__':
    unittest.main()

driver.close()
