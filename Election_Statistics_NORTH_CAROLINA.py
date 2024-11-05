from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from pandas import DataFrame
from random import random
from re import findall
from time import sleep

# WebDriver Chrome
options = ChromeOptions()
options.add_argument('--headless=new')
# adding argument to disable the AutomationControlled flag 
options.add_argument("--disable-blink-features=AutomationControlled") 
# exclude the collection of enable-automation switches 
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
# turn-off userAutomationExtension 
options.add_experimental_option("useAutomationExtension", False)
options.add_argument('--disable-extensions')
options.add_argument('--profile-directory=Default')
options.add_argument("--incognito")
options.add_argument("--disable-plugins-discovery")
options.add_argument("--start-maximized")

driver:Chrome = Chrome(options=options)
sleep(4.53298)
driver.get("https://www.foxnews.com/elections/2024/general-results/state/north-carolina")
first_iteration:bool = True
sleep(3.32382901)
while True:
    sleep(random()*13.329104+11.430829)
    if(random()<0.0025):
        print('PAUSING')
        sleep(75)
    wait:WebDriverWait = WebDriverWait(driver,(random()*4)+2)
    page:str = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body"))).text
    lines:list[str] = page.split('\n')
    extraction_time:datetime = datetime.now()
    print(f"{extraction_time.strftime('%D, %H:%M:%S.%f')}")
    current_row:list = [0]*7
    for i,line in enumerate(lines):
        if('Electoral Votes' in line):
            current_row[4] = float(lines[i+5].replace('%','').replace(',','').replace(' ',''))
            current_row[5] = int(lines[i+7].replace('%','').replace(',','').replace(' ',''))
            current_row[6] = int(lines[i+3].replace('%','').replace(',','').replace(' ',''))
        if('Statewide Results' in line):
            current_row[0] = int(findall(r"[0-9]+",lines[i+3].replace(',','').replace('-','0'))[0])
            current_row[1] = float(findall(r"[0-9]+",lines[i+3].replace(',','').replace('-','0'))[1])
            current_row[2] = int(findall(r"[0-9]+",lines[i+6].replace(',','').replace('-','0'))[0])
            current_row[3] = float(findall(r"[0-9]+",lines[i+6].replace(',','').replace('-','0'))[1])
            if(first_iteration):
                DataFrame([current_row],columns=['KH_Vote_Count','KH_Vote_Pct','DT_Vote_Count','DT_Vote_Pct','Pct_Reported','Est_Votes_Remain','Population'],index=[extraction_time])\
                    .to_csv(f'State_Details/{"North_Carolina".replace("-","_").replace(" ","_")}_Results.csv',
                            mode='w',header=True,index=True,float_format='%.3f')
                first_iteration:bool = False
            else:
                DataFrame([current_row],columns=['KH_Vote_Count','KH_Vote_Pct','DT_Vote_Count','DT_Vote_Pct','Pct_Reported','Est_Votes_Remain','Population'],index=[extraction_time])\
                    .to_csv(f'State_Details/{"North_Carolina".replace("-","_").replace(" ","_")}_Results.csv',
                            mode='a',header=False,index=True,float_format='%.3f')
            current_row:list = [0]*7
            break