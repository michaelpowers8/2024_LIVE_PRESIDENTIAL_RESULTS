from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from pandas import DataFrame
from random import random
from re import findall,sub
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
sleep(4.53298)
driver.get("https://www.azcentral.com/elections/results/2024-11-05/race/0/arizona")
first_iteration:bool = True
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
        if('Select a county to jump to results' in line and not(counties_found)):
            counties_found:bool = True
        if(
            ("County" in line)and
            (not('Election' in line))and
            (counties_found)
        ):
            current_row:list = []
            kamala_vote_line:str = lines[i+4]
            kamala_vote_counts:list[str] = kamala_vote_line.split(' ')
            current_row.append(int(kamala_vote_counts[0].replace('-','0').replace(',','').replace('%','')))
            current_row.append(float(kamala_vote_counts[1].replace('-','0').replace(',','').replace('%','')))
            trump_vote_line:str = lines[i+10]
            trump_vote_counts:list[str] = trump_vote_line.split(' ')
            current_row.append(int(trump_vote_counts[0].replace('-','0').replace(',','').replace('%','')))
            current_row.append(float(trump_vote_counts[1].replace('-','0').replace(',','').replace('%','')))
            current_row.append(float(findall(r"[0-9]{1,}[\.]{0,1}[0-9]{0,2}\%",lines[i+1].replace('-','0'))[0].replace('%','')))
            third_party_vote_count:int = int(lines[i+6].split(' ')[0].replace('-','0').replace(',','').replace('%',''))+int(lines[i+8].split(' ')[0].replace('-','0').replace(',','').replace('%',''))
            current_row.insert(0,
                        int(trump_vote_counts[0].replace('-','0').replace(',','').replace('%',''))+int(kamala_vote_counts[0].replace('-','0').replace(',','').replace('%',''))+third_party_vote_count)
            
            if(first_iteration):
                DataFrame([current_row],columns=['Total_Votes','KH_Vote_Count','KH_Vote_Pct','DT_Vote_Count','DT_Vote_Pct','Pct_Reported'],index=[extraction_time])\
                    .to_csv(f'C:/Users/michael/Documents/Election_Statistics/2024_LIVE_PRESIDENTIAL_RESULTS/State_Details/Arizona/{line.replace("-","_").replace(" ","_")}.csv',
                            mode='w',header=True,index=True,float_format='%.3f')
                current_row:list = []
            else:
                DataFrame([current_row],columns=['Total_Votes','KH_Vote_Count','KH_Vote_Pct','DT_Vote_Count','DT_Vote_Pct','Pct_Reported'],index=[extraction_time])\
                    .to_csv(f'C:/Users/michael/Documents/Election_Statistics/2024_LIVE_PRESIDENTIAL_RESULTS/State_Details/Arizona/{line.replace("-","_").replace(" ","_")}.csv',
                            mode='a',header=False,index=True,float_format='%.3f')
        if('Yuma' in line):
            first_iteration:bool = False
            break
    first_iteration:bool = False