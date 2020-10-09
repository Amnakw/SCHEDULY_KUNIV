from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import Instructor, Student, DateTimeInterval, Course, ElectiveCourse, Progress, UnpreferredLectureTime
from .forms import (
    UserLogin, UserCreate, UserUpdate, AddUpdateStudent, AddUpdateInstructor,
    AddDateTimeInterval, AddCourse, AddElectiveCourse, UpdateCourse, ProgressFormSet
)
from django.db.models import Q
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from itertools import chain
import datetime
# User Authentication

def help(request):
    return render(request, 'help.html')

def user_login(request):
    if not request.user.is_anonymous:
        return redirect("home")

    form = UserLogin()
    if request.method == 'POST':
        form = UserLogin(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            print(username, password)

            auth_user = authenticate(username=username, password=password)
            print(auth_user)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('home')
            messages.warning(
                request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)

    context = {
        "form": form
    }
    return render(request, 'login.html', context)

def user_logout(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'home.html')

def add_instructor(request):
    if request.user.is_anonymous:
        return redirect('login')

     # checking of the user who is attempting to add a user is an instructor
     # who is an admin, if he is not an admin he will be redirected to no access page
    instructor_obj = Instructor.objects.get(user=request.user)

    if instructor_obj.is_admin == False:
        return redirect('no-access')

    # else if the user is an admin instructor the adding a user is allowed
    create_user_form = UserCreate()
    instructor_form = AddUpdateInstructor()

    if request.method == 'POST':
        create_user_form = UserCreate(request.POST)
        instructor_form = AddUpdateInstructor(request.POST)

        if create_user_form.is_valid() and instructor_form.is_valid():
            creadeted_user = create_user_form.save(commit=False)
            creadeted_user.set_password(creadeted_user.password)
            creadeted_user.save()

            instructor = instructor_form.save(commit=False)
            instructor.user = creadeted_user
            instructor_form.save()
            messages.success(request, "The user was created successfuly")
            return redirect('add-instructor')

        # if form isn't valid:
        messages.warning(request, create_user_form.errors)
        messages.warning(request, instructor_form.errors)

    context = {
        'create_user_form': create_user_form,
        'instructor_form': instructor_form,

    }
    return render(request, 'admin/admin_add_instructor.html', context)


def add_student(request):
    if request.user.is_anonymous:
        return redirect('login')

     # checking of the user who is attempting to add a user is an instructor
     # who is an admin, if he is not an admin he will be redirected to no access page
    instructor_obj = Instructor.objects.get(user=request.user)

    if instructor_obj.is_admin == False:
        return redirect('no-access')

    # else if the user is an admin instructor the adding a user is allowed
    create_user_form = UserCreate()
    student_form = AddUpdateStudent()

    if request.method == 'POST':
        create_user_form = UserCreate(request.POST)
        student_form = AddUpdateStudent(request.POST)

        if create_user_form.is_valid() and student_form.is_valid():
            creadeted_user = create_user_form.save(commit=False)
            creadeted_user.set_password(creadeted_user.password)
            creadeted_user.save()

            student = student_form.save(commit=False)
            student.user = creadeted_user
            student_form.save()
            messages.success(request, "The user was created successfuly")
            return redirect('add-student')

        # if form isn't valid:
        messages.warning(request, create_user_form.errors)
        messages.warning(request, student_form.errors)

    context = {
        'create_user_form': create_user_form,
        'student_form': student_form,

    }
    return render(request, 'admin/admin_add_student.html', context)


# used to list and search users to edit a user
def list_to_edit(request):
    if request.user.is_anonymous:
        return redirect('login')

     # checking of the user who is attempting to update a user is an instructor
     # who is an admin, if he is not an admin he will be redirected to no access page
    instructor_obj = Instructor.objects.get(user=request.user)

    if instructor_obj.is_admin == False:
        return redirect('no-access')
    students = Student.objects.all()
    instructors = Instructor.objects.all()

    # if search is used filter students and instructors
    query = request.GET.get('q')

    if query:
        students = students.filter(
            Q(user__username__icontains=query) |
            Q(fullname__icontains=query) |
            Q(student_id__icontains=query)
        ).distinct()

        instructors = instructors.filter(
            Q(user__username__icontains=query) |
            Q(fullname__icontains=query) |
            Q(instructor_id__icontains=query)
        ).distinct()

    context = {
        'students_list': students,
        'instructors_list': instructors,
    }
    return render(request, 'admin/edit_users.html', context)


# used to edit instructors
def edit_instructor(request, user_id):
    if request.user.is_anonymous:
        return redirect('login')

     # checking of the user who is attempting to add a user is an instructor
     # who is an admin, if he is not an admin he will be redirected to no access page
    instructor_obj = Instructor.objects.get(user=request.user)

    if instructor_obj.is_admin == False:
        return redirect('no-access')

    # else if the user is an admin instructor the updating a user is allowed
    instructor = Instructor.objects.get(id=user_id)
    instructor_form = AddUpdateInstructor(instance=instructor)

    if request.method == 'POST':
        instructor_form = AddUpdateInstructor(
            request.POST, instance=instructor)

        if instructor_form.is_valid():
            instructor_form.save()
            messages.success(request, "The user was updated successfuly")
            return redirect('edit-users')

        # if form isn't valid:
        messages.warning(request, instructor_form.errors)

    context = {
        'instructor_form': instructor_form,
        'instructor': instructor,
    }
    return render(request, 'admin/edit_instructor.html', context)


# used to edit student
def edit_student(request, user_id):
    if request.user.is_anonymous:
        return redirect('login')

     # checking of the user who is attempting to add a user is an instructor
     # who is an admin, if he is not an admin he will be redirected to no access page
    instructor_obj = Instructor.objects.get(user=request.user)

    if instructor_obj.is_admin == False:
        return redirect('no-access')

    # else if the user is an admin instructor the updating a user is allowed
    student = Student.objects.get(id=user_id)
    student_form = AddUpdateStudent(instance=student)

    if request.method == 'POST':
        student_form = AddUpdateStudent(request.POST, instance=student)

        if student_form.is_valid():
            student_form.save()
            messages.success(request, "The user was updated successfuly")
            print("student_form", student_form)
            return redirect('edit-users')

        # if form isn't valid:
        messages.warning(request, student_form.errors)

    context = {
        'student_form': student_form,
        'student': student,
    }
    return render(request, 'admin/edit_student.html', context)


# used to list and search users to delete a user
def list_to_delete(request):
    if request.user.is_anonymous:
        return redirect('login')

     # checking of the user who is attempting to delete a user is an instructor
     # who is an admin, if he is not an admin he will be redirected to no access page
    instructor_obj = Instructor.objects.get(user=request.user)

    if instructor_obj.is_admin == False:
        return redirect('no-access')
    students = Student.objects.all()
    instructors = Instructor.objects.all()

    # if search is used filter students and instructors
    query = request.GET.get('q')

    if query:
        students = students.filter(
            Q(user__username__icontains=query) |
            Q(fullname__icontains=query) |
            Q(student_id__icontains=query)
        ).distinct()

        instructors = instructors.filter(
            Q(user__username__icontains=query) |
            Q(fullname__icontains=query) |
            Q(instructor_id__icontains=query)
        ).distinct()

    context = {
        'students_list': students,
        'instructors_list': instructors,
    }
    return render(request, 'admin/admin_delete.html', context)


# used to delete a user using user_id
def delete_user(request, user_id):
    if request.user.is_anonymous:
        return redirect('login')

     # checking of the user who is attempting to add a user is an instructor
     # who is an admin, if he is not an admin he will be redirected to no access page
    instructor_obj = Instructor.objects.get(user=request.user)

    if instructor_obj.is_admin == False:
        return redirect('no-access')

    # else if the user is an admin instructor the deleting a user is allowed
    # to combin deleting students and instructors using the same function

    # filter instructors and students if the passed user_id belonges to an instructor or student
    try:
        instructor = Instructor.objects.get(instructor_id=user_id)
        if instructor:
            instructor.user.delete()
            instructor.delete()
    except ObjectDoesNotExist:
        pass

    try:
        student = Student.objects.get(student_id=user_id)
        if student:
            student.user.delete()
            student.delete()
    except ObjectDoesNotExist:
        pass

    messages.success(request, 'User deleted')
    return redirect("delete-users")


def delete_user_confirmation(request, user_id):
    if request.user.is_anonymous:
        return redirect('login')
    context = {
        'user_id': user_id
    }
    return render(request, "admin/delete_user_confirmation.html", context)


# used to send emails to users it will be called inside
def send_email(email_subject, email_body):
    email_from = settings.EMAIL_HOST_USER
    # to get the emails of the users as email recipients
    instructors = Instructor.objects.all()
    students = Student.objects.all()
    send_to = []

    for instructor in instructors:
        send_to.append(instructor.user.username)
        # recipients = zip(instructor.user.first_name, instructor.user.username)

    for student in students:
        send_to.append(student.user.username)

        # recipients = zip(student.user.first_name, student.user.username)
        print("TYPE", type(student.user.username))

    send_mail(
        email_subject,
        email_body,
        email_from,
        send_to,
       
        fail_silently=False,
    )
    # msg = EmailMessage('Request Callback',
    #                    email_body, to=to)
    # msg.send()


# setting_time and update_time and delete_time functions
def setting_time(request):
    if request.user.is_anonymous:
        return redirect('login')

     # checking of the user who is attempting to add a user is an instructor
     # who is an admin, if he is not an admin he will be redirected to no access page
    instructor_obj = Instructor.objects.get(user=request.user)

    if instructor_obj.is_admin == False:
        return redirect('no-access')

    # If there is a registration time redirect to setting time list
    registration_time = DateTimeInterval.objects.all()

    if registration_time:
        return redirect('time')

    # else if the user is an admin instructor, setting the time is allowed
    date_time_form = AddDateTimeInterval()
    if request.method == 'POST':
        date_time_form = AddDateTimeInterval(request.POST)

        if date_time_form.is_valid():
            # getting the date and time values from the form

            starting_time = date_time_form.cleaned_data['starting_time']
            starting_date = date_time_form.cleaned_data['starting_date']
            finishing_time = date_time_form.cleaned_data['finishing_time']
            finishing_date = date_time_form.cleaned_data['finishing_date']

            if starting_date > finishing_date or starting_time > finishing_time:
                messages.warning(
                    request, "Incorrect values of days or times! Check again")
            else:
                date_time_form.save()
                messages.success(request, "The time was set successfuly")
                email_subject = "Scheduly Wishlist Registration Reminder"
                message_body = "Your next registration period starts on  {} - {} and ends on  {} - {}. ".format(
                    starting_date, starting_time, finishing_date, finishing_time)
                # Send email
                send_email(email_subject, message_body)

                return redirect('setting-time')

        # else if form isn't valid:
        messages.warning(request, date_time_form.errors)

    context = {
        'date_time_form': date_time_form,
    }
    return render(request, 'setting_time.html', context)


def list_time(request):
    if request.user.is_anonymous:
        return redirect('login')

     # checking of the user who is attempting to add a user is an instructor
     # who is an admin, if he is not an admin he will be redirected to no access page
    instructor_obj = Instructor.objects.get(user=request.user)

    if instructor_obj.is_admin == False:
        return redirect('no-access')
    # else if the user is the admin, show the page
    registration_times = DateTimeInterval.objects.all()

    context = {
        'registration_times': registration_times,
    }
    return render(request, 'time.html', context)


def delete_time(request, time_id):
    if request.user.is_anonymous:
        return redirect('login')

     # checking of the user who is attempting to add a user is an instructor
     # who is an admin, if he is not an admin he will be redirected to no access page
    instructor_obj = Instructor.objects.get(user=request.user)

    if instructor_obj.is_admin == False:
        return redirect('no-access')

    # else if user is admin allow delete
    time_to_delete = DateTimeInterval.objects.get(id=time_id)
    time_to_delete.delete()

    messages.success(request, 'Registration time cancelled')
    return redirect("home")


def delete_time_confirmation(request, time_id):
    if request.user.is_anonymous:
        return redirect('login')
    context = {
        'time_id': time_id
    }
    return render(request, "admin/delete_time_confirmation.html", context)


def update_time(request, time_id):
    if request.user.is_anonymous:
        return redirect('login')

     # checking of the user who is attempting to add a user is an instructor
     # who is an admin, if he is not an admin he will be redirected to no access page
    instructor_obj = Instructor.objects.get(user=request.user)

    if instructor_obj.is_admin == False:
        return redirect('no-access')

    # else if user is admin allow update
    time_to_update = DateTimeInterval.objects.get(id=time_id)
    date_time_form = AddDateTimeInterval(instance=time_to_update)

    if request.method == "POST":
        date_time_form = AddDateTimeInterval(
            request.POST, instance=time_to_update)
        if date_time_form.is_valid():
            # getting the date and time values from the form
            starting_time = date_time_form.cleaned_data['starting_time']
            starting_date = date_time_form.cleaned_data['starting_date']
            finishing_time = date_time_form.cleaned_data['finishing_time']
            finishing_date = date_time_form.cleaned_data['finishing_date']

            if starting_date > finishing_date or starting_time > finishing_time:
                messages.warning(
                    request, "Incorrect values of days or times! Check again")
            else:
                date_time_form.save()
                messages.success(request, "The time was set successfuly")

                email_subject = "Scheduly Wishlist Registration Changed"
                message_body = "Your next registration period starts on  {} - {} and ends on  {} - {}. ".format(
                    starting_date, starting_time, finishing_date, finishing_time)
                # Send email
                send_email(email_subject, message_body)
                return redirect("time")

        # else if form isn't valid:
        messages.warning(request, date_time_form.errors)

    context = {
        "date_time_form": date_time_form,
        "time": time_to_update
    }
    return render(request, 'admin/edit_registration_time.html', context)


def no_access(request):
    return render(request, 'no_access.html')


def user_profile(request):
    if request.user.is_anonymous:
        return redirect('login')

    if request.method == "GET":
        return render(request, 'profile.html', context={'user': request.user})

    elif request.method == "POST":
        form = UserUpdate(request.POST, instance=request.user)
        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
            request.user.username = form.cleaned_data['username']
            request.user.set_password(form.cleaned_data['password'])
            request.user.save()
            messages.success(request, "Profile has been updated successfully!")
            return redirect('home')
        print("form.cleaned_data['password']", form.cleaned_data['password'])
        print("form.cleaned_data['confirm_password']",
              form.cleaned_data['confirm_password'])
        if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
            messages.warning(
                request, "password and confirm password do not match!")

        messages.warning(request, form.errors)

        return render(request, 'profile.html', context={'user': request.user})


def edit_major_sheet(request):
    if request.user.is_anonymous:
        return redirect('login')

     # checking of the user who is attempting to add a user is an instructor
     # who is an admin, if he is not an admin he will be redirected to no access page
    instructor_obj = Instructor.objects.get(user=request.user)

    if instructor_obj.is_admin == False:
        return redirect('no-access')

    courses = Course.objects.all().exclude(number='0410101').exclude(
        number='0410111').exclude(number='0410102').exclude(number='0410211').order_by('number')
    electives = ElectiveCourse.objects.all()
    all_courses = chain(courses, electives)

    # if search is used filter Courses
    query = request.GET.get('q')

    if query:
        try:
            courses = courses.filter(
                Q(number__icontains=query) |
                Q(name__icontains=query)).distinct()
            if courses:
                all_courses = courses
        except ObjectDoesNotExist:
            pass

        try:
            electives = electives.filter(
                Q(number__icontains=query) |
                Q(name__icontains=query)).distinct()
            if electives:
                all_courses = electives
        except ObjectDoesNotExist:
            pass

    context = {
        'courses': all_courses,
    }
    return render(request, 'admin/admin_edit_major_sheet.html', context)


def add_course(request):
    if request.user.is_anonymous:
        return redirect('login')

     # checking of the user who is attempting to add a user is an instructor
     # who is an admin, if he is not an admin he will be redirected to no access page
    instructor_obj = Instructor.objects.get(user=request.user)

    if instructor_obj.is_admin == False:
        return redirect('no-access')

    # else if the user is an admin instructor the adding a course is allowed
    course_form = AddCourse()
    # passing all courses so the user can select prerequisite
    courses = Course.objects.all().exclude(number='0410101').exclude(
        number='0410111').exclude(number='0410102').exclude(number='0410211').order_by('number')
    electives = ElectiveCourse.objects.all()
    all_courses = chain(courses, electives)

    if request.method == 'POST':
        course_form = AddCourse(request.POST)
        print("request.POST.items()", request.POST.items())

        if course_form.is_valid():
            student = course_form.save(commit=False)
            course_form.save()
            messages.success(request, "The course was created successfuly")
            return render(request, 'admin/admin_edit_major_sheet.html', context={"courses": all_courses})

        # if form isn't valid:
        messages.warning(request, course_form.errors)

    context = {
        'courses': courses,
        'course_form': course_form,

    }
    return render(request, 'admin/admin_add_course.html', context)


def add_elective_course(request):
    if request.user.is_anonymous:
        return redirect('login')

     # checking of the user who is attempting to add a user is an instructor
     # who is an admin, if he is not an admin he will be redirected to no access page
    instructor_obj = Instructor.objects.get(user=request.user)

    if instructor_obj.is_admin == False:
        return redirect('no-access')

    # else if the user is an admin instructor the adding a course is allowed
    elective_course_form = AddElectiveCourse()
    # passing all courses so the user can select prerequisite
    courses = Course.objects.all()
    electives = ElectiveCourse.objects.all()
    all_courses = chain(courses, electives)

    if request.method == 'POST':
        elective_course_form = AddElectiveCourse(request.POST)
        print("request.POST.items()", request.POST.items())

        if elective_course_form.is_valid():
            student = elective_course_form.save(commit=False)
            elective_course_form.save()
            messages.success(request, "The course was created successfuly")
            return render(request, 'admin/admin_edit_major_sheet.html', context={"courses": all_courses})

        # if form isn't valid:
        messages.warning(request, course_form.errors)

    context = {
        'course_form': elective_course_form,

    }
    return render(request, 'admin/admin_add_elective_course.html', context)


def edit_course(request, course_number):
    if request.user.is_anonymous:
        return redirect('login')

    courses = Course.objects.all()
    electives = ElectiveCourse.objects.all()
    all_courses = chain(courses, electives)

    try:
        course_obj = Course.objects.get(number=course_number)

        # function code
        if request.method == "GET":
            context = {"courses": courses, "course": course_obj,
                       "prerequisites": course_obj.prerequisite.all()}
            return render(request, 'admin/admin_edit_course.html', context)

        elif request.method == "POST":
            form = UpdateCourse(request.POST, instance=course_obj)

            if form.is_valid():
                course_obj.number = form.cleaned_data['number']
                course_obj.name = form.cleaned_data['name']
                course_obj.credits = form.cleaned_data['credits']

                prerequisites = request.POST.getlist('prerequisite')
                course_obj.prerequisite.clear()
                for prerequisite in prerequisites:
                    prerequisite_obj = Course.objects.get(number=prerequisite)
                    course_obj.prerequisite.add(prerequisite_obj)
                course_obj.save()

                messages.success(
                    request, "Course " + course_obj.name + " has been updated successfully!")
                return redirect("edit-major-sheet")

    except ObjectDoesNotExist:
        pass

    try:
        course_obj = ElectiveCourse.objects.get(number=course_number)

        # function code
        if request.method == "GET":
            context = {"courses": courses, "course": course_obj}
            return render(request, 'admin/admin_edit_elective_course.html', context)

        elif request.method == "POST":
            form = UpdateCourse(request.POST, instance=course_obj)
            if form.is_valid():
                course_obj.number = form.cleaned_data['number']
                course_obj.name = form.cleaned_data['name']
                course_obj.credits = form.cleaned_data['credits']
                course_obj.save()

                messages.success(
                    request, "Course " + course_obj.name + " has been updated successfully!")
                return redirect("edit-major-sheet")

    except ObjectDoesNotExist:
        pass


# used to delete a course using course_id
def delete_course(request, course_number):
    if request.user.is_anonymous:
        return redirect('login')
    try:
        course_obj = Course.objects.get(number=course_number)
        if course_obj:
            course_obj.delete()

    except ObjectDoesNotExist:
        pass

    try:
        course_obj = ElectiveCourse.objects.get(number=course_number)
        if course_obj:
            course_obj.delete()

    except ObjectDoesNotExist:
        pass

    messages.success(request, 'Course has been deleted successfully')
    return redirect("edit-major-sheet")


def delete_course_confirmation(request, course_number):
    if request.user.is_anonymous:
        return redirect('login')
    try:
        course_obj = Course.objects.get(number=course_number)
    except ObjectDoesNotExist:
        pass

    try:
        course_obj = ElectiveCourse.objects.get(number=course_number)
    except ObjectDoesNotExist:
        pass

    context = {
        'course': course_obj
    }
    return render(request, 'admin/delete_course_confirmation.html', context)


# used to display insructor wishlist
def instructor_wishlist(request):
    if request.user.is_anonymous:
        return redirect('login')
    instructor_obj = Instructor.objects.get(user=request.user)

    # check registeration time
    try:
        datetime_interval_last_obj = DateTimeInterval.objects.latest('id')
        if datetime_interval_last_obj.finishing_date < datetime.date.today() or datetime_interval_last_obj.starting_date > datetime.date.today():
            messages.warning(
                request, "You can't access wishlist page! No active registeration time")
            return redirect('home')
        elif datetime_interval_last_obj.finishing_date == datetime.date.today():
            if datetime_interval_last_obj.finishing_time <= datetime.datetime.now().time() or datetime_interval_last_obj.starting_time > datetime.datetime.now().time():
                messages.warning(
                    request, "You can't access wishlist page! No active registeration time")
                return redirect('home')

    except ObjectDoesNotExist:
        messages.warning(
            request, "You can't access wishlist page! No active registeration time")
        return redirect('home')

    courses = Course.objects.all().exclude(number='0410101').exclude(
        number='0410111').exclude(number='0410102').exclude(number='0410211').order_by('number')
    # courses = Course.objects.all()
    elective_courses = ElectiveCourse.objects.all()
    all_courses = chain(courses, elective_courses)

    selected_courses = instructor_obj.whishlist_courses.all()
    selected_elective_courses = instructor_obj.wishlist_elective_courses.all()

    # if search is used filter courses
    query = request.GET.get('q')

    if query:
        try:
            courses = courses.filter(
                Q(number__icontains=query) |
                Q(name__icontains=query)).distinct()
            if courses:
                all_courses = courses
        except ObjectDoesNotExist:
            pass

        try:
            elective_courses = elective_courses.filter(
                Q(number__icontains=query) |
                Q(name__icontains=query)).distinct()
            if elective_courses:
                all_courses = elective_courses
        except ObjectDoesNotExist:
            pass

    context = {
        'all_courses': all_courses,
        'selected_courses': selected_courses,
        'selected_elective_courses': selected_elective_courses
    }

    if request.method == 'GET':
        return render(request, 'instructor/instructor_wishlist.html', context)

    if request.method == 'POST':

        courses = request.POST.getlist('course')
        if len(courses) > 5 or len(courses) == 0:
            # messages.warning(request, "Please Re-check your maximum number of choices")
            return render(request, 'instructor/instructor_wishlist.html', context)

        # Reset old data to set the new wishlist
        instructor_obj.whishlist_courses.clear()
        instructor_obj.wishlist_elective_courses.clear()
        courses1 = Course.objects.exclude(number='0410101').exclude(number='0410111').exclude(
            number='0410102').exclude(number='0410211').order_by('number')

        for c in courses1:
            c.chosen_by.remove(instructor_obj)
        for e in ElectiveCourse.objects.all():
            e.chosen_by.remove(instructor_obj)

        for course in courses:
            try:
                course_obj = Course.objects.get(number=course)
                course_obj.chosen_by.add(instructor_obj)
                instructor_obj.whishlist_courses.add(course_obj)
            except ObjectDoesNotExist:
                pass

            try:
                course_obj = ElectiveCourse.objects.get(number=course)
                course_obj.chosen_by.add(instructor_obj)
                instructor_obj.wishlist_elective_courses.add(course_obj)
            except ObjectDoesNotExist:
                pass

        context = {
            'instructor': instructor_obj
        }

        messages.success(request, "Your whishlist has been saved")
        return render(request, 'instructor/instructor_wishlist_settime.html', context)


# used to submit unpreferred lecture time for instructor wishlist courses
def instructor_wishlist_settime(request):
    if request.user.is_anonymous:
        return redirect('login')
    instructor_obj = Instructor.objects.get(user=request.user)

    if request.method == "GET":
        try:
            datetime_interval_last_obj = DateTimeInterval.objects.latest('id')
            if datetime_interval_last_obj.finishing_date < datetime.date.today():
                messages.warning(
                    request, "You can't access set unpreferred time page! No active registeration")
                return redirect('home')
            elif datetime_interval_last_obj.finishing_date == datetime.date.today():
                if datetime_interval_last_obj.finishing_time < datetime.datetime.now().time():
                    messages.warning(
                        request, "You can't access set unpreferred time page! No active registeration")
                    return redirect('home')
        except ObjectDoesNotExist:
            pass

        return render(request, 'instructor/instructor_wishlist_settime.html', context={})

    if request.method == "POST":
        days1 = request.POST.getlist('days1')
        unpreferred_time1_list = request.POST.getlist('unpreferred_time1')

        days2 = request.POST.getlist('days2')
        unpreferred_time2_list = request.POST.getlist('unpreferred_time2')

        unpreferred_time1 = UnpreferredLectureTime.objects.create(days=days1[0], starting_time=unpreferred_time1_list[0],
                                                                  finishing_time=unpreferred_time1_list[1])

        unpreferred_time2 = UnpreferredLectureTime.objects.create(days=days2[0], starting_time=unpreferred_time2_list[0],
                                                                  finishing_time=unpreferred_time2_list[1])

        instructor_obj.unpreferred_time1 = unpreferred_time1
        instructor_obj.unpreferred_time2 = unpreferred_time2
        instructor_obj.save()

        messages.success(request, "Your unpreferred lecture time has been set")
        return redirect('home')


# used to display each subject statistics
def instructors_statistics(request):
    if request.user.is_anonymous:
        return redirect('login')
    courses = Course.objects.all()
    elective_courses = ElectiveCourse.objects.all()
    all_courses = chain(courses, elective_courses)
    instructors_statistics = []

    for course in all_courses:
        if course.chosen_by.exists():
            instructors_statistics.append(
                (course, course.chosen_by.all().count()))

    # if search is used filter courses
    query = (request.GET.get('q'))

    if query:
        try:
            courses = courses.filter(
                Q(number__icontains=query) |
                Q(name__icontains=query)
            ).distinct()
            if courses:
                all_courses = courses
        except ObjectDoesNotExist:
            pass

        try:
            elective_courses = elective_courses.filter(
                Q(number__icontains=query) |
                Q(name__icontains=query)
            ).distinct()
            if elective_courses:
                all_courses = elective_courses
        except ObjectDoesNotExist:
            pass

        instructors_statistics = [
            tup for tup in instructors_statistics if any(i in tup for i in all_courses)]

    context = {
        'instructors_statistics': instructors_statistics
    }

    return render(request, 'instructor/instructors_statistics.html', context)


# used to reset all instructors statistics confirmation page
def reset_instructors_statistics_confirmation(request):
    if request.user.is_anonymous:
        return redirect('login')
    return render(request, 'instructor/instructor_reset_statistics.html')


# used to reset all instructors statistics
def reset_instructors_statistics(request):
    if request.user.is_anonymous:
        return redirect('login')
    courses = Course.objects.all()
    elective_courses = ElectiveCourse.objects.all()
    instructors = Instructor.objects.all()

    if courses:
        for course in courses:
            if course.chosen_by.exists():
                course.chosen_by.clear()

        for instructor in instructors:
            if instructor.whishlist_courses.exists():
                instructor.whishlist_courses.clear()

    if elective_courses:
        for course in elective_courses:
            if course.chosen_by.exists():
                course.chosen_by.clear()

        for instructor in instructors:
            if instructor.wishlist_elective_courses.exists():
                instructor.wishlist_elective_courses.clear()

    messages.success(request, 'All instructors statistics have been reset')
    return redirect('instructors-statistics')


# used to show instructors names and time for each course statistic
def candidate_info(request, course_number):
    if request.user.is_anonymous:
        return redirect('login')
    try:
        course_obj = Course.objects.get(number=course_number)
        instructors = course_obj.chosen_by.all()

    except ObjectDoesNotExist:
        pass

    try:
        course_obj = ElectiveCourse.objects.get(number=course_number)
        instructors = course_obj.chosen_by.all()

    except ObjectDoesNotExist:
        pass

    # if search is used filter instructors
    query = request.GET.get('q')

    if query:
        instructors = instructors.filter(
            Q(user__username__icontains=query) |
            Q(fullname__icontains=query) |
            Q(instructor_id__icontains=query)
        ).distinct()

    context = {
        'course': course_obj,
        'instructors': instructors
    }

    return render(request, 'instructor/candidate_info.html', context)


def progress(request):
    if request.user.is_anonymous:
        return redirect('login')
    if request.method == 'POST':
        formset = ProgressFormSet(request.POST)
        for form in formset:
            if form.is_valid():
                course_id = form.cleaned_data['course_id']
                course_id = int(course_id)
                student = Student.objects.get(user=request.user)
                is_completed = form.cleaned_data['is_completed']
                if is_completed:
                    Progress.objects.get_or_create(
                        course_id=course_id,
                        student=student
                    )
                else:
                    Progress.objects.filter(
                        course_id=course_id,
                        student=student
                    ).delete()
    courses = Course.objects.all().order_by('number')
    # courses = Course.objects.exclude(number='0410101').exclude(number='0410111').exclude(number='0410102').exclude(number='0410211').order_by('number')

    initial = []
    for course in courses:
        is_completed = Progress.objects.filter(
            course=course, student__user=request.user).exists()
        initial.append({
            'name': course.name,
            'is_completed': is_completed,
            'course_id': course.id
        })
    formset = ProgressFormSet(initial=initial)
    return render(
        request,
        'student/progress.html',
        context={'formset': formset}
    )


def plan(request):
    if request.user.is_anonymous:
        return redirect('login')
    # get the students ID
    student = Student.objects.get(user=request.user)
    # get the students credits
    cred = 0
    # get the courses the student completed
    courses_completed = [
        progress.course for progress in Progress.objects.filter(student=student)]
    for course in courses_completed:
        cred += course.credits
    if cred < 20:
        limit = 3
    else:
        limit = 2
    courses_left = list(
        set(Course.objects.all().order_by('number')) - set(courses_completed))
    semesters = []
    semester = []
    creds = []
    while courses_left:
        courses_available = [
            course for course in courses_left
            if course.is_available_after(courses_completed)
        ]
        if not courses_available:
            courses_completed.extend(semester)
            semesters.append(semester)
            semester = []
        while courses_available:
            course = courses_available.pop()
            courses_left.remove(course)
            if len(semester) < limit:
                semester.append(course)
            else:
                courses_completed.extend(semester)
                semesters.append(semester)
                semester = [course]
    semesters.append(semester)
    for semester in semesters:
        x = 15
        for course in semester:
            x = x - course.credits
        creds.append(x)
    return render(request, 'student/plan.html', context={'semesters': semesters, 'cr': creds})


def student_wishlist(request):
    if request.user.is_anonymous:
        return redirect('login')
    student = Student.objects.get(user=request.user)
    elective_courses = ElectiveCourse.objects.all()
    selected_elective_courses = student.wishlist_elective_courses.all()

    if request.method == 'POST':
        temp_selected_elective_courses = selected_elective_courses
        temp = temp_selected_elective_courses
        print("temp", temp_selected_elective_courses)

        courses = request.POST.getlist('course')
        print("course", courses)

        if len(courses) > 3 or len(courses) == 0:

            context = {'courses': elective_courses,
                       'selected_elective_courses': selected_elective_courses}
            return render(request, 'student/student_wishlist.html', context)

        courses = request.POST.getlist('course')

        # student.wishlist_elective_courses.clear()

        for course in courses:
            course_obj = ElectiveCourse.objects.get(number=course)
            if course_obj not in temp:
                print("new", course_obj.name)
                course_obj.total_num_of_students += 1
                course_obj.save()
            else:
                print("existing", course_obj.name)

        print("TEMP", temp)

        for c in temp:
            if c.number not in courses:
                course_obj = ElectiveCourse.objects.get(number=c.number)
                print("removed", c.name, course_obj)
                course_obj.total_num_of_students -= 1
                course_obj.save()
            else:
                print("existing", c.name)

        print("END TEMP", temp)

        student.wishlist_elective_courses.clear()
        for course in courses:
            course_obj = ElectiveCourse.objects.get(number=course)
            student.wishlist_elective_courses.add(course_obj)

        # student.wishlist_elective_courses.clear()
        for course in courses:
            course_obj = ElectiveCourse.objects.get(number=course)
            student.wishlist_elective_courses.add(course_obj)

        messages.success(request, "Your whishlist has been saved!")
        return redirect("home")

    elif request.method == 'GET':

        # check registeration time
        try:
            datetime_interval_last_obj = DateTimeInterval.objects.latest('id')
            if datetime_interval_last_obj.finishing_date < datetime.date.today() or datetime_interval_last_obj.starting_date > datetime.date.today():
                messages.warning(
                    request, "You can't access wishlist page! No active registeration time")
                return redirect('home')
            elif datetime_interval_last_obj.finishing_date == datetime.date.today():
                if datetime_interval_last_obj.finishing_time <= datetime.datetime.now().time() or datetime_interval_last_obj.starting_time > datetime.datetime.now().time():
                    messages.warning(
                        request, "You can't access wishlist page! No active registeration time")
                    return redirect('home')
        except ObjectDoesNotExist:
            messages.warning(
                request, "You can't access wishlist page! No active registeration time")
            return redirect('home')

        # if search is used filter elective courses
        query = request.GET.get('q')

        if query:
            elective_courses = elective_courses.filter(
                Q(number__icontains=query) |
                Q(name__icontains=query)
            ).distinct()

        context = {"courses": elective_courses,
                   'selected_elective_courses': selected_elective_courses}

        return render(request, 'student/student_wishlist.html', context)


# used to display student statistics
def students_statistics(request):
    if request.user.is_anonymous:
        return redirect('login')
    elective_courses = ElectiveCourse.objects.filter(
        total_num_of_students__gte=1)

    query = request.GET.get('q')

    if query:
        elective_courses = elective_courses.filter(
            Q(name__icontains=query) |
            Q(number__icontains=query)
        ).distinct()

    context = {"courses": elective_courses}

    return render(request, 'student/students_statistics.html', context)


# used to reset all students statistics confirmation page
def reset_students_statistics_confirmation(request):
    if request.user.is_anonymous:
        return redirect('login')
    return render(request, 'student/student_reset_statistics.html')

# used to reset all students statistics


def reset_students_statistics(request):
    if request.user.is_anonymous:
        return redirect('login')
    elective_courses = ElectiveCourse.objects.filter(
        total_num_of_students__gte=1)
    elective_courses.update(total_num_of_students=0)

    students = Student.objects.all()
    for student in students:
        student.wishlist_elective_courses.clear()
        student.save()
    return redirect('students-statistics')
