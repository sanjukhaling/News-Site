from django.urls import path,include
from .views import *

app_name = "backendapp"

urlpatterns = [
    ##LOGIN/LOGOUT
    path('login', AdminLoginView.as_view(), name='admin_login'),
    path('logout', AdminLogoutView.as_view(), name='admin_logout'),


    path('users/',UserListView.as_view(),name="user_list"),
    path('users/add/',UserAddView.as_view(),name="admin_signup"),
    path('user/<int:id>/update/',UserUpdateView.as_view(),name="user_update"),
    path('user/<int:id>/delete/',UserDeleteView.as_view(),name="user_delete"),   
    path("", AdminDashboardView.as_view(), name="dashboard"),


    #####NEWS####
    path("newslist/", AdminNewsListView.as_view(), name="admin_news_list"),
    path("newscreate/", AdminNewsCreateView.as_view(), name="admin_news_create"),
    path("news<int:id>-dnews/", AdminNewsDetailView.as_view(), name="admin_news_detail"),
    path("news<int:id>-update/", AdminNewsUpdateView.as_view(), name="newsupdate"),
    path("news<int:id>-delete/", AdminNewsDeleteView.as_view(), name="newsdelete"),


    ######NEWS CATEGORY####
    path("categorylist/", AdminCategoryNewsListView.as_view(), name="admin_categorynews_list"),
    path("categorycreate/", AdminCreateCategoryView.as_view(), name="news_cat_create"),
    path("newscat<int:id>update/", NewsCategoryUpdateView.as_view(), name="categoryupdate"),
    path("newscategory<int:id>delete/", NewsCategoryDeleteView.as_view(), name="newscategory_delete"),
    path("newscategory<int:id>detail/", NewsCategoryDetailView.as_view(), name="newscategorydetail"),


     ####NEWS####COMMENT#####
    path("newscommentlist/", NewsCommentListView.as_view(), name="news_comment_list"),
    path("newscommentcreate/", NewsCommentCreateView.as_view(), name="news_comment_create"),
    path("newscomment<int:id>update/", NewsCommentUpdateView.as_view(), name="news_comment_update"),
    path("newscomment<int:id>delete/", NewsCommentDeleteView.as_view(), name="news_comment_delete"),
    path("newscomment<int:id>detail/", NewsCommentDetailView.as_view(), name="news_comment_detail"),


    ###CONTACT######
    path("ourcontact/", OurContactCreateView.as_view(), name="ourcontact_create"),
    path('contact/list/', ContactListView.as_view(), name="contact_list"),


    ###About####
    path("staff/create", StaffCreateView.as_view(), name="staff_create"),
    path("staff/list", StaffListView.as_view(), name="staff_lists"),
    path("staff/<int:id>/update", StaffUpdateView.as_view(), name="staff_update"),
    path("staff/<int:id>/delete", StaffDeleteView.as_view(), name="staff_delete"),
    path("staff/<int:id>/detail", StaffDetailView.as_view(), name="staff_detail"),

]