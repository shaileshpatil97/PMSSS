from django.contrib import admin
from django.urls import path
from home.views import home ,student_home
from accounts.views import register , profile_personal
from accounts.views import login_view
from applications.views import new_application ,student_dashboard
from django.urls import include


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



]
