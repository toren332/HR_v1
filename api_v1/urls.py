from rest_framework import routers

from . import views as profiles_views

router = routers.DefaultRouter()

# ACCOUNTS BLOCK

router.register('account', profiles_views.AccountViewSet, 'account')
router.register('users', profiles_views.UserViewSet, basename='users')
router.register('profiles', profiles_views.ProfileViewSet, basename='profiles')
router.register('teachers', profiles_views.TeacherViewSet, basename='teachers')
router.register('students', profiles_views.StudentViewSet, basename='students')
router.register('clients', profiles_views.ClientViewSet, basename='clients')


# OBJECTS BLOCK

router.register('groups', profiles_views.GroupViewSet, basename='groups')
router.register('lessons', profiles_views.LessonViewSet, basename='lessons')
router.register('universities', profiles_views.UniversityViewSet,
                basename='universities')


urlpatterns = router.urls
