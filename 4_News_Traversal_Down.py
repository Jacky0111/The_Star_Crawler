import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get('https://www.thestar.com.my/')

star_plus = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Sport')]"))).click()
load_more = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Load More"))).click()


def to_list(x):
    convert = []
    for i in x:
        # convert.append(i.get_attribute('href'))
        convert.append(i.text)
    return convert


travel1 = driver.find_elements_by_xpath(".//main//div[5]//h2/a")
travel2 = driver.find_elements_by_xpath(".//main//div[6]/div/div/div[2]//h2/a")

links_list1 = to_list(travel1)
links_list2 = to_list(travel2)
links_list = links_list1 + links_list2
print(len(links_list1))
print(len(links_list2))
print(links_list)
print(links_list1)
print(links_list2)
print(len(links_list))

for index in range(22, 28):
    # xpath = f".//h/a[@href = '{links_list[index]}']"
    to_travel = driver.find_element_by_link_text(links_list[index])
    driver.execute_script("arguments[0].click();", to_travel)
    print(links_list[index])
    print(index)
    driver.back()
    load_more = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Load More"))).click()

driver.close()
