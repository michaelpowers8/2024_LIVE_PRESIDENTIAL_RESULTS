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

states:list[str] = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
               "District Of Columbia", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois",
               "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", 
               "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", 
               "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", 
               "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont", 
               "Washington", "Wisconsin", "West Virginia", "Wyoming"]

driver:Chrome = Chrome(options=options)
sleep(4.53298)
driver.get("https://www.foxnews.com/elections")
first_iteration:bool = True
sleep(3.32382901)
while True:
    sleep(random()*13.329104+11.430829)
    wait:WebDriverWait = WebDriverWait(driver,(random()*4)+2)
    page:str = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body"))).text
    lines:list[str] = page.split('\n')
    extraction_time:datetime = datetime.now()
    all_states_found:bool = False
    for i,line in enumerate(lines):
        if('All State Races' in line and 'Alaska' in lines[i+2] and '3' in lines[i+3]):
            all_states_found:bool = True
        if(all_states_found):
            if(line in states):
                current_row:list = [
                        int(findall(r"[0-9]+",lines[i+5].replace(',','').replace('-','0'))[0]),
                        float(findall(r"[0-9]+",lines[i+5].replace(',','').replace('-','0'))[1]),
                        int(findall(r"[0-9]+",lines[i+8].replace(',','').replace('-','0'))[0]),
                        float(findall(r"[0-9]+",lines[i+8].replace(',','').replace('-','0'))[1])
                    ]
                if(first_iteration):
                    DataFrame([current_row],columns=['KH_Vote_Count','KH_Vote_Pct','DT_Vote_Count','DT_Vote_Pct'],index=[extraction_time])\
                        .to_csv(f'State_Summary_Results/{line.replace("-","_").replace(" ","_")}_Results.csv',
                                mode='w',header=True,index=True,float_format='%.3f')
                else:
                    DataFrame([current_row],columns=['KH_Vote_Count','KH_Vote_Pct','DT_Vote_Count','DT_Vote_Pct'],index=[extraction_time])\
                        .to_csv(f'State_Summary_Results/{line.replace("-","_").replace(" ","_")}_Results.csv',
                                mode='a',header=False,index=True,float_format='%.3f')
        if('Sponsored Stories' in line and all_states_found):
            break
    first_iteration:bool = False