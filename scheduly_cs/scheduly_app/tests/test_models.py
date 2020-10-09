from django.test import TestCase
from scheduly_app.models import Instructor, Student, DateTimeInterval, Course, ElectiveCourse, Progress, UnpreferredLectureTime, Profile, Wishlist, Semester
from django.contrib.auth.models import User
from datetime import datetime


class TestModels(TestCase):
    def setUp(self):
        # creating a user object to assign it to the instructor user field when testing creating an instructor
        self.user1 = User.objects.create(
            username='someone1@test.com',
            password='abc12312q'
        )
        # creating a user object to assign it to the instructor user field when testing creating an student
        self.user2 = User.objects.create(
            username='someone2@.testcom',
            password='abc12312q'
        )

        self.instructor1 = Instructor.objects.create(
            is_admin=False,
            all_statistics_allowed=False,
            instructor_id=245678,
            fullname='instructor1',
            user= User.objects.create(
                username='someone3@.testcom',
                password='abc12312q'),
        )

    def test_create_Instructor(self):
        self.instructor1 = Instructor.objects.create(
            is_admin=False,
            all_statistics_allowed=False,
            instructor_id=2154475,
            fullname='Someone',
            user=self.user1,
        )

    def test_create_Student(self):
        Student.objects.create(
            student_id=222154475,
            fullname='Someone2',
            user=self.user2,
        )


    def test_create_DateTimeInterval(self):
        DateTimeInterval.objects.create(
            starting_date = datetime.strptime('2020-09-02', "%Y-%m-%d").date(),
            starting_time = datetime.strptime( "04:00:00", '%H:%M:%S').time(),
            finishing_date = datetime.strptime('2020-09-02', "%Y-%m-%d").date(),
            finishing_time = datetime.strptime( "16:00:00", '%H:%M:%S').time(),
        )

    def test_create_Profile(self):
        Profile.objects.create(
           user=self.user1, 
        )

    def test_create_Course(self):
        self.course1 = Course.objects.create(
            name = 'Calculus 1',
            number = '0410101',
            credits = 3,
 
        )
        # Adding the chosen by later.
        self.course1.chosen_by.add(self.instructor1)


    def test_create_Course(self):
        self.course2 = Course.objects.create(
            name = 'Calculus 2',
            number = '0410102',
            credits = 3,
 
        )
        # Adding the chosen by later.
        self.course2.chosen_by.add(self.instructor1)
        self.course2.prerequisite.add(
            Course.objects.create(
            name = 'Calculus 1',
            number = '0410101',
            credits = 3,
 
        ))


    def test_create_ElectiveCourse(self):
        self.elective_course1 = ElectiveCourse.objects.create(
            name = 'Technical Writting',
            number = '9988173',
            credits = 3,
            total_num_of_students = 1,
 
        )
        # Adding the chosen by later.
        self.elective_course1.chosen_by.add(self.instructor1)


    def test_create_Progress(self):
        Progress.objects.create(
           student = Student.objects.create(student_id=454567,fullname='Someone3',user=self.user2),
           course = Course.objects.create(name='Calculus 2', number="0410102", credits=3)
        )

    def test_create_Wishlist(self):
        Wishlist.objects.create(
            id=12345,
            studentID = Student.objects.create(student_id=454567,fullname='Someone4',user=self.user2),
            instructorID = Instructor.objects.create(instructor_id=450007,fullname='Someone5',user=self.user1),
            firstChoice = "1",
            secondChoice = "2",
            thirdChoice = "3",
            fourthChoice = "4",
            )

    def test_create_Semester(self):
        self.semester1 = Semester.objects.create(
            name="Fall",
            student= Student.objects.create(student_id=454567,fullname='Someone4',user=self.user2),
            )
        self.semester1.courses.add(
            Course.objects.create(name = 'Calculus 1',number = '0410101',credits = 3,)
            )

    def test_create_UnpreferredLectureTime(self):
        UnpreferredLectureTime.objects.create(
            days = "135",
            starting_time = datetime.strptime( "04:00:00", '%H:%M:%S').time(),
            finishing_time = datetime.strptime( "16:00:00", '%H:%M:%S').time(),
        )
