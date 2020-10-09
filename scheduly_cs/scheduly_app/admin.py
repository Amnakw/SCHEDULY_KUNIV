from django.contrib import admin
from .models import Instructor, Student, DateTimeInterval, Course, ElectiveCourse, Profile, Progress, Wishlist, Semester

admin.site.register(Instructor)
admin.site.register(Student)
admin.site.register(DateTimeInterval)
admin.site.register(Course)
admin.site.register(ElectiveCourse)
admin.site.register(Profile)
admin.site.register(Progress)
admin.site.register(Semester)
admin.site.register(Wishlist)

