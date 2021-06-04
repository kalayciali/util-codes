from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
import sys
import time



class FormSubmit():
    driver = None

    def __init__(self, your_phone, agency, state, lga, agent_phone, transaction, txntype):
        self.your_phone = your_phone
        self.agency = agency
        self.state = state
        self.lga = lga
        self.agent_phone = agent_phone
        self.transaction = transaction
        self.txntype = txntype

        self.phone_num_xpath = '//input[contains(@class,"phonenumber form-control")]'

        self.agency_xpath = f'//*[@id="agency"]/option[contains(text(),"{self.agency}")]'
        self.state_xpath = f'//*[@id="state"]/option[contains(text(),"{self.state}")]'

        self.lga_xpath = f'//*[@id="lga"]/option[contains(text(),"{self.lga}")]'

        self.agent_phone_xpath = '(//input[contains(@class,"phonenumber form-control")])[2]'
        self.customer_phone_xpath = '(//input[contains(@class,"phonenumber form-control")])[3]'
        self.transaction_xpath = '//input[@ng-model="canvasser.amount"]'

        self.txntype_xpath = f'//select[@name="txntype"]/option[contains(text(),"{self.txntype}")]'
        self.next_btn = '(//button[@type="submit"])[1]'
        self.submit = '(//button[@type="submit"])[2]'
        self.full_submit = '//*[@id="confirmcanvassbox"]/div/div[@class="modal-content"]/div[@class="modal-footer"]/button[contains(text(),"Submit")]'

    @staticmethod
    def driverOpen(url):
        opts = Options()
        opts.add_argument("user-agent = Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36")
        opts.add_argument("--headless")
        FormSubmit.driver = webdriver.Chrome('./chromedriver', options=opts)
        FormSubmit.driver.get(url)


    def read_file(self, filename):
        """
        Read the text file with the given filename;
        return a list of the lines of text in the file.
        """
        try:
            with open(filename, 'r') as f:
                return f.read()
        except IOError:
            sys.exit()

    def clean_file(self, doc):
        doc = doc.replace('\n', '\t')
        numbers = doc.split('\t')
        for number in numbers:
            number = '0' + number
            yield number

    def submit_form(self, driver, num):
        try:
            phone_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.phone_num_xpath))
            )
            phone_field.click()
            phone_field.send_keys(self.your_phone)
            time.sleep(.1)

            driver.find_element_by_xpath(self.agency_xpath).click()
            time.sleep(.1)
            driver.find_element_by_xpath(self.state_xpath).click()
            time.sleep(.1)
            driver.find_element_by_xpath(self.lga_xpath).click()
            time.sleep(.1)
            driver.find_element_by_xpath(self.next_btn).click()
            time.sleep(.1)

            agent_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.agent_phone_xpath))
            )
            agent_field.click()
            agent_field.send_keys(self.agent_phone)
            time.sleep(.1)


            customer_field = driver.find_element_by_xpath(self.customer_phone_xpath)
            customer_field.click()
            customer_field.send_keys(num)
            time.sleep(.1)

            txn_field = driver.find_element_by_xpath(self.transaction_xpath)
            txn_field.click()
            txn_field.send_keys(self.transaction)
            time.sleep(.1)

            driver.find_element_by_xpath(self.txntype_xpath).click()
            time.sleep(.1)

            driver.find_element_by_xpath(self.submit).click()

            time.sleep(.5)
            full_submit = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.full_submit)))
            full_submit.click()
            time.sleep(.5)

        except (NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException) as e:
            url = 'https://www.momoforms.com.ng/30dayscanvasser'
            driver.get(url)
            return num

    def run(self, url, filename):
        FormSubmit.driverOpen(url)
        doc = self.read_file(filename)
        not_accepted = ''
        try:
            i = 0
            for number in self.clean_file(doc):
                i += 1
                num = self.submit_form(FormSubmit.driver, number)
                if num is not None:
                    print(num)
                    not_accepted += f'{num}\t'
                    if i == 10:
                        i == 0
                        not_accepted += '\n'

        finally:
            print("finished or interrupted")
            with open('not_accepted.csv', 'w+') as f:
                f.write(not_accepted)

def main():
    if len(sys.argv) != 9:
        print("Usage: form_submit.py filename your_phone agency state lga agent_phone transaction txntype")
        sys.exit()
    else:
        url = 'https://www.momoforms.com.ng/30dayscanvasser'
        filename = sys.argv[1]
        your_phone = sys.argv[2]
        agency = sys.argv[3]
        state = sys.argv[4]
        lga = sys.argv[5]
        agent_phone = sys.argv[6]
        transaction = sys.argv[7]
        txntype = sys.argv[8]

        fs = FormSubmit(your_phone, agency, state, lga, agent_phone, transaction, txntype)
        fs.run(url, filename)

if __name__=="__main__":
    main()





