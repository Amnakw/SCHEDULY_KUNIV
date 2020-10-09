
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from scheduly_app.views import ( user_login, user_logout, home,
     add_instructor, add_student, edit_major_sheet, add_course, add_elective_course, edit_course, delete_course, delete_course_confirmation,
     list_to_edit, edit_instructor, help,
     edit_student, list_to_delete, delete_user, delete_user_confirmation, setting_time,
     list_time, update_time, delete_time, delete_time_confirmation, no_access, user_profile, instructor_wishlist, instructor_wishlist_settime,
     instructors_statistics, reset_instructors_statistics,reset_instructors_statistics_confirmation, candidate_info, progress, plan,
     student_wishlist, students_statistics, reset_students_statistics, reset_students_statistics_confirmation)

urlpatterns = [
    path('help/', help, name='help'),
    path('admin/', admin.site.urls),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', home, name='home'),
    path('noaccess/', no_access ,name='no-access'),
    path('profile/', user_profile, name='user-profile'),

    # admin instructor urls:
    path('manage/add/instructor/', add_instructor, name='add-instructor'),
    path('manage/add/student/', add_student, name='add-student'),
    path('manage/edit/major_sheet/', edit_major_sheet, name='edit-major-sheet'),
    path('manage/edit/major_sheet/add/course/', add_course, name='add-course'),
    path('manage/edit/major_sheet/add/elective/course/', add_elective_course, name='add-elective-course'),
    path('manage/edit/major_sheet/edit/course/<str:course_number>/', edit_course, name='edit-course'),
    path('manage/edit/major_sheet/delete/course/<str:course_number>/', delete_course, name='delete-course'),
    path('manage/edit/major_sheet/delete/course/confirmation/<str:course_number>/', delete_course_confirmation, name="delete-course-confirmation"),

    path('manage/edit/users/', list_to_edit, name='edit-users'),
    path('manage/edit/instructor/<int:user_id>/', edit_instructor, name='edit-instructor'),
    path('manage/edit/student/<int:user_id>/', edit_student, name='edit-student'),

    path('delete/user/<int:user_id>/', delete_user, name='delete-user'),
    path('delete/user/confirmation/<int:user_id>/', delete_user_confirmation, name='delete-user-confirmation'),
    path('manage/delete/users/', list_to_delete, name='delete-users'),

    path('manage/settime/', setting_time ,name='setting-time'),
    path('manage/time/', list_time ,name='time'),
    path('manage/edit/time/<int:time_id>/', update_time ,name='edit-time'),
    path('manage/delete/time/<int:time_id>/', delete_time ,name='delete-time'),
    path('manage/delete/time/confirmation/<int:time_id>/', delete_time_confirmation ,name='delete-time-confirmation'),

    path('instructor/whishlist/', instructor_wishlist, name='instructor-wishlist' ),
    path('instructor/wishlist/settime/', instructor_wishlist_settime, name='instructor-wishlist-settime'),
    path('instructors/statistics/', instructors_statistics, name='instructors-statistics' ),
    path('candidate/info/<str:course_number>/', candidate_info, name='candidate-info' ),
    path('instructors/statistics/reset/' , reset_instructors_statistics, name='reset-instructors-statistics' ),
    path('instructors/statistics/reset/confirmation/' , reset_instructors_statistics_confirmation, name='reset-instructors-statistics-confirmation' ),

    # student urls:
    path('student/progress/', progress, name='student-progress'),
    path('student/plan/', plan, name='student-plan'),
    path('student/wishlist/', student_wishlist, name='student-wishlist'),
    path('students/statistics/', students_statistics, name='students-statistics'),
    path('students/statistics/reset/' , reset_students_statistics, name='reset-students-statistics' ),
    path('students/statistics/reset/confirmation' , reset_students_statistics_confirmation, name='reset-students-statistics-confirmation' ),


]

# Serving static files during development
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
