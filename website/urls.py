from django.urls import path

from . import views


urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('reset-password', views.reset_password, name='reset-password'),
    path('account', views.account, name='account'),
    path('logout', views.logout, name='logout'),
    path('delete-account', views.delete_account, name='delete-account'),
    path('validate-email', views.validate_email, name='validate-email'),
    path('change-password', views.change_password, name='change-password'),
    path('exercises', views.exercises, name='exercises'),
    path('exercises/<exercise>/test', views.exercise_test, name='exercise-test'),
    path('exercises/<exercise>/cr/files/<path:path>', views.exercise_cr_files, name='exercise-cr-files'),
    path('exercises/<exercise>/cr/notes', views.exercise_cr_files, name='exercise-cr-files'),
    path('exercises/<exercise>/forum', views.exercise_forum, name='exercise-forum'),
    path('extension', views.extension, name='extension'),
    path('', views.index, name='index'),
]
