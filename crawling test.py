from selenium import webdriver
import pandas as pd
import time
import json
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import clipboard
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import pyautogui
import os.path

def starttoend(start, end, year, month, day):
    s_year = start[0:4]
    s_mon = start[4:6]
    s_day = start[6:8]
    e_year = end[0:4]
    e_mon = end[4:6]
    e_day = end[6:8]
    ret = []
    for i in range(year.index(s_year), year.index(e_year)+1):
        for j in range(month.index(s_mon), month.index(e_mon)+1):
            if i == year.index(s_year) and j == month.index(s_mon):
                for k in range(day.index(s_day), 31):
                    ret.append(year[i]+month[j]+day[k])
            elif i == year.index(e_year) and j == month.index(e_mon):
                for k in range(0, day.index(e_day)+1):
                    ret.append(year[i]+month[j]+day[k])
            else:
                for k in range(31):
                    ret.append(year[i]+month[j]+day[k])
    return ret
                    
    
#name of papers to find
papernames = ["tulsa-world"]
start = "20200525"
end = "20200614"
cont_fail = 0
dates = []

year = ["2020"]
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
days = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]


date_tul = starttoend(start, end, year, months, days)

dates.append(date_tul)

index = list(range(25))

#set up to save print as PDF file
settings = {
    "appState": {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local"
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }  
}
prefs = {'printing.print_preview_sticky_settings': json.dumps(settings)}

#change chrome printing option to minimize work.
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--kiosk-printing')

#traverse through all papers
for i in range(len(papernames)):
    #traverse through dates
    for j in dates[i]:
        count = 1
        dobreak = False
        for k in index:
            if(dobreak):
                break
            try:
                #run driver.
                driver = webdriver.Chrome(r'C:\Users\Asui\Downloads\chromedriver_win32\chromedriver.exe', chrome_options=chrome_options)
                driver.get("https://www.pressreader.com/usa/" + papernames[i] +"/"+j+"/page/1/textview")
                actions1 = webdriver.common.action_chains.ActionChains(driver)
                actions2 = webdriver.common.action_chains.ActionChains(driver)

                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="thumbsToolbarBottom_0"]/a')))

                bottom_button = driver.find_element_by_xpath('//*[@id="thumbsToolbarBottom_0"]/a')
    
                bottom_button.click()

                time.sleep(2)

                all_bottom = driver.find_element_by_xpath('//*[@id="thumbsToolbarBottomPreview_0"]')
                all_news = all_bottom.find_elements_by_xpath('//a[@page-number="1"]')
                
                news = all_news[k]
                first = True
            
                article_id = news.get_attribute("article-id")
                print(article_id)
                actions1.move_to_element(news).perform()
                news.click()



                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//article[@aid="'+str(article_id)+'"]')))
                time.sleep(2)
                arti = driver.find_element_by_xpath('//article[@aid="'+str(article_id)+'"]')
                head = arti.find_element_by_tag_name("hgroup")
                time.sleep(1)
                actions2.move_to_element(head).perform()
                time.sleep(1)
                actions2.context_click(head).perform()

                time.sleep(2)
                printbutton = driver.find_element_by_xpath('/html/body/div[12]/div/section/div/div/ul/li[7]/a')
                printbutton.click()

                time.sleep(1)

                printtext = driver.find_element_by_xpath('/html/body/div[12]/div/section/div/div/ul/li[1]/a')
                printtext.click()

                time.sleep(4)
                name = ""
                if(count < 10):
                    name = papernames[i]+"_"+j +"_"+"0"+ str(count)
                    pyautogui.typewrite(papernames[i]+"_"+j +"_"+"0"+ str(count))
                else:
                    name = papernames[i]+ "_"+j +"_" + str(count)
                    pyautogui.typewrite(papernames[i]+ "_"+j +"_" + str(count))
                        
                    
                time.sleep(1)
                pyautogui.press('enter')
                print("saved" + name)
    
                time.sleep(10)
                
                count+=1
                cont_fail = 0
                if k == len(all_news)-1:
                    driver.quit()
                    dobreak = True
                    break
                driver.quit()
                time.sleep(1)
            except:
                cont_fail += 1
                print("failed on" + papernames[i]+j+str(k))
                driver.quit()
                if cont_fail > 5:
                    break
                continue






