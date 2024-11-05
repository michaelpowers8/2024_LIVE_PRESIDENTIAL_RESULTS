from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from pandas import DataFrame
from random import random
from re import sub
from time import sleep

def scroll_screen_down(driver:Chrome):
    SCROLL_PAUSE_TIME:float = 0.679348234
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


# WebDriver Chrome
options = ChromeOptions()
#options.add_argument('--headless=new')
# adding argument to disable the AutomationControlled flag 
options.add_argument("--disable-blink-features=AutomationControlled") 
# exclude the collection of enable-automation switches 
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
# turn-off userAutomationExtension 
options.add_experimental_option("useAutomationExtension", False) 
driver = Chrome(options=options)
driver.get("https://enr.elections.virginia.gov/results/public/Virginia/elections/2024NovemberGeneral/ballot-items/01000000-c7a0-1ae0-1363-08dcde4d9d9f")
sleep(27.437289)
wait = WebDriverWait(driver, 10)  # 10 seconds timeout
button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Vote Method']]")))
sleep(1.321891)
button.click()
sleep(0.9843294)
scroll_screen_down(driver=driver)
sleep(19.483024)


county_results:dict[str,list] = {}
first_iteration:bool = True

while True:
    sleep(random()*51.473892+random()*12.043298+3.43829)
    wait:WebDriverWait = WebDriverWait(driver,(random()*4)+2)
    page:str = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body"))).text
    extraction_time:datetime = datetime.now()
    print(extraction_time.strftime('%D, %H:%M:%S.%f'))
    lines:list[str] = page.split('\n')
    counties_found:bool = False
    for i,line in enumerate(lines):
        if(line.upper().__eq__(line) and 'LOCALITY RESULTS' in line and not(counties_found)):
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
            (not('OFFICIAL RESULTS' in line))and
            (not('ELECTIONS' in line))and
            (not('POWERED BY' in line))and
            (not('LOCALITY RESULTS' in line))and
            (not(line.isspace()))and
            (not(line.replace(' ','').isnumeric()))and
            (len(line)>0)
        ):
            kamala_vote_line:str = lines[i+5]
            kamala_vote_counts:list[str] = kamala_vote_line.split(' ')
            trump_vote_line:str = lines[i+8]
            trump_vote_counts:list[str] = trump_vote_line.split(' ')
            total_votes_line:str = sub(r"[a-zA-Z]", "", lines[i+23])
            while total_votes_line.startswith(' '):
                total_votes_line:str = total_votes_line[1:]
            while total_votes_line.endswith(' '):
                total_votes_line:str = total_votes_line[:-1]
            total_vote_counts:list[str] = total_votes_line.split(' ')
            final_list:list[str] = kamala_vote_counts.copy()
            final_list.extend(trump_vote_counts)
            final_list.extend(total_vote_counts)
            county_results[line] = [int(x) for x in final_list.copy()]
            county_results[line].insert(0,extraction_time)
    if(first_iteration):
        for key in county_results.keys():
            DataFrame(DataFrame(county_results[key]).T).set_axis([
                        'Extraction_Datetime',
                        'KH_Early','KH_Election_Day','KH_Mailed_Absentee','KH_Provisional','KH_Post_Election','KH_Total',
                        'DT_Early','DT_Election_Day','DT_Mailed_Absentee','DT_Provisional','DT_Post_Election','DT_Total',
                        'Total_Early','Total_Election_Day','Total_Mailed_Absentee','Total_Provisional','Total_Post_Election','Total_Total'
                    ],
                        axis=1).set_index('Extraction_Datetime').to_csv(f"State_Details/Virginia/{key.replace(' ','_')}_Results.csv",mode='w',header=True,index=True)
        first_iteration:bool = False
    else:
        for key in county_results.keys():
            DataFrame(DataFrame(county_results[key]).T).set_axis([
                        'Extraction_Datetime',
                        'KH_Early','KH_Election_Day','KH_Mailed_Absentee','KH_Provisional','KH_Post_Election','KH_Total',
                        'DT_Early','DT_Election_Day','DT_Mailed_Absentee','DT_Provisional','DT_Post_Election','DT_Total',
                        'Total_Early','Total_Election_Day','Total_Mailed_Absentee','Total_Provisional','Total_Post_Election','Total_Total'
                    ],
                        axis=1).set_index('Extraction_Datetime').to_csv(f"State_Details/Virginia/{key.replace(' ','_')}_Results.csv",mode='a',header=False,index=True)