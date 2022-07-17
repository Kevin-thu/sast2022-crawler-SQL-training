from selenium.webdriver.remote.webdriver import WebDriver as wd
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC
import selenium
import json
from bs4 import BeautifulSoup as BS

class WebVPN:
    def __init__(self, opt: dict, headless=False):
        self.root_handle = None
        self.driver: wd = None
        self.userid = opt["username"]
        self.passwd = opt["password"]
        self.headless = headless

    def login_webvpn(self):
        """
        Log in to WebVPN with the account specified in `self.userid` and `self.passwd`

        :return:
        """
        d = self.driver
        if d is not None:
            d.close()
        d = selenium.webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        d.get("https://webvpn.tsinghua.edu.cn/login")
        username = d.find_elements(By.XPATH,
                                   '//div[@class="login-form-item"]//input'
                                   )[0]
        password = d.find_elements(By.XPATH,
                                   '//div[@class="login-form-item password-field" and not(@id="captcha-wrap")]//input'
                                   )[0]
        username.send_keys(str(self.userid))
        password.send_keys(self.passwd)
        d.find_element(By.ID, "login").click()
        self.root_handle = d.current_window_handle
        self.driver = d
        return d

    def access(self, url_input):
        """
        Jump to the target URL in WebVPN

        :param url_input: target URL
        :return:
        """
        d = self.driver
        url = By.ID, "quick-access-input"
        btn = By.ID, "go"
        wdw(d, 5).until(EC.visibility_of_element_located(url))
        actions = AC(d)
        actions.move_to_element(d.find_element(*url))
        actions.click()
        actions.\
            key_down(Keys.CONTROL).\
            send_keys("A").\
            key_up(Keys.CONTROL).\
            send_keys(Keys.DELETE).\
            perform()

        d.find_element(*url)
        d.find_element(*url).send_keys(url_input)
        d.find_element(*btn).click()

    def switch_another(self):
        """
        If there are only 2 windows handles, switch to the other one

        :return:
        """
        d = self.driver
        assert len(d.window_handles) == 2
        wdw(d, 5).until(EC.number_of_windows_to_be(2))
        for window_handle in d.window_handles:
            if window_handle != d.current_window_handle:
                d.switch_to.window(window_handle)
                return

    def to_root(self):
        """
        Switch to the home page of WebVPN

        :return:
        """
        self.driver.switch_to.window(self.root_handle)

    def close_all(self):
        """
        Close all window handles

        :return:
        """
        while True:
            try:
                l = len(self.driver.window_handles)
                if l == 0:
                    break
            except selenium.common.exceptions.InvalidSessionIdException:
                return
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.driver.close()

    def login_info(self):
        """
        TODO: After successfully logged into WebVPN, login to info.tsinghua.edu.cn

        :return:
        """

        # Hint: - Use `access` method to jump to info.tsinghua.edu.cn
        #       - Use `switch_another` method to change the window handle
        #       - Wait until the elements are ready, then preform your actions
        #       - Before return, make sure that you have logged in successfully
        d = self.driver
        self.access("http://info.tsinghua.edu.cn/index.jsp")
        self.switch_another()
        wdw(d, 5).until(EC.visibility_of_element_located((By.ID, "userName")))
        username = d.find_element(By.ID, "userName")
        username.send_keys(self.userid)
        password = d.find_element(By.NAME, "password")
        password.send_keys(self.passwd)
        enter_key = d.find_element(By.XPATH, "//td/table/tbody/tr/td/input[@type='image']")
        enter_key.click()

    def get_grades(self):
        """
        TODO: Get and calculate the GPA for each semester.

        Example return / print:
            2020-秋: *.**
            2021-春: *.**
            2021-夏: *.**
            2021-秋: *.**
            2022-春: *.**

        :return:
        """

        # Hint: - You can directly switch into
        #         `zhjw.cic.tsinghua.edu.cn/cj.cjCjbAll.do?m=bks_cjdcx&cjdlx=zw`
        #         after logged in
        #       - You can use Beautiful Soup to parse the HTML content or use
        #         XPath directly to get the contents
        #       - You can use `element.get_attribute("innerHTML")` to get its
        #         HTML code
        d = self.driver
        url = By.XPATH, "//ul[@id='menu']/li/a[@href='https://webvpn.tsinghua.edu.cn/http/77726476706e69737468656265737421eaff4b8b69336153301c9aa596522b20bc86e6e559a9b290/cj.cjCjbAll.do?m=bks_yxkccj']"
        wdw(d, 5).until(EC.visibility_of_element_located(url))
        score_page = d.find_element(*url)
        score_page.click()
        d.switch_to.window(d.window_handles[2]) # 切换到当前点击进入的窗口
        report = d.find_elements(By.TAG_NAME, "table")[2]
        report = report.get_attribute("innerHTML")
        soup = BS(report, features="html.parser")
        courses = soup.find_all('tr')
        courses.pop(0)
        courses.pop()
        courses.pop()
        for year in range(2018, 2025):
            for term in range(1, 3):
                gpa, credit_sum = 0, 0
                for course in courses:
                    divs = course.find_all('div')
                    if divs[7].text == f'{year}-{year+1}-{term}':
                        credit = int(divs[2].text.strip())
                        grade = divs[5].text.strip()
                        if grade != 'N/A':
                            credit_sum += credit
                            gpa += float(grade) * credit
                if credit_sum != 0:
                    gpa /= credit_sum
                    if term == 1:
                        print(f"{year}-秋：{gpa:.2f}")
                    else:
                        print(f"{year+1}-春：{gpa:.2f}")

if __name__ == "__main__":
    # TODO: Write your own query process
    with open("./settings.json", 'r') as f:
        setting = json.load(f)
    web = WebVPN(setting)
    web.login_webvpn()
    web.login_info()
    web.get_grades()
    web.close_all()