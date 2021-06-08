import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get('https://www.thestar.com.my/')

star_plus = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'StarPlus')]"))).click()
news = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//div[@class = 'content']/h2/a"))).click()

title = driver.find_element_by_tag_name('h1').text
author = driver.find_element_by_xpath(".//div[@class = 'credit__authors']/a").text
date = driver.find_element_by_xpath(".//p[@class = 'date']").text
time = driver.find_element_by_xpath(".//time[@class = 'timestamp']").text

parent = driver.find_element_by_id('story-body')
content = list(parent.text.split('\n'))
child = parent.find_elements_by_xpath(".//div[contains(@class, 'flourish')]")
full_content = []
for child_ele in child:
    full_content.append(child_ele.text)

for index, i in enumerate(content):
    for j in full_content:
        if i == j:
            content[index] = ''

real_content = ''
for element in content:
    real_content += element

print(title)
print(author)
print(date)
print(time)
print(real_content)

news_list = []
news_items = {'Date': date, 'Time': time, 'Title': title, 'Author': author, 'Content': real_content}
news_list.append(news_items)

df = pd.DataFrame(news_list)
df.to_csv('News.csv', index=False)
print(df.head(10))

driver.close()
