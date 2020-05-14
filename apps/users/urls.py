from django.urls import path

from .views import (
    UserPositionCreateView,
    UserPositionListView,
    UserPositionUpdateView,
    AdminDashboardView,
    UserTeamCreateView,
    UserTeamListView,
    UserTeamUpdateView,
    UserProjectJoinedCreateView,
    UserProjectJoinedListView,
    # SignUpView,
    # SignInView,
    # SignOutView,
    # UserListView,
)

app_name = 'users'

urlpatterns = [
    # path('signup', SignUpView.as_view(), name='signup'),
    # path('signin', SignInView.as_view(), name='signin'),
    # path('signout', SignOutView.as_view(), name='signout'),
    #
    # path('user/<int:id>/change-role/', ChangeRoleUserView.as_view(), name='change-role'),
    # path('users/', UserListView.as_view(), name='users-list'),
    # path('user/<int:id>/edit/', UserUpdateView.as_view(), name='user-update'),
    # path('user/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('dashboard/', AdminDashboardView.as_view(), name='dashboard'),
    path('position/add/', UserPositionCreateView.as_view(), name='position-add'),
    path('position/<int:id>/edit/', UserPositionUpdateView.as_view(), name='position-update'),
    path('positions/', UserPositionListView.as_view(), name='position-list'),
    path('teams/', UserTeamListView.as_view(), name='team-list'),
    path('team/add/', UserTeamCreateView.as_view(), name='team-add'),
    path('team/<int:id>/edit/', UserTeamUpdateView.as_view(), name='team-update'),
    path('project-joined/add/', UserProjectJoinedCreateView.as_view(), name='project-joined-add'),
    path('projects-joined/', UserProjectJoinedListView.as_view(), name='project-joined-list'),
]