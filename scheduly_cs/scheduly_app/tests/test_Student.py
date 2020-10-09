from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
import random


user_id = "2131110038@cs.ku.edu.kw"
password = "Amnah1234"
path = "driver/chromedriver85.exe"
driver = webdriver.Chrome(executable_path=path)
driver.maximize_window()

def test_Validate_Login_Student():
    driver.get("http://15.236.43.203:8000/")
    driver.find_element_by_xpath("//a[contains(text(),'Login')]").click()
    driver.find_element_by_xpath("//input[@placeholder='email@example.com']").send_keys(user_id)
    driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys(password)
    driver.find_element_by_xpath("//button[@class='form-button-submit rounded-pill']").click()
    message = driver.find_element_by_xpath("//div[@class='alert alert-success']").text
    assert "Welcome Back!" in message.strip()

def test_Validate_HomePage_Student():
    driver.find_element_by_xpath("//a[contains(text(),'Home')]").click()
    assert "Home" in driver.title
    message = driver.find_element_by_xpath("//p[@class='home-intro']").text
    assert "The Computer Science Department aspires to be an outstanding academic institution for teaching and research in computing. The department is to be the best locally, one of the leading Computer Science departments in the reigon, and recognized internationally." in message.strip()

# Validate successfull change password
def test_Validate_Profile_Successfull_Update_Password_Student():
    driver.find_element_by_xpath("//a[contains(text(),'Profile')]").click()
    assert "Profile" in driver.title
    driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys("Pass123")
    driver.find_element_by_xpath("//input[@placeholder='confirm new password']").send_keys("Pass123")
    driver.find_element_by_xpath("//button[@class='form-button-submit rounded-pill']").click()
    message = driver.find_element_by_xpath("//div[@class='alert alert-success']").text
    assert "Profile has been updated successfully!" in message.strip()

    driver.find_element_by_xpath("//a[contains(text(),'Login')]").click()
    driver.find_element_by_xpath("//input[@placeholder='email@example.com']").send_keys(user_id)
    driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys("Pass123")
    driver.find_element_by_xpath("//button[@class='form-button-submit rounded-pill']").click()
    message = driver.find_element_by_xpath("//div[@class='alert alert-success']").text
    assert "Welcome Back!" in message.strip()

    driver.find_element_by_xpath("//a[contains(text(),'Profile')]").click()
    driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys(password)
    driver.find_element_by_xpath("//input[@placeholder='confirm new password']").send_keys(password)
    driver.find_element_by_xpath("//button[@class='form-button-submit rounded-pill']").click()
    message = driver.find_element_by_xpath("//div[@class='alert alert-success']").text
    assert "Profile has been updated successfully!" in message.strip()



# Validate error message for incorrect change password
def test_Validate_Error_Message_Profile_Update_Password_Student():

    driver.find_element_by_xpath("//a[contains(text(),'Login')]").click()
    driver.find_element_by_xpath("//input[@placeholder='email@example.com']").send_keys(user_id)
    driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys(password)
    driver.find_element_by_xpath("//button[@class='form-button-submit rounded-pill']").click()
    message = driver.find_element_by_xpath("//div[@class='alert alert-success']").text
    assert "Welcome Back!" in message.strip()


    driver.find_element_by_xpath("//a[contains(text(),'Profile')]").click()
    assert "Profile" in driver.title
    driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys("Pass123")
    driver.find_element_by_xpath("//input[@placeholder='confirm new password']").send_keys("SomeRandomeNumber")
    driver.find_element_by_xpath("//button[@class='form-button-submit rounded-pill']").click()
    message = driver.find_element_by_xpath("//div[@class='alert alert-warning']").text
    assert "password and confirm password do not match!" in message.strip()

# Validate change password if user enter current password
def test_Validate__Profile_Update_Password_Student_Same_Pass():
    driver.find_element_by_xpath("//a[contains(text(),'Profile')]").click()
    assert "Profile" in driver.title
    driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys(password)
    driver.find_element_by_xpath("//input[@placeholder='confirm new password']").send_keys(password)
    driver.find_element_by_xpath("//button[@class='form-button-submit rounded-pill']").click()
    message = driver.find_element_by_xpath("//div[@class='alert alert-success']").text
    assert "Profile has been updated successfully!" in message.strip()

    driver.find_element_by_xpath("//a[contains(text(),'Login')]").click()
    driver.find_element_by_xpath("//input[@placeholder='email@example.com']").send_keys(user_id)
    driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys(password)
    driver.find_element_by_xpath("//button[@class='form-button-submit rounded-pill']").click()
    message = driver.find_element_by_xpath("//div[@class='alert alert-success']").text
    assert "Welcome Back!" in message.strip()

# Validate Help Functionality
def test_Validate_Help_Page_Student():
    driver.find_element_by_xpath("//a[contains(text(),'Help')]").click()
    assert "Help" in driver.title
    message = driver.find_element_by_xpath("//h1").text
    assert "Not yet registered?" in message.strip()


# Validate Progress Functionality
def test_Validate_Progress_Student():
    driver.get("http://15.236.43.203:8000/student/progress/")
    assert "Progress" in driver.title
    message = driver.find_element_by_xpath("//h1").text
    assert "Your current progress is:" in message.strip()
    message = driver.find_element_by_xpath("//h5").text
    assert "Please check all the courses you passed and keep the courses you wish to take unchecked" in message.strip()
    driver.find_element_by_xpath("//label[1]//span[1]").click()
    driver.find_element_by_xpath("//label[1]//span[1]").click()
    driver.find_element_by_xpath("//button[contains(text(),'Update progress')]").click()

# Validate Plan Functionality
def test_Validate_Plan_Student():
    driver.get("http://15.236.43.203:8000/student/plan/")
    assert "Student Suggested Plan" in driver.title
    message = driver.find_element_by_xpath("//h1").text
    assert "The plan for your future semesters:" in message.strip()
    message = driver.find_element_by_xpath("//tr[3]//td[1]").text
    assert "Number of credits outside of the department for the next semester:" in message.strip()

# Validate Wishlist Functionality
def test_Add_Wishlist_Student():
    driver.find_element_by_xpath("//a[contains(text(),'Wishlist')]").click()
    time.sleep(2)
    assert "Student Wishlist" in driver.title
    driver.find_element_by_xpath("//label[contains(text(),'0418346 Declarative Programming')]").click()
    obj = driver.switch_to.alert
    message = obj.text
    print("Alert shows following message: " + message)
    time.sleep(2)
    obj.accept()
    driver.find_element_by_xpath("//button[@id='nextButton']").click()
    obj = driver.switch_to.alert
    message = obj.text
    print("Alert shows following message: " + message)
    time.sleep(2)
    obj.accept()
    driver.find_element_by_xpath("//button[@id='nextButton']").click()
    message = driver.find_element_by_xpath("//div[@class='alert alert-success']").text
    assert "Your whishlist has been saved!" in message.strip()
    driver.close()



