from selenium import webdriver
from selenium.webdriver.common.by import By
from math import ceil
from datetime import datetime
from pandas import DataFrame
from random import random
from re import search
from time import sleep
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
state_names:list[str] = ["Arizona","Florida","Georgia","Michigan", "Nevada", "North Carolina", "Pennsylvania", "Virginia", "Wisconsin"]
first_iteration:bool = True
while True:
    sleep((random()*10)+(random()*3))
    extraction_time = datetime.now()
    for state in state_names:
        driver.get(f"https://www.nbcnews.com/politics/2024-elections/{state.lower()}-results")
        page:str = driver.find_element(By.XPATH, "/html/body").text
        lines = page.split('\n')
        total_votes_found:bool = False
        democrat_pct_found:bool = False
        for line in lines:
            if('mail-in and early in-person votes cast' in line.lower()):
                total_votes:int = int(search(r"[0-9]{3,}",line.replace(',','')).group())
                total_votes_found:bool = True
            if('%' in line and total_votes_found and not(democrat_pct_found)):
                democrat_pct:int = int(search(r"[0-9]+",line.replace('%','')).group())
                democrat_vote_estimate:int = ceil(total_votes*(democrat_pct/100))
                democrat_pct_found:bool = True
            elif('%' in line and total_votes_found and democrat_pct_found):
                republican_pct:int = int(search(r"[0-9]+",line.replace('%','')).group())
                republican_vote_estimate:int = ceil(total_votes*(republican_pct/100))
                other_pct:int = 100-democrat_pct-republican_pct
                other_votes_estimate:int = total_votes-democrat_vote_estimate-republican_vote_estimate
                break
        if(first_iteration):
            DataFrame(
                [[extraction_time,total_votes,democrat_vote_estimate,democrat_pct,republican_vote_estimate,republican_pct,other_votes_estimate,other_pct]],
                columns=['Extraction_Datetime','Total_Votes','Democratic_Vote_Count','Democratic_Vote_Percent','Republican_Vote_Count',
                        'Republican_Vote_Percent','Other_Vote_Count','Other_Vote_Percent']).to_csv(
                            index=False,mode='w',path_or_buf=f"State_Summary_Results/{state.replace(' ','_')}_Early_Results.csv",header=True)
            first_iteration:bool = False
        else:
            DataFrame(
                [[extraction_time,total_votes,democrat_vote_estimate,democrat_pct,republican_vote_estimate,republican_pct,other_votes_estimate,other_pct]],
                columns=['Extraction_Datetime','Total_Votes','Democratic_Vote_Count','Democratic_Vote_Percent','Republican_Vote_Count',
                        'Republican_Vote_Percent','Other_Vote_Count','Other_Vote_Percent']).to_csv(
                            index=False,mode='a',path_or_buf=f"State_Summary_Results/{state.replace(' ','_')}_Early_Results.csv",header=False)