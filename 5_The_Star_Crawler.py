import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Click the "Load More" button for scraping more news
def extendPage():
    while True:
        try:
            try:
                # Just to locate to the Load More button to be clicked
                load_more = driver.find_element_by_class_name('quicklinks')
                actions = ActionChains(driver)
                actions.move_to_element(load_more).perform()
            except NoSuchElementException:
                print('Skip')
                break

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "loadMorestories"))).click()
            break
        except ElementClickInterceptedException as a:
            print("Try again")
            pass
        except TimeoutException as b:
            print("Try again")
            pass
        except NoSuchElementException as c:
            print("Try again")
            pass


# Iterate the given list to text or url
def toList(given_list, condition):
    convert = []
    for i in given_list:
        if condition == 'link':
            convert.append(i.get_attribute('href'))
        else:
            convert.append(i.text)
    non_empty_ele = [j for j in convert if j]
    return non_empty_ele


# activate chrome driver
driver = webdriver.Chrome()
driver.get('https://www.thestar.com.my/')

# Get all the types of news
types = driver.find_elements_by_xpath(".//li[@class = 'dropdown']")
all_type = toList(types, 'text')
all_type.remove('Videos')
all_type.remove('Photos')
print(all_type)

links_list = []
news_list = []

# Browser through every type of webpage, scrape the links and store into a list
for element in all_type:
    xpath = f"//a[contains(text(), '{element}')]"
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath))).click()
    print(xpath)
    extendPage()

    travel1 = driver.find_elements_by_xpath(".//main//div[5]//h2/a")
    if element.lower() == 'starplus' or element.lower() == 'business' or element.lower() == 'lifestyle' or element.lower() == 'opinion':
        travel2 = driver.find_elements_by_xpath(".//main//div[6]//h2/a")
    else:
        travel2 = driver.find_elements_by_xpath(".//main//div[6]/div/div/div[2]//h2/a")

    links_list1 = toList(travel1, 'link')
    links_list2 = toList(travel2, 'link')
    links_list = links_list + links_list1 + links_list2
    print(len(links_list))
driver.close()

# Removes duplicates from list
filtered_links = []
[filtered_links.append(x) for x in links_list if x not in filtered_links]
print(f'No. of non-duplicated link: {len(filtered_links)}')

# Considering the Food category contains some recipes which will lead to another web page.
# Therefore I decided to remove non The Star link here
for i, ele in enumerate(filtered_links):
    if not ele.startswith('https://www.thestar.com.my/'):
        del filtered_links[i]
print(f'No. of non-TheStar link: {len(filtered_links)}')

# Browse through each url and crawl the news content
for link in filtered_links:
    driver = webdriver.Chrome()
    url = f"{link}"
    print(link)
    driver.get(url)

    try:
        title = driver.find_element_by_tag_name('h1').text
    except NoSuchElementException:
        driver.close()
        continue

    try:
        author = driver.find_elements_by_xpath(".//div[@class = 'credit__authors']/a")
        author = toList(author, 'text')
        author = re.sub(",", " ", '，'.join(author))
    except NoSuchElementException:
        author = ''
        pass

    try:
        date = driver.find_element_by_xpath(".//p[@class = 'date']").text
    except NoSuchElementException:
        date = ''
        pass

    try:
        timestamp = driver.find_element_by_xpath(".//time[@class = 'timestamp']").text
    except NoSuchElementException:
        timestamp = ''
        pass

    # Extract all the text of the news content
    parent = driver.find_element_by_id('story-body')
    content = list(parent.text.split('\n'))

    # The following 4 statements are to extract all irrelevant content such as chart and image caption
    chart_text = parent.find_elements_by_xpath(".//div[contains(@class, 'flourish')]")
    inline_text = parent.find_elements_by_xpath(".//span[contains(@class, 'inline-caption')]")
    caption_text = parent.find_elements_by_xpath(".//p[contains(@class, 'caption')]")
    extra_text = chart_text + inline_text + caption_text

    full_content = []
    for child_ele in extra_text:
        full_content.append(child_ele.text)
    full_content = list(set(full_content))

    # Filter out irrelevant content
    for index, i in enumerate(content):
        for j in full_content:
            if i == j:
                content[index] = ''

    # Remove the enter and empty field from the extracted news content
    real_content = ''
    for element in content:
        real_content += element

    # Determine the type of the news by using the url
    for category in all_type:
        str = f"https://www.thestar.com.my/{category.lower()}"
        result = re.search(str, link)
        if result is not None:
            break

    print(date)
    print(timestamp)
    print(title)
    print(category)
    print(author)
    print(real_content)

    news_items = {'Date': date, 'Time': timestamp, 'Type': category, 'Author': author, 'Title': title,
                  'Content': real_content}
    news_list.append(news_items)
    print(len(news_list))
    driver.close()
    time.sleep(1)

# Store the crawled data into data frame
current = pd.DataFrame(news_list)
print(current.head())
print("Shape    : ", current.shape)

# Read older csv file
before = pd.read_csv('News.csv')
print(before.head())
print("Shape    : ", before.shape)

# Concatenate current and older data
data = pd.concat([before, current])
# Drop duplicates between previous and current data
data.drop_duplicates(inplace = True, subset = ['Content'])
# Store the data back to the News csv file
data.to_csv('News.csv', index=False)
data.head()

print("Rows     : ", data.shape[0])
print("Columns  : ", data.shape[1])
print("Shape    : ", data.shape)
print("Features : ", data.columns.tolist())
