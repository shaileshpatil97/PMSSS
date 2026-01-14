from django.urls import path
from . import views

urlpatterns = [

    # Student Home
    path("student/home/", views.student_home, name="student_home"),

    # Profile Wizard
    path("student/profile/", views.profile_personal, name="profile_personal"),
    path("student/profile/address/", views.profile_address, name="profile_address"),
    path("student/profile/other/", views.profile_other, name="profile_other"),
    path("student/profile/course/", views.profile_course, name="profile_course"),
    path("student/profile/qualification/", views.profile_qualification, name="profile_qualification"),
    path("student/profile/hostel/", views.profile_hostel, name="profile_hostel"),

    # Schemes
    path("student/schemes/", views.all_schemes, name="all_schemes"),

    # Applications
    path("student/my-applied/", views.my_applied, name="my_applied"),
    path("student/my-cancelled/", views.my_cancelled, name="my_cancelled"),
    path("student/scheme-history/", views.scheme_history, name="scheme_history"),

    # Notifications
    path("student/notifications/", views.notifications, name="notifications"),

 
]
