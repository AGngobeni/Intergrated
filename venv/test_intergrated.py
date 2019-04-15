import openpyxl
import pytest
import json
import requests


from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture()
def environment_setup():
    global driver
    path = "C:\\Users\\amukelani.ngobeni\\Documents\\Softwares\\Python\\geckodriver.exe"
    driver = Firefox(executable_path=path);
    driver.get('https://pp.video-play.vodacom.co.za/#!/register');
    driver.maximize_window()
    yield
    driver.close()

work_books = openpyxl.load_workbook("C:\\Users\\amukelani.ngobeni\\Documents\\Self-learning\\TestData.xlsx")
activeSheet = work_books["Sheet1"]
name = activeSheet['A2'].value
surname = activeSheet['B2'].value
contact = activeSheet['C2'].value
password = activeSheet['D2'].value
confirm = activeSheet['E2'].value

r = requests.post("https://pp.video-play.vodacom.co.za/AGL/1.0/A/ENG/PCTV/VIDEOPLAY_EMEA_ZA/USER/LOGIN", data={'username': name, 'password': password})
jData = (r.text[:300])
pjson= json.loads(jData)
print(pjson['resultCode'])

def run_first():
    return pjson['resultCode']

def validate():
    return "OK"

def test_register(environment_setup):
    driver.implicitly_wait(300) # seconds
    myDynamicElement = driver.find_element_by_link_text("Got it!")
    myDynamicElement.click()
    driver.find_element_by_id("betaField").send_keys("!060v0d@c0m_o82")
    driver.implicitly_wait(100) # seconds
    myDynamicElement = driver.find_element_by_css_selector(".btn.btn-ctl.button_login")
    myDynamicElement.click()
    driver.find_element_by_name("first_name").send_keys(name)
    driver.find_element_by_name("surname").send_keys(surname)
    driver.find_element_by_name("phoneNumber").send_keys(contact)
    driver.find_element_by_name("userPassword").send_keys(password)
    driver.find_element_by_name("userPasswordConfirm").send_keys(confirm)
    driver.find_element_by_id("terms-and-condition").click()
    driver.implicitly_wait(100)
    wait = WebDriverWait(driver, 10)
    myDynamicElement = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.btn.btn-ctl.btn-block.btn-registration.submit")))
    myDynamicElement.click()
    if(run_first()=="KO"):
        assert validate()== pjson

