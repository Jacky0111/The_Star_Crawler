from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Visit through every types of news pages
driver = webdriver.Chrome()
driver.get('https://www.thestar.com.my/')

typ = driver.find_elements_by_xpath(".//li[@class = 'dropdown']")

types = []
for i in typ:
    types.append(i.text)

print(types)

for ele in types:
    xpath = f"//a[contains(text(), '{ele}')]"
    if ele.lower() != 'videos' and ele.lower() != 'photos':
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))).click()
        print(xpath)

driver.close()
