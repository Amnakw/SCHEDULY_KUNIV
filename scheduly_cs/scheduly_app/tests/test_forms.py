from django.test import TestCase

from scheduly_app.forms import (
    UserLogin, UserCreate, UserUpdate, AddUpdateStudent, AddUpdateInstructor,
    AddDateTimeInterval, AddCourse, AddElectiveCourse, ProgressFormSet
)


class TestForms(TestCase):
    def test_add_date_time_interval_form(self):
        starting_date = "2020-10-12"
        starting_time = "12:15:00"
        finishing_date = "2020-12-12"
        finishing_time = "15:15:00"
        data = {
            'starting_date': starting_date,
            'starting_time': starting_time,
            'finishing_date': finishing_date,
            'finishing_time': finishing_time,
        }

        form = AddDateTimeInterval(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_add_date_time_form(self):
        starting_date = "2020-10-12"
        starting_time = "12:15:00"
        data = {
            'starting_date': starting_date,
            'starting_time': starting_time,
        }
        form = AddDateTimeInterval(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_add_date_time_form_types_date(self):
        starting_date = "2020 12"
        starting_time = "12:15:00"
        finishing_date = "2020-12-12"
        finishing_time = "18:15:00"
        data = {
            'starting_date': starting_date,
            'starting_time': starting_time,
            'finishing_date': finishing_date,
            'finishing_time': finishing_time,
            'starting_time': starting_time,
        }

        form = AddDateTimeInterval(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_add_date_time_form_types_time(self):
        starting_date = "2020-10-12"
        starting_time = "12:15:00"
        finishing_date = "2020-12-12"
        finishing_time = "223"
        data = {
            'starting_date': starting_date,
            'starting_time': starting_time,
            'finishing_date': finishing_date,
            'finishing_time': finishing_time,
            'starting_time': starting_time,
        }

        form = AddDateTimeInterval(data=data)
        self.assertFalse(form.is_valid())

    def test_user_update_form(self):
        username = "user@usertest.com"
        password = "avfd124$"
        confirm_password = "avfd124$"

        data = {
            "username": username,
            "password": password,
            "confirm_password": confirm_password
        }

        form = UserUpdate(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_update_form(self):
        username = "user@usertest.com"
        password = "avfd124$"
        confirm_password = "avfd124$"

        data = {
            "username": username,
            "password": password,
        }

        form = UserUpdate(data=data)
        self.assertFalse(form.is_valid())

    def test_user_login_form(self):
        username = "user@usertest.com"
        password = "avfd124$"

        data = {
            "username": username,
            "password": password,
        }

        form = UserLogin(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_login_form(self):
        username = "user@usertest.com"
        password = "avfd124$"

        data = {
            "username": username,
            "password": "",
        }

        form = UserLogin(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_user_login_form_no_username(self):
        username = "user@usertest.com"
        password = "avfd124$"

        data = {
            "username": "",
            "password": password,
        }

        form = UserLogin(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_user_login_form_empty_fields(self):
        username = "user@usertest.com"
        password = "avfd124$"

        data = {
            "username": "",
            "password": "",
        }

        form = UserLogin(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_add_course_form_empty_fields(self):
        name = ""
        number = ""
        prerequisite = ""
        credits = ""
        chosen_by = ""

        data = {
            "name":  name,
            "number":  number,
            "prerequisite": prerequisite,
            "credits": credits,
            "chosen_by": chosen_by,
        }

        form = AddCourse(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_add_course_form_empty_name(self):
        name = ""
        number = "1234"
        credits = "3"

        data = {
            "name":  name,
            "number":  number,
            "credits": credits,
        }

        form = AddCourse(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_add_course_form_empty_credits(self):
        name = "test"
        number = "1234"
        credits = ""

        data = {
            "name":  name,
            "number":  number,
            "credits": credits,
        }

        form = AddCourse(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_add_course_form_empty_number(self):
        name = "test"
        number = ""
        credits = "2"

        data = {
            "name":  name,
            "number":  number,
            "credits": credits,
        }

        form = AddCourse(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_add_course_form_invalid_number(self):
        name = "test"
        number = "asv"
        credits = "2"

        data = {
            "name":  name,
            "number":  number,
            "credits": credits,
        }

        form = AddCourse(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_add_course_form_invalid_credits(self):
        name = "test"
        number = "023301"
        credits = "aq"

        data = {
            "name":  name,
            "number":  number,
            "credits": credits,
        }

        form = AddCourse(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_add_course_form_negative_credits(self):
        name = "test"
        number = "023301"
        credits = "-3"

        data = {
            "name":  name,
            "number":  number,
            "credits": credits,
        }

        form = AddCourse(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_add_course_form(self):
        name = "C++"
        number = "03210100"
        credits = "3"

        data = {
            "name":  name,
            "number":  number,
            "credits": credits,
        }

        form = AddCourse(data=data)
        self.assertTrue(form.is_valid())

        # testing ElectiveCourse form
    def test_invalid_add_elective_course_form_empty_fields(self):
        name = ""
        number = ""
        prerequisite = ""
        credits = ""
        chosen_by = ""

        data = {
            "name":  name,
            "number":  number,
            "prerequisite": prerequisite,
            "credits": credits,
            "chosen_by": chosen_by,
        }

        form = AddElectiveCourse(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_add_elective_course_form_empty_name(self):
        name = ""
        number = "1234"
        credits = "3"

        data = {
            "name":  name,
            "number":  number,
            "credits": credits,
        }

        form = AddElectiveCourse(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_add_elective_course_form_empty_credits(self):
        name = "test"
        number = "1234"
        credits = ""

        data = {
            "name":  name,
            "number":  number,
            "credits": credits,
        }

        form = AddElectiveCourse(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_add_elective_course_form_empty_number(self):
        name = "test"
        number = ""
        credits = "2"

        data = {
            "name":  name,
            "number":  number,
            "credits": credits,
        }

        form = AddElectiveCourse(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_add_elective_course_form_invalid_number(self):
        name = "test"
        number = "asv"
        credits = "2"

        data = {
            "name":  name,
            "number":  number,
            "credits": credits,
        }

        form = AddElectiveCourse(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_add_elective_course_form_invalid_credits(self):
        name = "test"
        number = "023301"
        credits = "aq"

        data = {
            "name":  name,
            "number":  number,
            "credits": credits,
        }

        form = AddElectiveCourse(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_add_elective_course_form_negative_credits(self):
        name = "test"
        number = "023301"
        credits = "-3"

        data = {
            "name":  name,
            "number":  number,
            "credits": credits,
        }

        form = AddElectiveCourse(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_add_elective_course_form(self):
        name = "C++"
        number = "03210100"
        credits = "3"

        data = {
            "name":  name,
            "number":  number,
            "credits": credits,
        }

        form = AddElectiveCourse(data=data)
        self.assertTrue(form.is_valid())

    def test_valid_add_elective_course_form_with_total_num_of_students(self):
        name = "C++"
        number = "03210100"
        credits = "3"
        total_num_of_students = "10"

        data = {
            "name":  name,
            "number":  number,
            "credits": credits,
            "total_num_of_students": total_num_of_students,
        }

        form = AddElectiveCourse(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_add_elective_course_form_with_total_num_of_students(self):
        name = "C++"
        number = "03210100"
        credits = "3"
        total_num_of_students = "aa"

        data = {
            "name":  name,
            "number":  number,
            "credits": credits,
            "total_num_of_students": total_num_of_students,
        }

        form = AddElectiveCourse(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_add_elective_course_form_with_total_num_of_students_negative(self):
        name = "C++"
        number = "03210100"
        credits = "3"
        total_num_of_students = "-30"

        data = {
            "name":  name,
            "number":  number,
            "credits": credits,
            "total_num_of_students": total_num_of_students,
        }

        form = AddElectiveCourse(data=data)
        self.assertFalse(form.is_valid())
