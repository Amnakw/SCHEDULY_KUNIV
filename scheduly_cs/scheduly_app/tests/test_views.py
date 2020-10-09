from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.http import response
from django.contrib import auth
from scheduly_app.models import Course, ElectiveCourse, Instructor, Student
from scheduly_app import views
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_user_login_GET(self):
        response = self.client.get(reverse('login'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_user_logout_GET(self):
        response = self.client.get(reverse('logout'))

        self.assertEquals(response.status_code, 302)

    def test_home_GET(self):
        response = self.client.get(reverse('home'))

        self.assertEquals(response.status_code, 302)

    # def test_list_to_delete_GET(self):
    # 	status_code = 200
    # 	view_class = views.list_to_delete

    # 	req = RequestFactory().get('manage/delete/users/')
    # 	req.user = AnonymousUser()
    # 	resp = views.list_to_delete(req, *[], **{})
    # 	self.assertEqual(resp.status_code, 200)
    # 	response = self.client.get(reverse('delete-users'))

    # 	self.assertEquals(response.status_code, 200)
    # 	self.assertTemplateUsed(response, 'admin/admin_delete.html')

    # def test_list_time_GET(self):
    # 	user = auth.get_user(self.client)

    # 	if user.is_anonymous():
    # 		response = self.client.get(reverse('login'))
    # 		self.assertEquals(response.status_code, 302)
    # 	else:
    # 		response = self.client.get(reverse('time'))
    # 		self.assertEquals(response.status_code, 200)
    # 		self.assertTemplateUsed(response, 'time.html')

    # def test_edit_major_sheet_GET(self):
    # 	response = self.client.get(reverse('edit-major-sheet'))

    # 	self.assertEquals(response.status_code, 200)
    # 	self.assertTemplateUsed(response, 'admin/admin_edit_major_sheet.html')

    # def test_add_course_GET(self):
    # 	response = self.client.get(reverse('add-course'))

    # 	self.assertEquals(response.status_code, 200)
    # 	self.assertTemplateUsed(response, 'admin/admin_add_course.html')


class TestStudentViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.instructor_user1 = User.objects.create(
            username='someone1@test.com',
            password='abc12312q'
        )
        self.instructor_user1.set_password(self.instructor_user1.password)
        self.instructor_user1.save()
        self.instructor1 = Instructor.objects.create(
            is_admin=True,
            all_statistics_allowed=False,
            instructor_id=2154475,
            fullname='Someone',
            user=self.instructor_user1,
        )

        self.instructor_user2 = User.objects.create(
            username='someone2@test.com',
            password='abc12312q'
        )
        self.instructor_user2.set_password(self.instructor_user2.password)
        self.instructor_user2.save()
        self.instructor2 = Instructor.objects.create(
            is_admin=False,
            all_statistics_allowed=False,
            instructor_id=2154575,
            fullname='Someone2',
            user=self.instructor_user2,
        )

        # creating a user object to assign it to the user field when testing creating a student
        self.student1 = User.objects.create(
            username='someone3@test.com',
            password='abc12312q'
        )
        self.student1.set_password(self.student1.password)
        self.student1.save()

        self.student_data_1 = {
            "student_id": 222154475,
            "fullname": 'Someone3',
            "user": self.student1,
        }

        self.student2 = User.objects.create(
            username='someone4@test.com',
            password='abc12312q'
        )
        self.student2.set_password(self.student2.password)
        self.student2.save()

        self.student_data_2 = {
            "student_id": 2221526760,
            "fullname": 'Someone4',
            "user": self.student2,
        }

    def test_add_student_view(self):
        create_url = reverse("add-student")
        # instructor is an admin case:
        request = self.factory.post(create_url, self.student_data_1)
        request.user = self.instructor1.user
        """When you use RequestFactory only the view runs,
        not the middleware. That why we need first to annotate
        it with a session and then a messages.  """
        # Annotate a request object with a session
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        # Annotate a request object with a messages
        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()

        response = views.add_student(request)
        self.assertEqual(response.status_code, 200)
