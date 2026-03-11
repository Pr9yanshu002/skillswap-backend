from django.urls import path
from .views import MentorProfileView, SkillListView, AddUserSkillView, MyUserSkillView, MentorListView

urlpatterns = [
    path('skills/', SkillListView.as_view(), name='skills'),
    path('users/skills/', AddUserSkillView.as_view(), name='add_user_skill'),
    path('users/me/skills/', MyUserSkillView.as_view(), name='my_user_skills'),
    path('mentors/', MentorListView.as_view(), name='mentors'),
    path('mentors/<int:pk>/', MentorProfileView.as_view(), name='mentor_profile'),
]