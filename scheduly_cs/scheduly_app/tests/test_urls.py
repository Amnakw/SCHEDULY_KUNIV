from django.test import TestCase
from django.urls import reverse, resolve
from scheduly_app.views import (user_login, user_logout, home, no_access, user_profile,
                                add_instructor, add_student, edit_major_sheet, add_course, add_elective_course, edit_course, 
                                edit_course, delete_course, delete_course_confirmation,
                                list_to_edit, edit_instructor, edit_student, 
                                list_to_delete, delete_user, delete_user_confirmation,
                                setting_time, list_time, update_time, 
                                delete_time, delete_time_confirmation,
                                instructor_wishlist, instructor_wishlist_settime,
                                instructors_statistics, candidate_info, reset_instructors_statistics, reset_instructors_statistics_confirmation,
                                progress, plan,student_wishlist, students_statistics, reset_students_statistics,
                                reset_students_statistics_confirmation)


class TestUrls(TestCase):
    # main tests
    def test_user_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, user_login)

    def test_user_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, user_logout)

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_user_profile_url_is_resolved(self):
        url = reverse('user-profile')
        self.assertEquals(resolve(url).func,user_profile)

    def test_no_access_url_is_resolved(self):
        url = reverse('no-access')
        self.assertEquals(resolve(url).func, no_access)



    # admin instructor tests
    def test_add_instructor_url_is_resolved(self):
        url = reverse('add-instructor')
        self.assertEquals(resolve(url).func, add_instructor)

    def test_add_student_url_is_resolved(self):
        url = reverse('add-student')
        self.assertEquals(resolve(url).func, add_student)

    def test_edit_major_sheet_url_is_resolved(self):
        url = reverse('edit-major-sheet')
        self.assertEquals(resolve(url).func, edit_major_sheet)

    def test_add_course_url_is_resolved(self):
        url = reverse('add-course')
        self.assertEquals(resolve(url).func, add_course)

    def test_add_elective_course_url_is_resolved(self):
        url = reverse('add-elective-course')
        self.assertEquals(resolve(url).func, add_elective_course)

    def test_edit_course_url_is_resolved(self):
        url = reverse('edit-course', args=['2'])
        self.assertEquals(resolve(url).func, edit_course)

    def test_delete_course_url_is_resolved(self):
        url = reverse('delete-course', args=['2'])
        self.assertEquals(resolve(url).func, delete_course)

    def test_delete_course_confirmation_url_is_resolved(self):
        url = reverse('delete-course-confirmation', args=['2'])
        self.assertEquals(resolve(url).func, delete_course_confirmation)



    # edit users tests
    def test_list_to_edit_url_is_resolved(self):
        url = reverse('edit-users')
        self.assertEquals(resolve(url).func, list_to_edit)

    def test_edit_instructor_url_is_resolved(self):
        url = reverse('edit-instructor', args=['1'])
        self.assertEquals(resolve(url).func, edit_instructor)

    def test_edit_student_url_is_resolved(self):
        url = reverse('edit-student', args=['1'])
        self.assertEquals(resolve(url).func, edit_student)



    # delete users tests
    def test_delete_user_url_is_resolved(self):
        url = reverse('delete-user', args=['1'])
        self.assertEquals(resolve(url).func, delete_user)

    def test_delete_user_confirmation_url_is_resolved(self):
        url = reverse('delete-user-confirmation', args=['1'])
        self.assertEquals(resolve(url).func, delete_user_confirmation)

    def test_delete_users_url_is_resolved(self):
        url = reverse('delete-users')
        self.assertEquals(resolve(url).func, list_to_delete)



    # setting time tests
    def test_setting_time_url_is_resolved(self):
        url = reverse('setting-time')
        self.assertEquals(resolve(url).func, setting_time)

    def test_list_time_url_is_resolved(self):
        url = reverse('time')
        self.assertEquals(resolve(url).func, list_time)

    def test_update_time_url_is_resolved(self):
        url = reverse('edit-time', args=['1'])
        self.assertEquals(resolve(url).func, update_time)

    def test_delete_time_url_is_resolved(self):
        url = reverse('delete-time', args=['1'])
        self.assertEquals(resolve(url).func, delete_time)

    def test_delete_time_confirmation_url_is_resolved(self):
        url = reverse('delete-time-confirmation', args=['1'])
        self.assertEquals(resolve(url).func, delete_time_confirmation)



    # instructor tests
    def test_instructor_wishlist_url_is_resolved(self):
        url = reverse('instructor-wishlist')
        self.assertEquals(resolve(url).func, instructor_wishlist)

    def test_instructor_wishlist_settime_url_is_resolved(self):
        url = reverse('instructor-wishlist-settime')
        self.assertEquals(resolve(url).func, instructor_wishlist_settime)

    def test_instructors_statistics_url_is_resolved(self):
        url = reverse('instructors-statistics')
        self.assertEquals(resolve(url).func, instructors_statistics)

    def test_candidate_info_url_is_resolved(self):
        url = reverse('candidate-info', args=['1'])
        self.assertEquals(resolve(url).func, candidate_info)

    def test_reset_instructors_statistics_url_is_resolved(self):
        url = reverse('reset-instructors-statistics')
        self.assertEquals(resolve(url).func, reset_instructors_statistics)

    def test_reset_instructors_statistics_confirmation_url_is_resolved(self):
        url = reverse('reset-instructors-statistics-confirmation')
        self.assertEquals(resolve(url).func, reset_instructors_statistics_confirmation)



    # student tests
    def test_progress_url_is_resolved(self):
        url = reverse('student-progress')
        self.assertEquals(resolve(url).func, progress)

    def test_plan_url_is_resolved(self):
        url = reverse('student-plan')
        self.assertEquals(resolve(url).func, plan)

    def test_student_wishlist_url_is_resolved(self):
        url = reverse('student-wishlist')
        self.assertEquals(resolve(url).func, student_wishlist)

    def test_students_statistics_url_is_resolved(self):
        url = reverse('students-statistics')
        self.assertEquals(resolve(url).func, students_statistics)

    def test_reset_students_statistics_url_is_resolved(self):
        url = reverse('reset-students-statistics')
        self.assertEquals(resolve(url).func, reset_students_statistics)

    def test_reset_students_statistics_confirmation_url_is_resolved(self):
        url = reverse('reset-students-statistics-confirmation')
        self.assertEquals(resolve(url).func, reset_students_statistics_confirmation)