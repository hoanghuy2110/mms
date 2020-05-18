from django.urls import path



from apps.users.views import (
    UserPositionCreateView,
    UserPositionListView,
    UserPositionUpdateView,
    AdminDashboardView,
    UserTeamCreateView,
    UserTeamListView,
    UserTeamUpdateView,
    UserProjectJoinedCreateView,
    UserProjectJoinedListView,
    UserProjectJoinedUpdateView,
    UserMemberCreateView,
    UserMemberListView,
    UserExportCSVCreateView,
    SignUpView,
    SignInView,
    SignOutView,
    UserMemberUpdateView
)

app_name = 'users'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', SignOutView.as_view(), name='signout'),
    # path('user/<int:id>/change-role/', ChangeRoleUserView.as_view(), name='change-role'),
    path('member/add/', UserMemberCreateView.as_view(), name='member-add'),
    path('members/', UserMemberListView.as_view(), name='member-list'),
    path('member/<int:id>/edit/', UserMemberUpdateView.as_view(), name='member-update'),
    path('dashboard/', AdminDashboardView.as_view(), name='dashboard'),
    path('position/add/', UserPositionCreateView.as_view(), name='position-add'),
    path('position/<int:id>/edit/', UserPositionUpdateView.as_view(), name='position-update'),
    path('positions/', UserPositionListView.as_view(), name='position-list'),
    path('teams/', UserTeamListView.as_view(), name='team-list'),
    path('team/add/', UserTeamCreateView.as_view(), name='team-add'),
    path('team/<int:id>/edit/', UserTeamUpdateView.as_view(), name='team-update'),
    path('project-joined/add/', UserProjectJoinedCreateView.as_view(), name='project-joined-add'),
    path('projects-joined/', UserProjectJoinedListView.as_view(), name='project-joined-list'),
    path('project-joined/<int:id>/edit/', UserProjectJoinedUpdateView.as_view(), name='project-joined-update'),
    path('export/', UserExportCSVCreateView.as_view(), name='export')
]
