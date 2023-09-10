from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import warnings
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

warnings.simplefilter("ignore")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
chrome_options.add_argument("--mute-audio")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument("--lang=en-US")

proxies = [
    "IP:PORT","IP:PORT","IP:PORT"
    ]

proxyrotator = 0

with open("account.txt", "r") as f:
    account = f.read()

posts = int(input("How many posts should be generated for this account: "+account.split(":")[0]+"\n"))
postbreached = input("What should the post look like?\n")
while True:
    if not len(postbreached) < 5:
        break
    else:
        postbreached = input("Your post cant be shorter than five characters, try again:\n")

while True:
    if proxyrotator == 4:
        proxyrotator = 0
    chrome_options.add_argument("proxy-server="+proxies[proxyrotator])
    driver = webdriver.Chrome("chromedriver.exe",options=chrome_options)
    driver.minimize_window()
    try:
        driver.get("https://breached.to/member.php?action=login")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(account.split(":")[0])
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys(account.split(":")[1])
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "submit"))).click()
    except:
        print("Proxy not working, rotating proxy...")
        proxyrotator = proxyrotator+1
        driver.quit()
    else:
        break

driver.get("https://breached.to/Thread-Post-your-MEMES-here")
start_credits = int(WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/header/nav/div/ul/li[3]/a/span"))).text)
print("Start credits: "+str(start_credits))
iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"cke_1_contents\"]/iframe")))
driver.switch_to.frame(iframe)
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body"))).send_keys(postbreached)
driver.switch_to.default_content()
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "quick_reply_submit"))).click()
while True:
    try:
        driver.find_element(By.XPATH, "//*[@title='Delete this post']")
    except:
        time.sleep(0.001)
    else:
        print("Posted: "+postbreached)
        break
for i in range(posts):
    iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"cke_1_contents\"]/iframe")))
    driver.switch_to.frame(iframe)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body"))).send_keys("[b][/b]")
    driver.switch_to.default_content()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "quick_reply_submit"))).click()
    while True:
        postcount = driver.find_elements(By.CLASS_NAME, 'mycode_hr')
        if len(postcount) == i+1:
            break
        time.sleep(0.001)
    print("Posted "+str(len(postcount)))

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@title='Delete this post']"))).click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.jquery-modal.blocker.current > div > div > table > tbody > tr:nth-child(3) > td > div > input:nth-child(1)"))).click()
print("Deleted all evidence!")
driver.get("https://breached.to/newpoints.php")
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'NewPoints')]")))
current_credits = int(WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/header/nav/div/ul/li[3]/a/span"))).text)
print("Start credits: "+str(start_credits)+" and Current credits: "+str(current_credits)+" meaning that "+str(current_credits-start_credits)+" were generated")
driver.quit()
close = input("Press ENTER to close")