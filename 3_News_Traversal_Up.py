import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get('https://www.thestar.com.my/')


def extend_page():
    while True:
        try:
            load_more = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "loadMorestories"))).click()
            break
        except ElementClickInterceptedException:
            print("Try again")


def to_list(x):
    convert = []
    for i in x:
        # convert.append(i.get_attribute('href'))
        convert.append(i.text)
    no_empty_ele = [i for i in convert if i]
    return no_empty_ele


star_plus = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Sport')]"))).click()
extend_page()

travel1 = driver.find_elements_by_xpath(".//main//div[5]//h2/a")
# travel2 = driver.find_elements_by_xpath(".//main//div[6]/div/div[1]//h2/a")
travel2 = driver.find_elements_by_xpath(".//main//div[6]/div/div/div[2]//h2/a")

links_list1 = to_list(travel1)
links_list2 = to_list(travel2)
links_list = links_list1 + links_list2

print(links_list)
print(len(links_list))

driver.refresh()

for index in range(len(links_list)):
    # for index, element in enumerate(links_list):
    #     if index <= 15:
    #         xpath = f".//main//div[5]//h2/a[@href = '{element}']"
    #     else:
    #         xpath = f".//main//div[6]/div/div/div[2]//h2/a[@href = '{element}']"
    try:
        to_travel = driver.find_element_by_link_text(links_list[index])
        driver.execute_script("arguments[0].click();", to_travel)
        print(links_list[index])
        print(index + 1)
        time.sleep(5)
        driver.back()

        extend_page()
    except NoSuchElementException:
        print(index + 1)
        continue
    except TimeoutException:
        print(index + 1)
        continue
    # finally:
    time.sleep(5)

driver.close()
