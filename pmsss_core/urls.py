from django.contrib import admin
from django.urls import path
from home.views import home ,student_home
from accounts.views import register , profile_personal
from accounts.views import login_view
from applications.views import new_application ,student_dashboard
from django.urls import include
from institutes.views import institute_dashboard , upload_students_csv , institute_student_tracking , rejected_applications


urlpatterns = [
    path("", home, name="home"),
    path("", include("accounts.urls")),
    path("register/", register, name="register"),
    path("admin/", admin.site.urls),
    path("login/", login_view, name="login"),
    path("apply/", new_application, name="apply"),
    path("mock/digilocker/", include("digilocker_mock.urls")),
    path("mock/applisarkar/", include("applisarkar_mock.urls")),
    path("dashboard/", student_dashboard, name="dashboard"),
    path("student/home/", student_home, name="student_home"),
    path("student/profile/personal/", profile_personal, name="profile_personal"),
    path("institute/dashboard/", institute_dashboard, name="institute_dashboard"),
    path("institute/upload-students/", upload_students_csv, name="upload_students"),
    path("institute/student-tracking/",institute_student_tracking,name="institute_student_tracking"),
    path("institute/rejected-applications/", rejected_applications, name="rejected_applications"),




]
