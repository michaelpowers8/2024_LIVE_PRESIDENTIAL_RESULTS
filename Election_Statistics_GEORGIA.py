from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from pandas import DataFrame
from random import random
from re import search,findall,sub
from time import sleep

# WebDriver Chrome
options = ChromeOptions()
#options.add_argument('--headless=new')
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
#sleep(4.53298)
driver.get("https://www.nbcnews.com/politics/2024-elections/georgia-president-results")
wait:WebDriverWait = WebDriverWait(driver,(random()*4)+2)
page:str = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body"))).text
first_iteration:bool = True
counties_found:bool = False
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
    counties_found:bool = False
    for i,line in enumerate(lines):
        if('APPLING' in line and not(counties_found)):
            counties_found:bool = True
        if('Exit Polls' in line):
            break
        if(counties_found and line.upper().__eq__(line) and not(search(r"[0-9]+",line)) and not(line.isspace()) and len(line)>3):
            leading_candidate = lines[i+3]
            try:
                if('Harris' in leading_candidate):
                    current_row = [
                        int(search(r"[0-9]+",sub(r"[A-Za-z]+","",lines[i+1]).replace(',','').replace('.','').replace('%','')).group()),
                        int(search(r"[0-9]+",lines[i+5].replace(',','').replace('.','').replace('%','')).group()),
                        float(search(r"[0-9]+\.[0-9]+",lines[i+6]).group()),
                        int(search(r"[0-9]+",lines[i+9].replace(',','').replace('.','').replace('%','')).group()),
                        float(search(r"[0-9]+\.[0-9]+",lines[i+10]).group()),
                        float(search(r"[0-9]+[\.]{0,1}[0-9]{0,2}\%",lines[i+2]).group().replace(' ','').replace('%',''))
                    ]
                else:
                    current_row = [
                        int(search(r"[0-9]+",sub(r"[A-Za-z]+","",lines[i+1]).replace(',','').replace('.','').replace('%','')).group()),
                        int(search(r"[0-9]+",lines[i+9].replace(',','').replace('.','').replace('%','')).group()),
                        float(search(r"[0-9]+\.[0-9]+",lines[i+10]).group()),
                        int(search(r"[0-9]+",lines[i+5].replace(',','').replace('.','').replace('%','')).group()),
                        float(search(r"[0-9]+\.[0-9]+",lines[i+6]).group()),
                        float(search(r"[0-9]+[\.]{0,1}[0-9]{0,2}\%",lines[i+2]).group().replace(' ','').replace('%',''))
                    ]
                if(first_iteration):
                    DataFrame([current_row],columns=['Total_Votes','KH_Vote_Count','KH_Vote_Pct','DT_Vote_Count','DT_Vote_Pct','Pct_Reported'],index=[extraction_time])\
                        .to_csv(f'State_Details/Georgia/{line.replace("-","_").replace(" ","_")}_Results.csv',
                                mode='w',header=True,index=True,float_format='%.3f')
                    first_iteration:bool = False
                else:
                    DataFrame([current_row],columns=['Total_Votes','KH_Vote_Count','KH_Vote_Pct','DT_Vote_Count','DT_Vote_Pct','Pct_Reported'],index=[extraction_time])\
                        .to_csv(f'State_Details/Georgia/{line.replace("-","_").replace(" ","_")}_Results.csv',
                                mode='a',header=False,index=True,float_format='%.3f')
            except:pass