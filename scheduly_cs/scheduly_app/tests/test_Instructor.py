from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
import random


user_id = "abdullah@gmail.com"
password = "Amnah1234"
path = "driver/chromedriver85.exe"
driver = webdriver.Chrome(executable_path=path)
driver.maximize_window()

def test_Validate_Login_Instructor():
    driver.get("http://15.236.43.203:8000/")
    driver.find_element_by_xpath("//a[contains(text(),'Login')]").click()
    driver.find_element_by_xpath("//input[@placeholder='email@example.com']").send_keys(user_id)
    driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys(password)
    driver.find_element_by_xpath("//button[@class='form-button-submit rounded-pill']").click()
    message = driver.find_element_by_xpath("//div[@class='alert alert-success']").text
    assert "Welcome Back!" in message.strip()

def test_Validate_HomePage_Instructor():
    driver.find_element_by_xpath("//a[contains(text(),'Home')]").click()
    assert "Home" in driver.title
    message = driver.find_element_by_xpath("//p[@class='home-intro']").text
    assert "The Computer Science Department aspires to be an outstanding academic institution for teaching and research in computing. The department is to be the best locally, one of the leading Computer Science departments in the reigon, and recognized internationally." in message.strip()

# Validate successfull change password
def test_Validate_Profile_Successfull_Update_Password_Instructor():
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
def test_Validate_Error_Message_Profile_Update_Password_Instructor():

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
def test_Validate__Profile_Update_Password_Instructor_Same_Pass():
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
def test_Validate_Help_Page_Instructor():
    driver.find_element_by_xpath("//a[contains(text(),'Help')]").click()
    assert "Help" in driver.title
    message = driver.find_element_by_xpath("//h1").text
    assert "Not yet registered?" in message.strip()




# Validate Students Statistics Functionality
def test_Students_Statistics_Instructor():
    driver.get("http://15.236.43.203:8000/students/statistics/")
    headingcourse = driver.find_element_by_xpath("(//table[@class='table table-striped table-dark']//tr/th)[1]").text
    assert "Course#" in headingcourse.strip()
    headingcourse = driver.find_element_by_xpath("(//table[@class='table table-striped table-dark']//tr/th)[2]").text
    assert "Course Name" in headingcourse.strip()
    headingcourse = driver.find_element_by_xpath("(//table[@class='table table-striped table-dark']//tr/th)[3]").text
    assert "#advise" in headingcourse.strip()


# Validate Wishlist Functionality
def test_Add_Wishlist_Instructor():
    driver.find_element_by_xpath("//a[contains(text(),'Wishlist')]").click()
    time.sleep(2)
    assert "Instructor Wishlist" in driver.title
    driver.find_element_by_xpath("//label[contains(text(),'0418111 Discrete Mathematics forComputer Science')]").click()
    driver.find_element_by_xpath("//label[contains(text(),'0418141 Computer Programming I')]").click()
    driver.find_element_by_xpath("//label[contains(text(),'0418142 Computer Programming II')]").click()
    driver.find_element_by_xpath("//label[contains(text(),'0418201 Data Structures and Algorithms')]").click()
    driver.find_element_by_xpath("//label[contains(text(),'0418211 Theory ofComputation I')]").click()
    driver.find_element_by_xpath("//label[contains(text(),'0418220 Programming in C & Unix')]").click()
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
    driver.find_element_by_xpath("//label[contains(text(),'0418220 Programming in C & Unix')]").click()
    driver.find_element_by_xpath("//button[@id='nextButton']").click()
    BackToWishlist_Message = driver.find_element_by_xpath("//a[@class ='btn btn-secondary rounded-pill']").text
    assert "Back to Wishlist" in BackToWishlist_Message.strip()
    # message = driver.find_element_by_xpath("//div[@class='alert alert-success']").text
    # assert "Your whishlist has been saved" in message.strip()

    Set_PrefferenceTime_Message = driver.find_element_by_xpath("//h2[contains(@class,'selectcoursestitle')]").text
    assert "Set your Unpreferred Lecture Time" in Set_PrefferenceTime_Message.strip()

    select = Select(driver.find_element_by_id('days1'))
    select.select_by_value("24")
    driver.find_element_by_xpath("//td[1]//div[1]//div[2]//input[1]").send_keys("21:30")
    driver.find_element_by_xpath("//td[1]//div[1]//div[2]//input[2]").send_keys("22:45")

    select2 = Select(driver.find_element_by_id('days2'))
    select2.select_by_value("135")
    driver.find_element_by_xpath("//td[2]//div[1]//div[2]//input[1]").send_keys("18:53")
    driver.find_element_by_xpath("//td[2]//div[1]//div[2]//input[2]").send_keys("20:53")
    driver.find_element_by_xpath("//button[@id='submitButton']").click()
    message = driver.find_element_by_xpath("//div[@class='alert alert-success']").text
    assert "Your unpreferred lecture time has been set" in message.strip()
    driver.close()

