from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Instructor(models.Model):
    is_admin = models.BooleanField(default=False)
    all_statistics_allowed = models.BooleanField(default=False)
    instructor_id = models.PositiveIntegerField(unique=True)
    fullname = models.CharField(max_length=150)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    whishlist_courses = models.ManyToManyField(
        "Course", related_name="instructor_courses", blank=True)
    wishlist_elective_courses = models.ManyToManyField(
        "ElectiveCourse", related_name="instructor_elective_courses", blank=True)
    unpreferred_time1 = models.ForeignKey(
        "UnpreferredLectureTime", on_delete=models.CASCADE, related_name="unpreferred_time1", blank=True, null=True)
    unpreferred_time2 = models.ForeignKey(
        "UnpreferredLectureTime", on_delete=models.CASCADE, related_name="unpreferred_time2", blank=True, null=True)

    # Shows the name of the Instructor object in the admin site table instead of Instructor object id

    def __str__(self):
        return self.fullname


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')


class Student(models.Model):
    student_id = models.PositiveIntegerField(unique=True)
    fullname = models.CharField(max_length=150)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wishlist_elective_courses = models.ManyToManyField(
        "ElectiveCourse", related_name="student_elective_courses", blank=True)

    # Shows the name of the Student object in the admin site table instead of Student object id
    def __str__(self):
        return self.fullname


class DateTimeInterval(models.Model):
    starting_date = models.DateField()
    starting_time = models.TimeField()
    finishing_date = models.DateField()
    finishing_time = models.TimeField()


class Course(models.Model):
    name = models.CharField(max_length=150)
    number = models.CharField(max_length=12, unique=True, validators=[
        RegexValidator(r'^[0-9]*$', message="Course number must consists of numbers only")])
    prerequisite = models.ManyToManyField(
        'self', related_name='dependants', symmetrical=False, blank=True)
    credits = models.PositiveIntegerField(blank=False, default=3)
    chosen_by = models.ManyToManyField(
        "Instructor", related_name="courses_chosen_by", blank=True)

    # Shows the name of the Course object in the admin site table instead of Course object id
    def __str__(self):
        return self.name

    def is_available(self, user):
        return all(
            Progress.objects.filter(course=course, student__user=user).exists()
            for course in self.prerequisite.all()
        )

    def is_available_after(self, courses_completed):
        return all(
            course in courses_completed
            for course in self.prerequisite.all()
        )


class ElectiveCourse(models.Model):
    name = models.CharField(max_length=150)
    number = models.CharField(max_length=12, unique=True, validators=[
        RegexValidator(r'^[0-9]*$', message="Course number must consists of numbers only")])
    credits = models.PositiveIntegerField(blank=False, default=3)
    chosen_by = models.ManyToManyField(
        "Instructor", related_name="elective_courses_chosen_by", blank=True)
    total_num_of_students = models.PositiveIntegerField(
        default=0, blank=True, null=True)

    def __str__(self):
        return self.name


class Progress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Wishlist(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    studentID = models.ForeignKey(Student, on_delete=models.CASCADE)
    instructorID = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    firstChoice = models.CharField(max_length=150)
    secondChoice = models.CharField(max_length=150)
    thirdChoice = models.CharField(max_length=150)
    fourthChoice = models.CharField(max_length=150)

    def __str__(self):
        return self.id


class Semester(models.Model):
    name = models.CharField(max_length=20)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)
    # parent = models.ForeignKey('self', on_delete=models.CASCADE)


class UnpreferredLectureTime(models.Model):
    DAYS_CHOICES = (
        ('135', '135'),
        ('24', '24'),
    )
    days = models.CharField(blank=True, null=True,
                            max_length=10, choices=DAYS_CHOICES)
    starting_time = models.TimeField()
    finishing_time = models.TimeField()

    def __str__(self):
        return "From:{} To:{})".format(self.starting_time, self.finishing_time)
