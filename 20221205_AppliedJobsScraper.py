#Imports
from selenium import webdriver
import pandas as pd

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#LinkedIn Credentials
username='Update w/username'
password='Update w/password'

#URL's
loginurl='https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Fmy-items%2Fsaved-jobs%2F%3Fstart%3D0&fromSignIn=true&trk=cold_join_sign_in'
applied_url='https://www.linkedin.com/my-items/saved-jobs/?start=0'

#Posting info placeholders
company_name=[]
job_title=[]

#Load the web driver and get the url
driver = webdriver.Chrome(r'Update path to chromedriver file\\chromedriver.exe')
driver.get(loginurl)

#Find username/email field and fill in
driver.find_element(By.ID, "username").send_keys(username)

#Find password input field and fill in
driver.find_element(By.ID, "password").send_keys(password)

#Click login button
wait = WebDriverWait(driver, 10)
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
                                       "button[type='submit']"))).click()
driver.implicitly_wait(10)

#Page variable controls what page in list you're viewing. 
#LinkedIn increases it by 10 for each page back in history
page=0

#Loops through application history until it hits your designated stop point
while page<210:
    try:
        for i in range(11):
            #Find position title & append to list
            title=driver.find_elements(By.CLASS_NAME, 
                                       'entity-result__title-text')[i].text
            job_title.append(title)

            #Find company name & append to list            
            company=driver.find_elements(By.CLASS_NAME, 
                                         'entity-result__primary-subtitle')[i].text
            company_name.append(company)

    #Handles when page runs out of application info
    except IndexError: print(f'No posting at {i}, {page}')
    
    #Increases page variable to move to next page
    page+=10
    driver.get(applied_url+str(page))
    driver.implicitly_wait(5)

#Close driver window once information is pulled
driver.close()    

#Zips company and job info together, pushes to dataframe, then save to excel
zipped=list(zip(company_name, job_title))
df=pd.DataFrame(zipped, columns=['Company', 'Job Title'])
df.to_csv('Applied_Jobs_List.csv', index=False)
