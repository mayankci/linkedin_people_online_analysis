# %%
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import  Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime, timedelta

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()

driver.get("https://www.linkedin.com/feed/")
WebDriverWait(driver,10).until(
    EC.element_to_be_clickable((By.ID,"username"))
).send_keys("")

WebDriverWait(driver,10).until(
    EC.element_to_be_clickable((By.ID,"password"))
).send_keys("")

WebDriverWait(driver,10).until(
    EC.element_to_be_clickable((By.CLASS_NAME,"btn__primary--large"))
).click()


from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pyautogui

for _ in range(1,7):
    pyautogui.hotkey("ctrl","-")
for _ in range(20):  
    pyautogui.press("pagedown")  
    time.sleep(2) 
time.sleep(5)  
soup = BeautifulSoup(driver.page_source, "html.parser")
post_elements = soup.find_all("div", {"data-id": True})

post_links = []
for post in post_elements:
    post_id = post["data-id"].split(":")[-1]
    post_url = f"https://www.linkedin.com/feed/update/urn:li:activity:{post_id}/"
    post_links.append(post_url)

print("post_links",len(post_links))
count=1
data = []
for post_url in post_links:  
    print(count)
    driver.get(post_url)
    time.sleep(5)  

    try:
        comments_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'comments on')]"))
        )
        driver.execute_script("arguments[0].click();", comments_btn)
        time.sleep(3)
    except:
        print(f"No comments button found for {post_url}")
        continue  

    for _ in range(5):  
        try:
            load_more_btn = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Load more comments')]"))
            )
            driver.execute_script("arguments[0].click();", load_more_btn)
            time.sleep(3)
        except:
            break  

    soup = BeautifulSoup(driver.page_source, "html.parser")
    comments = soup.find_all("span", class_="comments-comment-item__main-content")
    timestamps = soup.find_all("time", class_="comments-comment-item__timestamp")  

    for i in range(len(comments)):
        comment_text = comments[i].get_text(strip=True)
        comment_time_text = timestamps[i].get_text(strip=True) if i < len(timestamps) else "Unknown"
        
        current_time = datetime.now()
        
        try:
            if "h" in comment_time_text:
                hours_ago = int(''.join(filter(str.isdigit, comment_time_text)))  
                comment_time = current_time - timedelta(hours=hours_ago)
                data.append([post_url, comment_text, comment_time]) 
            else:
                continue  
        except ValueError:
            continue  

        data.append([post_url, comment_text, comment_time])
    
    count+=1


df = pd.DataFrame(data, columns=["Post URL", "Comment", "Time Posted"])
df = df.drop_duplicates(subset=['Comment'])
df['Time Posted'] = pd.to_datetime(df['Time Posted'], errors='coerce')
df['time'] = df['Time Posted'].dt.time  
df['Formatted Time'] = df['Time Posted'].dt.strftime('%I %p')
df



# %%
df.groupby(['Formatted Time'])['Comment'].count()


