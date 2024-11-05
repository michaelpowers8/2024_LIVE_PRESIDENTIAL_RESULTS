from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from pandas import DataFrame
from random import random
from re import search
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
driver = Chrome(options=options)
driver.get(f"https://www.electionreturns.pa.gov/General/CountyBreakDownResults?officeId=1&districtId=1&ElectionID=105&ElectionType=G&IsActive=1&isRetention=0")

county_results:dict[str,list] = {}
first_iteration:bool = True

while True:
    driver.refresh()
    sleep(random()*42.4321987+random()*19.312087+5.192837)
    wait:WebDriverWait = WebDriverWait(driver,(random()*4)+2)
    page:str = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body"))).text
    extraction_time:datetime = datetime.now()
    print(extraction_time.strftime('%D, %H:%M:%S.%f'))
    lines:list[str] = page.split('\n')
    # PENNSYLVANIA COUNTY RESULTS
    counties_found:bool = False
    for i,line in enumerate(lines):
        if(line.upper().__eq__(line) and not(counties_found)):
            counties_found:bool = True
        if(
            (line.upper().__eq__(line))and 
            (counties_found)and 
            (not('KAMALA' in line))and
            (not('TRUMP' in line))and
            (not('CHASE OLIVER' in line))and
            (not('JILL STEIN' in line))and
            (not('PRIVACY POLICY' in line))and
            (not('COPYRIGHT' in line))and
            (not('COMMONWEALTH' in line))and
            (not('SECURITY POLICY' in line))and
            (not('TESTING MODE' in line))and
            (not(line.isspace()))and
            (len(line)>0)
        ):
            county_results[line] = [
                [
                    extraction_time,
                    float(search(r"[0-9]{1,3}\.[0-9]{1,2}\%",lines[i+4]).group().replace('%','')), # Kamala Harris Vote Percent
                    int(search(r"Votes: .+",lines[i+4]).group().replace('%','').replace(',','').replace('Votes:','').replace(' ','').replace('(','').replace(')','')), # Kamala Harris Vote Count
                    float(search(r"[0-9]{1,3}\.[0-9]{1,2}\%",lines[i+7]).group().replace('%','')), # Donald Trump Vote Percent
                    int(search(r"Votes: .+",lines[i+7]).group().replace('%','').replace(',','').replace('Votes:','').replace(' ','').replace('(','').replace(')','')) # Donald Trump Vote Count
                ] 
                                            ]
    if(first_iteration): 
        for key in county_results.keys():
            DataFrame(county_results[key],columns=['Extraction_Datetime','KH_Vote_Pct','KH_Vote_Count','DT_Vote_Pct','DT_Vote_Count']).set_index('Extraction_Datetime').to_csv(
                f"State_Details/Pennsylvania/{key.upper().replace(' ','_')}_Results.csv",header=True,index=True,float_format='%.4f',mode='w') 
        first_iteration:bool = False  
    else:
        for key in county_results.keys():
            DataFrame(county_results[key],columns=['Extraction_Datetime','KH_Vote_Pct','KH_Vote_Count','DT_Vote_Pct','DT_Vote_Count']).set_index('Extraction_Datetime').to_csv(
                f"State_Details/Pennsylvania/{key.upper().replace(' ','_')}_Results.csv",header=False,index=True,float_format='%.4f',mode='a')