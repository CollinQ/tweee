import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import openpyxl

options = Options()
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("window_size=1280,800")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-save-password-bubble")

def save_to_excel(data, filename):
    if os.path.exists(filename):
        df_existing = pd.read_excel(filename, engine='openpyxl')
        df_new = pd.DataFrame(data, columns=["Tweets"])
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_excel(filename, index=False, engine='openpyxl')
    else:
        df = pd.DataFrame(data, columns=["Tweets"])
        df.to_excel(filename, index=False, engine='openpyxl')



driver = webdriver.Chrome(options=options)
driver.get("https://accounts.google.com/v3/signin/identifier?hl=en_GB&ifkv=AXo7B7VGP4Y_gNfwPri72zV40Ii9kmgYbvLRXoOhOeBNkeBYcMPcPOX_Aolo1vK16FetaA4URMIfUA&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-1140670556%3A1692882589574310")
#email: 
email = 'tw3333ts@gmail.com'
#password:
password = 'twee1234'

#LOGIN
driver.find_element(By.XPATH,'//*[@id="identifierId"]').send_keys(email)
time.sleep(3)
driver.find_element(By.XPATH,'//*[@id="identifierNext"]/div/button/span').click()
time.sleep(5)
driver.find_element(By.XPATH,'//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
driver.find_element(By.XPATH,'//*[@id="passwordNext"]/div/button/span').click()
time.sleep(5)

#GO TO TWITTER
driver.get("https://twitter.com/")
time.sleep(10)
# current_window = driver.current_window_handle
# con = driver.find_element(By.XPATH,'/html/body/div/div/div[2]').click()
# wait = WebDriverWait(driver, 10)
# wait.until(EC.number_of_windows_to_be(2))
#
# for window_handle in driver.window_handles:
#     if window_handle != current_window:
#         driver.switch_to.window(window_handle)
#         break
hashtags = ['wow']

unique_texts = []
seen_texts = set()


for hashtag in hashtags:
    driver.get("https://twitter.com/explore")

    time.sleep(5)
    search = driver.find_element(By.XPATH,
                                 '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[1]/div[2]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input')
    search.send_keys(hashtag+" lang:en") #for language filtere, you can remove
    search.send_keys(Keys.ENTER)

    time.sleep(5)
    #
    # driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a/div/div/span').click()
    # time.sleep(5)

    actions = ActionChains(driver)

    previous_num_unique = 0  # Keep track of the number of unique tweets in the previous iteration

    while True:
        # Scroll 10 times
        for _ in range(5):
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(3)  # Giving the page some time to load new content

        # Fetch tweet data
        t_data = driver.find_elements(By.XPATH,
                                      '//*[@id="id__4at5iweovb9"]')
        
        print(t_data)

        # Store in set
        for i in t_data:
            try:
                tweet_text = i.text
                if tweet_text not in seen_texts:
                    unique_texts.append(tweet_text)
                    seen_texts.add(tweet_text)
            except StaleElementReferenceException:
                # If a stale element exception occurs, break out of the loop
                # and re-fetch the tweets
                break

        print(unique_texts)

        if len(unique_texts) == previous_num_unique:
            print("breaking")
            break

        previous_num_unique = len(unique_texts)

        for text in unique_texts:
            print(text)

        print(len(unique_texts))
        # Save the tweets to the Excel file after processing each hashtag
        save_to_excel(list(unique_texts), "tweets.xlsx")
# Print the unique texts
for text in unique_texts:
    print(text)
