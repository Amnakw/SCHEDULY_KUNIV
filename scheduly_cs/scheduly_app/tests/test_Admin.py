from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
import random


user_id = "admin@gmail.com"
password = "Amnah1234"
path = "driver/chromedriver.exe"
driver = webdriver.Chrome(executable_path=path)
driver.maximize_window()
def test_Validate_LoginAdmin():

    driver.get("http://15.236.43.203:8000/")
    driver.find_element_by_xpath("//a[contains(text(),'Login')]").click()
    driver.find_element_by_xpath("//input[@placeholder='email@example.com']").send_keys(user_id)
    driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys(password)
    driver.find_element_by_xpath("//button[@class='form-button-submit rounded-pill']").click()
    message = driver.find_element_by_xpath("//div[@class='alert alert-success']").text
    assert "Welcome Back!" in message.strip()

def test_Validate_HomePage_Admin():
    driver.find_element_by_xpath("//a[contains(text(),'Home')]").click()
    assert "Home" in driver.title
    message = driver.find_element_by_xpath("//p[@class='home-intro']").text
    assert "The Computer Science Department aspires to be an outstanding academic institution for teaching and research in computing. The department is to be the best locally, one of the leading Computer Science departments in the reigon, and recognized internationally." in message.strip()

# Validate successfull change password
def test_Validate_Profile_Successfull_Update_Password_Admin():
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
def test_Validate_Error_Message_Profile_Update_Password_Admin():

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
def test_Validate__Profile_Update_Password_Admin_Same_Pass():
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
def test_Validate_Help_Page_Admin():
    driver.find_element_by_xpath("//a[contains(text(),'Help')]").click()
    assert "Help" in driver.title
    message = driver.find_element_by_xpath("//h1").text
    assert "Not yet registered?" in message.strip()




# Validate Students Statistics Functionality
def test_Students_Statistics_Admin():
    driver.get("http://15.236.43.203:8000/students/statistics/")
    headingcourse = driver.find_element_by_xpath("(//table[@class='table table-striped table-dark']//tr/th)[1]").text
    assert "Course#" in headingcourse.strip()
    headingcourse = driver.find_element_by_xpath("(//table[@class='table table-striped table-dark']//tr/th)[2]").text
    assert "Course Name" in headingcourse.strip()
    headingcourse = driver.find_element_by_xpath("(//table[@class='table table-striped table-dark']//tr/th)[3]").text
    assert "#advise" in headingcourse.strip()




# Validate add Instructor Functionality
def test_Validate_Add_Instructor_Admin():
    driver.get("http://15.236.43.203:8000/manage/add/instructor/")
    heading = driver.find_element_by_xpath("//h3[@class='title']").text
    assert "Add an Instructor" in heading.strip()

    driver.find_element_by_xpath("//button[contains(@class,'rounded-pill')]").click()
    time.sleep(2)
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'username')]/ul/li").text
    assert "This field is required." in errormessage.strip()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'password')]/ul/li").text
    assert "This field is required." in errormessage.strip()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'instructor_id')]/ul/li").text
    assert "This field is required." in errormessage.strip()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'fullname')]/ul/li").text
    assert "This field is required." in errormessage.strip()

    driver.find_element_by_xpath("//input[@placeholder='Fullname']").send_keys("ABC")
    driver.find_element_by_xpath("//input[@placeholder='ID']").send_keys("aasdasd")
    driver.find_element_by_xpath("//input[@placeholder='Email address']").send_keys("abc@gmail.com")
    driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys("sdfsdf")
    driver.find_element_by_xpath("//span[@class='checkmark']").click()
    driver.find_element_by_xpath("//button[contains(@class,'rounded-pill')]").click()

    errormessage = driver.find_element_by_xpath("//li[contains(text(),'instructor_id')]/ul/li").text
    assert "Enter a whole number." in errormessage.strip()
    driver.find_element_by_xpath("//input[@placeholder='Fullname']").send_keys("New_Instructor")
    driver.find_element_by_xpath("//input[@placeholder='ID']").send_keys(9999)
    driver.find_element_by_xpath("//input[@placeholder='Email address']").send_keys("New_Instructor_9999@gmail.com")
    driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys("Pass123")
    driver.find_element_by_xpath("//span[@class='checkmark']").click()
    driver.find_element_by_xpath("//button[contains(@class,'rounded-pill')]").click()
    message = driver.find_element_by_xpath("//div[@class='alert alert-success']").text
    assert "The user was created successfuly" in message.strip()


# Validate Update Instructor Functionality
def test_Validate_Update_Instructor_Admin():
    driver.get("http://15.236.43.203:8000/manage/edit/users/")
    heading = driver.find_element_by_xpath("//h4[@class='title pt-4']").text
    assert "Instructors" in heading.strip()
    driver.find_element_by_xpath("//td[contains(text(),'New_Instructor')]//following-sibling::*/a").click()

    driver.find_element_by_xpath("//input[@name='fullname']").clear()
    driver.find_element_by_xpath("//input[@name='fullname']").send_keys("Updated_New_Instructor")
    driver.find_element_by_xpath("//input[@name='instructor_id']").clear()
    driver.find_element_by_xpath("//input[@name='instructor_id']").send_keys(87181)
    driver.find_element_by_xpath("//input[@name='username']").clear()
    driver.find_element_by_xpath("//input[@name='username']").send_keys("Updated_New_Instructor_87181@gmail.com")
    driver.find_element_by_xpath("//input[@name='password']").clear()
    driver.find_element_by_xpath("//input[@name='password']").send_keys("NewPass123")
    driver.find_element_by_xpath("//span[@class='checkmark']").click()
    driver.find_element_by_xpath("//button[@class='form-button-submit pr-5 btn-lg rounded-pill']").click()
    message = driver.find_element_by_xpath("//div[@class='alert alert-success']").text
    assert "The user was updated successfuly" in message.strip()


# Validate delete Instructor Functionality
def test_Validate_Delete_Instructor_Admin():
    driver.get("http://15.236.43.203:8000/manage/delete/users/")
    heading = driver.find_element_by_xpath("//h4[@class='title pt-4']").text
    assert "Instructors" in heading.strip()
    driver.find_element_by_xpath("//td[contains(text(),'Updated_New_Instructor')]//following-sibling::*/a").click()
    driver.find_element_by_xpath("//a[@class='btn btn-primary rounded-pill btn-block']").click()
    driver.find_element_by_xpath("//td[contains(text(),'New_Instructor')]//following-sibling::*/a").click()
    driver.find_element_by_xpath("//a[@class='btn btn-danger rounded-pill btn-block']").click()
    message = driver.find_element_by_xpath("//div[@class='alert alert-success']").text
    assert "User deleted" in message.strip()

# Validate add User Functionality
def test_Validate_Add_User_Admin():
    driver.get("http://15.236.43.203:8000/manage/add/student/")
    heading = driver.find_element_by_xpath("//h3[@class='title']").text
    assert "Add a Student" in heading.strip()

    driver.find_element_by_xpath("//button[contains(@class,'rounded-pill')]").click()
    time.sleep(2)
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'username')]/ul/li").text
    assert "This field is required." in errormessage.strip()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'password')]/ul/li").text
    assert "This field is required." in errormessage.strip()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'student_id')]/ul/li").text
    assert "This field is required." in errormessage.strip()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'fullname')]/ul/li").text
    assert "This field is required." in errormessage.strip()
    driver.find_element_by_xpath("//input[@placeholder='Fullname']").send_keys("ABC")
    driver.find_element_by_xpath("//input[@placeholder='ID']").send_keys("aasdasd")
    driver.find_element_by_xpath("//input[@placeholder='Email address']").send_keys("abc@gmail.com")
    driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys("sdfsdf")
    driver.find_element_by_xpath("//button[contains(@class,'rounded-pill')]").click()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'student_id')]/ul/li").text
    assert "Enter a whole number." in errormessage.strip()

    driver.find_element_by_xpath("//input[@placeholder='Fullname']").send_keys("New_Student")
    driver.find_element_by_xpath("//input[@placeholder='ID']").send_keys(2323)
    driver.find_element_by_xpath("//input[@placeholder='Email address']").send_keys("New_Student_2323@gmail.com")
    driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys("Pass123")
    driver.find_element_by_xpath("//button[contains(@class,'rounded-pill')]").click()
    message = driver.find_element_by_xpath("//div[@class='alert alert-success']").text
    assert "The user was created successfuly" in message.strip()


# Validate Update User Functionality
def test_Validate_Update_User_Admin():
    driver.get("http://15.236.43.203:8000/manage/edit/users/")
    heading = driver.find_element_by_xpath("(//h4)[2]").text
    assert "Students" in heading.strip()
    driver.find_element_by_xpath("//td[contains(text(),'New_Student')]//following-sibling::*/a").click()
    driver.find_element_by_xpath("//input[@name='fullname']").clear()
    driver.find_element_by_xpath("//input[@name='fullname']").send_keys("Updated_New_Student")
    driver.find_element_by_xpath("//input[@name='student_id']").clear()
    driver.find_element_by_xpath("//input[@name='student_id']").send_keys(45454)
    driver.find_element_by_xpath("//input[@name='username']").clear()
    driver.find_element_by_xpath("//input[@name='username']").send_keys("Updated_New_Student_45454@gmail.com")
    driver.find_element_by_xpath("//input[@name='password']").clear()
    driver.find_element_by_xpath("//input[@name='password']").send_keys("NewPass123")
    driver.find_element_by_xpath("//button[contains(@class,'rounded-pill')]").click()
    message = driver.find_element_by_xpath("//div[@class='alert alert-success']").text
    assert "The user was updated successfuly" in message.strip()


# Validate delete User Functionality
def test_Validate_Delete_User_Admin():
    driver.get("http://15.236.43.203:8000/manage/delete/users/")
    heading = driver.find_element_by_xpath("(//h4)[2]").text
    assert "Students" in heading.strip()
    driver.find_element_by_xpath("//td[contains(text(),'Updated_New_Student')]//following-sibling::*/a").click()
    driver.find_element_by_xpath("//a[@class='btn btn-primary rounded-pill btn-block']").click()
    driver.find_element_by_xpath("//td[contains(text(),'Updated_New_Student')]//following-sibling::*/a").click()
    driver.find_element_by_xpath("//a[@class='btn btn-danger rounded-pill btn-block']").click()
    message = driver.find_element_by_xpath("//div[@class='alert alert-success']").text
    assert "User deleted" in message.strip()



# Validate delete User Functionality
def test_Validate_Add_Course_Admin():
    driver.get("http://15.236.43.203:8000/manage/edit/major_sheet/")
    heading = driver.find_element_by_xpath("//h2[@class='title text-light text-white']").text
    assert "Edit Major Sheet" in heading.strip()
    driver.find_element_by_xpath("//a[contains(text(),'Add a Course')]").click()
    heading = driver.find_element_by_xpath("//h3[@class='title']").text
    assert "Add a Course" in heading.strip()

    driver.find_element_by_xpath("//button[@class='form-button-submit pr-5 btn-lg rounded-pill']").click()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'name')]/ul/li").text
    assert "This field is required." in errormessage.strip()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'number')]/ul/li").text
    assert "This field is required." in errormessage.strip()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'credits')]/ul/li").text
    assert "This field is required." in errormessage.strip()

    driver.find_element_by_xpath("//input[@placeholder='Course Name']").send_keys("Sample_Course_Name")
    driver.find_element_by_xpath("//input[@placeholder='Course Number']").send_keys("Sample_Course_Number")
    driver.find_element_by_xpath("//input[@placeholder='Course Credits']").send_keys("Sample_Course Credits")
    driver.find_element_by_xpath("//button[@class='form-button-submit pr-5 btn-lg rounded-pill']").click()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'number')]/ul/li").text
    assert "Ensure this value has at most 12 characters (it has 20)." in errormessage.strip()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'credits')]/ul/li").text
    assert "Enter a whole number." in errormessage.strip()


    driver.find_element_by_xpath("//input[@placeholder='Course Name']").send_keys("Sample_Course_Name")
    driver.find_element_by_xpath("//input[@placeholder='Course Number']").send_keys("888182")
    driver.find_element_by_xpath("//input[@placeholder='Course Credits']").send_keys("100000")
    driver.find_element_by_xpath("//button[@class='form-button-submit pr-5 btn-lg rounded-pill']").click()
    message = driver.find_element_by_xpath("//div[@class='alert alert-success']").text
    assert "The course was created successfuly" in message.strip()


# Validate Update Course Functionality
def test_Validate_Update_Course_Admin():
    driver.get("http://15.236.43.203:8000/manage/edit/major_sheet/")
    heading = driver.find_element_by_xpath("//h2[@class='title text-light text-white']").text
    assert "Edit Major Sheet" in heading.strip()
    driver.find_element_by_xpath("(//td[contains(text(),'Sample_Course_Name')]//following-sibling::*/a)[1]").click()
    driver.find_element_by_xpath("//input[@name='number']").clear()
    driver.find_element_by_xpath("//input[@name='number']").send_keys("333333")
    driver.find_element_by_xpath("//input[@name='name']").clear()
    driver.find_element_by_xpath("//input[@name='name']").send_keys("Updated Sample_Course_Name")
    driver.find_element_by_xpath("//input[@name='credits']").clear()
    driver.find_element_by_xpath("//input[@name='credits']").send_keys("212111")
    driver.find_element_by_xpath("//button[contains(@class,'rounded-pill')]").click()
    message = driver.find_element_by_xpath("//div[@class='alert alert-success']").text
    assert "Course Updated Sample_Course_Name has been updated successfully!" in message.strip()


# Validate delete Course Functionality
def test_Validate_Delete_Course_Admin():
    driver.get("http://15.236.43.203:8000/manage/edit/major_sheet/")
    heading = driver.find_element_by_xpath("//h2[@class='title text-light text-white']").text
    assert "Edit Major Sheet" in heading.strip()
    driver.find_element_by_xpath("(//td[contains(text(),'Updated Sample_Course_Name')]//following-sibling::*/a)[2]").click()
    driver.find_element_by_xpath("//a[@class='btn btn-primary rounded-pill btn-block']").click()
    driver.find_element_by_xpath("(//td[contains(text(),'Updated Sample_Course_Name')]//following-sibling::*/a)[2]").click()
    driver.find_element_by_xpath("//a[@class='btn btn-danger rounded-pill btn-block']").click()
    message = driver.find_element_by_xpath("//div[@class='alert alert-success']").text
    assert "Course has been deleted successfully" in message.strip()






# Validate Update Setting Time Functionality
def test_Validate_Update_Setting_Time_Admin():
    driver.get("http://15.236.43.203:8000/manage/time/")
    driver.find_element_by_xpath("//a[@class='btn btn-primary rounded-pill mt-3 btn-block']").click()
    heading = driver.find_element_by_xpath("//h3[@class='title']").text
    assert "Edit Registration Time" in heading.strip()

    driver.find_element_by_xpath("//input[@placeholder='starting date YYYY-MM-DD']").send_keys("randome text")
    driver.find_element_by_xpath("//input[@placeholder='Starting Time']").send_keys("randome text")
    driver.find_element_by_xpath("//input[@placeholder='Finishing Date YYYY-MM-DD']").send_keys("randome text")
    driver.find_element_by_xpath("//input[@placeholder='Finishing Time']").send_keys("randome text")
    driver.find_element_by_xpath("//button[contains(@class,'rounded-pill')]").click()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'starting_date')]/ul/li").text
    assert "Enter a valid date." in errormessage.strip()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'starting_time')]/ul/li").text
    assert "Enter a valid time." in errormessage.strip()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'finishing_date')]/ul/li").text
    assert "Enter a valid date." in errormessage.strip()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'finishing_time')]/ul/li").text
    assert "Enter a valid time." in errormessage.strip()

    driver.find_element_by_xpath("//input[@placeholder='starting date YYYY-MM-DD']").clear()
    driver.find_element_by_xpath("//input[@placeholder='Starting Time']").clear()
    driver.find_element_by_xpath("//input[@placeholder='Finishing Date YYYY-MM-DD']").clear()
    driver.find_element_by_xpath("//input[@placeholder='Finishing Time']").clear()


    driver.find_element_by_xpath("//input[@placeholder='starting date YYYY-MM-DD']").send_keys("2021-09-01")
    driver.find_element_by_xpath("//input[@placeholder='Starting Time']").send_keys("00:00:01")
    driver.find_element_by_xpath("//input[@placeholder='Finishing Date YYYY-MM-DD']").send_keys("2022-09-12")
    driver.find_element_by_xpath("//input[@placeholder='Finishing Time']").send_keys("00:00:02")
    driver.find_element_by_xpath("//button[contains(@class,'rounded-pill')]").click()

    message = driver.find_element_by_xpath("//h4[@class='timecolor']").text
    assert "midnight Sept. 1, 2021" in message.strip()
    message = driver.find_element_by_xpath("//h4[2]").text
    assert "midnight Sept. 12, 2022" in message.strip()



# Validate delete Setting Time Functionality
def test_Validate_Delete_Setting_Time_Admin():
    driver.get("http://15.236.43.203:8000/manage/time/")
    driver.find_element_by_xpath("//a[@class='btn btn-danger rounded-pill mt-3 btn-block']").click()
    driver.find_element_by_xpath("//a[@class='btn btn-primary rounded-pill btn-block']").click()
    driver.find_element_by_xpath("//a[@class='btn btn-danger rounded-pill mt-3 btn-block']").click()
    driver.find_element_by_xpath("//a[@class='btn btn-danger rounded-pill btn-block']").click()
    message = driver.find_element_by_xpath("//div[@class='alert alert-success']").text
    assert "Registration time cancelled" in message.strip()



# Validate Add Setting Time Functionality
def test_Validate_Add_Setting_Time_Admin():
    driver.get("http://15.236.43.203:8000/manage/settime/")
    heading = driver.find_element_by_xpath("//h3[@class='title']").text
    assert "Set Registration Time" in heading.strip()

    driver.find_element_by_xpath("//button[contains(@class,'rounded-pill')]").click()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'starting_date')]/ul/li").text
    assert "This field is required." in errormessage.strip()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'starting_time')]/ul/li").text
    assert "This field is required." in errormessage.strip()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'finishing_date')]/ul/li").text
    assert "This field is required." in errormessage.strip()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'finishing_time')]/ul/li").text
    assert "This field is required." in errormessage.strip()

    driver.find_element_by_xpath("//input[@placeholder='starting date YYYY-MM-DD']").send_keys("random text")
    driver.find_element_by_xpath("//input[@placeholder='Starting Time']").send_keys("random text")
    driver.find_element_by_xpath("//input[@placeholder='Finishing Date YYYY-MM-DD']").send_keys("random text")
    driver.find_element_by_xpath("//input[@placeholder='Finishing Time']").send_keys("randome text")
    driver.find_element_by_xpath("//button[contains(@class,'rounded-pill')]").click()

    errormessage = driver.find_element_by_xpath("//li[contains(text(),'starting_date')]/ul/li").text
    assert "Enter a valid date." in errormessage.strip()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'starting_time')]/ul/li").text
    assert "Enter a valid time." in errormessage.strip()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'finishing_date')]/ul/li").text
    assert "Enter a valid date." in errormessage.strip()
    errormessage = driver.find_element_by_xpath("//li[contains(text(),'finishing_time')]/ul/li").text
    assert "Enter a valid time." in errormessage.strip()
    driver.find_element_by_xpath("//input[@placeholder='starting date YYYY-MM-DD']").send_keys("2020-09-01")
    driver.find_element_by_xpath("//input[@placeholder='Starting Time']").send_keys("00:00:00")
    driver.find_element_by_xpath("//input[@placeholder='Finishing Date YYYY-MM-DD']").send_keys("2020-09-12")
    driver.find_element_by_xpath("//input[@placeholder='Finishing Time']").send_keys("00:00:00")
    driver.find_element_by_xpath("//button[contains(@class,'rounded-pill')]").click()

    message = driver.find_element_by_xpath("//h4[@class='timecolor']").text
    assert "midnight Sept. 1, 2020" in message.strip()
    message = driver.find_element_by_xpath("//h4[2]").text
    assert "midnight Sept. 12, 2020" in message.strip()

# Validate Wishlist Functionality
def test_Add_Wishlist_Admin():
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

# Validate Instructor Statistics Functionality, When
def test_Instructor_Statistics_Admin():
    driver.get("http://15.236.43.203:8000/instructors/statistics/")
    courseTest = driver.find_element_by_xpath("/html[1]/body[1]/main[1]/main[1]/div[1]/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[2]").text
    assert "Programming in C & Unix" in courseTest.strip()
    driver.find_element_by_xpath("//a[@class='btn btn-danger rounded-pill']").click()

    driver.find_element_by_xpath("//a[@class='btn btn-primary rounded-pill btn-block']").click()
    courseTest = driver.find_element_by_xpath("/html[1]/body[1]/main[1]/main[1]/div[1]/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[2]").text
    assert "Programming in C & Unix" in courseTest.strip()
    driver.find_element_by_xpath("//a[@class='btn btn-danger rounded-pill']").click()
    driver.find_element_by_xpath("//a[@class='btn btn-danger rounded-pill btn-block']").click()
    message = driver.find_element_by_xpath("(//h4)[1]").text
    assert "No instructors statistics" in message.strip()
    driver.close()