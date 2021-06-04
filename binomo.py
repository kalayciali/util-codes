from collections import namedtuple
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import unittest
import random
import time




Trade = namedtuple('Trade', ['currency', 'given', 'possib_rev', 'start_time', 'end_time', 'start_val', 'end_val', 'up_down'])
Bet = namedtuple('Bet', ['bet_val', 'bet_time', 'bet_finish', 'up_down'])


class TestSite(unittest.TestCase):

    driver = None
    money = 0

    LOGIN_PAN_XP = '//*[@id="qa_trading_profileDropdownButton"]/ng-component[1]'
    LOGIN_BUT_XP = "//button[text()='Oturum aç']"
    SIGNIN_BUT_XP = "//button[text()='Üye olun']"
    GOOGLE_XP = "//img[@src='/assets/binomo/images/auth/gp.svg']"
    FACEBOOK_XP = "//button[@type='button']"
    EMAIL_XP = "//vui-input-text[@class='hydrated']//input[1]"
    PASSWORD_XP = "//input[@type='password']"
    AFFIRM_XP = "//vui-checkbox[@class='hydrated']//label[1]"
    SUBMIT_XP = '//*[@id="qa_auth_SignIn"]/form'

    ACCOUNT_XP = "//vui-badge[@class='hydrated']//vui-avatar[1]"
    EXIT_XP = '//*[@id="qa_trading_singOutButton"]'

    MONEY_XP = '//*[@id="qa_trading_balance"]'
    BET_VAL_XP = '//*[@id="amount-counter"]'
    BET_TIME_XP = '//*[@id="qa_trading_dealTimeInput"]'
    BET_UP_XP = '//*[@id="qa_trading_dealUpButton"]'
    BET_DOWN_XP = '//*[@id="qa_trading_dealDownButton"]'
    HISTORY_BUT_XP = '//*[@id="qa_trading_abilityDashboard"]/div/div/div[2]'
    HISTORY_ITEMS_XP = '//*[@id="qa_trading_abilityDashboard"]/div/vui-sidebar/div/div/div[2]/app-virtual-scroll/app-scroll/div/div/div[1]/ng-component/ng-component/div/option-item/div.active'
    UP_DOWN_XP = '//*[@id="qa_trading_abilityDashboard"]/div/vui-sidebar/div/div/div[2]/app-virtual-scroll/app-scroll/div/div/div[1]/ng-component/ng-component/div/option-item/div.active/div[2]/div[1]/div/vui-icon'
    CURRENCY_XP = '//*[@id="qa_trading_abilityDashboard"]/div/vui-sidebar/div/div/div[2]/app-virtual-scroll/app-scroll/div/div/div[1]/ng-component/ng-component/option-detail/div/div[1]/div[2]'
    START_TIME_XP = '//*[@id="qa_trading_abilityDashboard"]/div/vui-sidebar/div/div/div[2]/app-virtual-scroll/app-scroll/div/div/div[1]/ng-component/ng-component/option-detail/div/div[3]/div[1]/div/div/p'
    END_TIME_XP = '//*[@id="qa_trading_abilityDashboard"]/div/vui-sidebar/div/div/div[2]/app-virtual-scroll/app-scroll/div/div/div[1]/ng-component/ng-component/option-detail/div/div[3]/div[2]/div/div/p'
    GIVEN_XP = '//*[@id="qa_trading_abilityDashboard"]/div/vui-sidebar/div/div/div[2]/app-virtual-scroll/app-scroll/div/div/div[1]/ng-component/ng-component/option-detail/div/div[3]/div[1]/p[1]'
    REVENUE_XP = '//*[@id="qa_trading_abilityDashboard"]/div/vui-sidebar/div/div/div[2]/app-virtual-scroll/app-scroll/div/div/div[1]/ng-component/ng-component/option-detail/div/div[3]/div[2]/p[1]'
    START_VAL_XP = '//*[@id="qa_trading_abilityDashboard"]/div/vui-sidebar/div/div/div[2]/app-virtual-scroll/app-scroll/div/div/div[1]/ng-component/ng-component/option-detail/div/div[3]/div[1]/div/p[2]'
    END_VAL_XP = '//*[@id="qa_trading_abilityDashboard"]/div/vui-sidebar/div/div/div[2]/app-virtual-scroll/app-scroll/div/div/div[1]/ng-component/ng-component/option-detail/div/div[3]/div[2]/div/p[2]'
    BACK_XP = '//*[@id="qa_trading_abilityDashboard"]/div/vui-sidebar/div/div/div[1]/div/app-breadcrumbs/vui-breadcrumbs/ul/li[1]'

    @classmethod
    def setUpClass(cls):
        opts = Options()
        opts.add_argument("user-agent = Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36")
        opts.add_experimental_option("excludeSwitches", ['enable-automation']);

        cls.driver = webdriver.Chrome('./chromedriver', options=opts)
        cls.driver.get('https://binomo.com/tr')
        time.sleep(4)

    @classmethod
    def tearDownClass(cls):
        print('finished test')
        cls.driver.close()

    def moneyClear(self, string):
        string = string.replace('.', '')
        try:
            i = string.index(',')
            money = int(money[:i])
            return money
        except:
            money = int(money)
            return money

    def checkHistoryBetEqual(self, trades, bets):
        j = len(trades) -1
        for i in range(len(trades)):
            bet = bets[i]
            trade = trades[j]
            if bet.bet_val != trade.given:
                print(f'Bet: {bet.bet_val}')
                print(f'Trade: {trade.given}')
                print('Bet and History values are not equal')
                return False
            if bet.bet_time != trade.start_time:
                print(f'Bet: {bet.bet_time}')
                print(f'Trade: {trade.start_time}')
                print('Bet and History times are not equal')
                return False
            if bet.up_down != trade.up_down:
                print(f'Bet: {bet.up_down}')
                print(f'Trade: {trade.up_down}')
                print('Bet and History up down are not equal')
                return False
            if bet.bet_finish != trade.end_time:
                print(f'Bet: {bet.bet_finish}')
                print(f'Trade: {trade.end_time}')
                print('Bet and History end times are not equal')
                return False
            j -= 1
        return True



    def makeBet(self, driver):

        priceTags = '//*[@id="amount-counter"]/div[1]/vui-popover/div/app-scroll/div/div/div/vui-option'
        timeTags = '//*[@id="qa_trading_dealTimeInput"]/div[1]/vui-popover/div/app-scroll/div/div/div/div/vui-option'
        bet_val_el = driver.find_element_by_xpath(self.BET_VAL_XP)
        bet_time_el = driver.find_element_by_xpath(self.BET_TIME_XP)
        bet_up_el = driver.find_element_by_xpath(self.BET_UP_XP)
        bet_down_el = driver.find_element_by_xpath(self.BET_DOWN_XP)

        bet_val_el.click()
        time.sleep(.5)
        price = random.choice(driver.find_elements_by_xpath(priceTags))
        bet_val = price.find_element_by_tag('span').get_text()[1:]
        bet_val = self.moneyClear(bet_val)
        price.click()

        bet_time_el.click()
        time.sleep(.5)
        time = random.choice(driver.find_elements_by_xpath(timeTags))
        bet_finish = time.find_element_by_tag('span').get_text() + ':00'
        time.click()

        if random.uniform(0, 1) < 0.5:
            now = datetime.now().strftime("%H:%M:%S")
            bet_up_el.click()
            time.sleep(.5)
            return Bet(bet_val, now, bet_finish, 'up')
        else:
            now = datetime.now().strftime("%H:%M:%S")
            bet_down_el.click()
            time.sleep(.5)
            return Bet(bet_val, now, bet_finish, 'down')

    def getHistory(self, driver):
        trades = []

        history_button = driver.find_element_by_xpath(self.HISTORY_BUT_XP)
        history_button.click()
        last_trades = driver.find_elements_by_xpath(self.HISTORY_ITEMS_XP)
        up_down_list = driver.find_elements_by_xpath(self.UP_DOWN_XP)

        for i, trade in enumerate(last_trades):
            time.sleep(.5)
            trade.click()
            up_down = up_down_list[i]

            start_time = driver.find_element_by_xpath(self.START_TIME_XP).get_text()
            currency = driver.find_element_by_xpath(self.CURRENCY_XP).get_text()
            given = driver.find_element_by_xpath(self.GIVEN_XP).get_text()[1:]
            given = self.moneyClear(given)
            possib_rev = driver.find_element_by_xpath(self.REVENUE_XP).get_text()[1:]
            possib_rev = self.moneyClear(possib_rev)
            end_time = driver.find_element_by_xpath(self.END_TIME_XP).get_text()
            start_val = float(driver.find_element_by_xpath(self.START_VAL_XP).get_text())
            end_val = float(driver.find_element_by_xpath(self.END_VAL_XP).get_text())

            trades.append(Trade(currency, given, possib_rev, start_time,
                                      end_time, start_val, end_val, up_down))
            back = driver.find_element_by_xpath(self.BACK_XP)
            back.click()

        history_button.click()
        return trades

    def exitAfterLogin(self, driver):
        driver.find_element_by_xpath(self.ACCOUNT_XP).click()
        driver.find_element_by_xpath(self.EXIT_XP).click()
        driver.get('https://binomo.com')

    def loginNormal(self, driver):
        login_pan = driver.find_element_by_xpath(self.LOGIN_PAN_XP)
        login_pan.click()
        time.sleep(1)
        login_but = driver.find_element_by_xpath(self.LOGIN_BUT_XP)
        login_but.click()
        time.sleep(1)
        # facebook_but = driver.find_element_by_xpath(self.FACEBOOK_XP)
        # google_but = driver.find_element_by_xpath(self.GOOGLE_XP)
        email_field = driver.find_element_by_xpath(self.EMAIL_XP)
        email_field.click()
        time.sleep(2)
        email_field.send_keys('alikalayci@std.iyte.edu.tr')
        time.sleep(2)
        password_field = driver.find_element_by_xpath(self.PASSWORD_XP)
        password_field.click()
        time.sleep(2)
        password_field.send_keys('asd-123ASD')
        time.sleep(3)
        driver.find_element_by_xpath(self.SUBMIT_XP).submit()
        time.sleep(4)

    def test_Login(self):
        driver = TestSite.driver
        self.loginNormal(driver)
        expected_url = "https://binomo.com/trading"
        self.assertEqual(driver.current_url(), expected_url)
        self.exitAfterLogin(driver)

    def test_Trade(self):
        driver = TestSite.driver
        self.loginNormal(driver)

        money = driver.find_element_by_xpath(self.MONEY_XP).get_text()[1:]
        self.money = self.moneyClear(money)

        BET_NUMBER = 3
        bets = []
        for i in range(BET_NUMBER):
            bets.append(self.makeBet(driver))
        trades = self.getHistory(driver)
        self.assertTrue(self.checkHistoryBetEqual(trades, bets))

        while True:
            lastTrade = self.history[-1]
            now = datetime.now().strftime("%H:%M:%S")
            if lastTrade.end_time < now:
                continue

            old_money = self.money
            money = driver.find_element_by_xpath(self.MONEY_XP).get_text()[1:]
            self.money = self.moneyClear(money)

            if lastTrade.up_down == 'up':
                self.assertTrue(lastTrade.end_val > lastTrade.start_val)
                self.assertEqual(self.money, old_money + lastTrade.pos_rev)
            else:
                self.assertTrue(lastTrade.end_val < lastTrade.start_val)
                self.assertEqual(self.money, old_money - lastTrade.pos_rev)
            try:
                lastTrade.pop()
            except IndexError as e:
                break

if __name__ == "__main__":
    unittest.main()
