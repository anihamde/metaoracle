from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from markdownify import markdownify as md
import os

driver = webdriver.Chrome()

driver.get("https://pythnetwork.medium.com/")

# scroll to bottom
SCROLL_PAUSE_TIME = 5.0
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


article_number = 1
post_links = []

while True:
    try:
        expl = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[3]/div[2]/div/main/div/div[2]/div/div/article[{article_number}]/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div[1]/a')
        post_links.append( expl.get_attribute("href") )
        article_number += 1
    except:
        print(f"Got {article_number-1} article links!")
        break

driver.close()

# write to markdown
for i in range(len(post_links)):
    for try_number in range(3):
        driver = webdriver.Chrome()
        driver.get(post_links[i])

        time.sleep(3.0)

        expl = driver.find_element(By.CSS_SELECTOR, '.cb')
        try:
            content = md(expl.get_attribute("innerHTML"))
            break
        except:
            driver.close()

    if not os.path.exists("training/blog"):
        os.makedirs("training/blog")
    with open(f"training/blog/article_{i}.md", 'w+') as f:
        f.write(content)
    
    driver.close()

