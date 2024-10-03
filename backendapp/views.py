from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse
from django.http import Http404, JsonResponse, HttpResponse
from .forms import *
from mainapp.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.core.paginator import Paginator


# LoginRequiredMixin
class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        else:
            return redirect(reverse('backendapp:admin_login'))

        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


# Admin Login
class AdminLoginView(TemplateView):
    template_name = 'admintemplates/loginlogout/adminlogin.html'


    def post(self, request, *args, **kwargs):
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            email = loginform.cleaned_data.get('email')  
            password = loginform.cleaned_data.get('password')
            
            # Use the email for authentication since CustomUser uses email as USERNAME_FIELD
            user = authenticate(email=email, password=password)
            
            if user:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect(reverse('backendapp:admin_news_list'))  # Redirect to admin page
            else:
                # Add an error message and pass the form back to the template
                messages.error(request, "Invalid email or password.")
                return render(request, self.template_name, {'loginform': loginform})
        else:
            # If form is invalid, pass the form back to the template with errors
            messages.error(request, "Form is invalid.")
            return render(request, self.template_name, {'loginform': loginform})
        

# Admin Logout
class AdminLogoutView(TemplateView):
    def get(self, request):
        logout(request)
        return redirect('backendapp:admin_login')


class AdminDashboardView(TemplateView):
    template_name = "admintemplates/basehome/home.html"


#News Category List
class AdminCategoryNewsListView(TemplateView):
    template_name = "admintemplates/newscategory/newscategorylist.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # Fetch all news categories
            categorylist = NewsCategory.objects.all().order_by("-id")
            
            # Implement pagination
            paginator = Paginator(categorylist, 5)  # Show 5 categories per page
            page_number = self.request.GET.get('page')  # Get the page number from the request
            paginated_categories = paginator.get_page(page_number)  # Get paginated results
            total_pages = paginated_categories.paginator.num_pages  # Get total number of pages
            
            # Add data to the context
            context['categorylist'] = paginated_categories  # Paginated category list
            context['lastpage'] = total_pages
            context['totalpagelist'] = [n + 1 for n in range(total_pages)]  # List of total pages

        except NewsCategory.DoesNotExist:
            context['categorylist'] = None
            context['error'] = "No categories found."
            messages.error(self.request, "No categories found.")
        except Exception as e:
            context['categorylist'] = None
            context['error'] = f"An error occurred: {str(e)}"
            messages.error(self.request, f"An error occurred: {str(e)}")

        return context


#News Category Create
class AdminCreateCategoryView(TemplateView):
    template_name = "admintemplates/newscategory/newscategorycreate.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NewsCategoryForm

        return context

    def post(self,request,*args,**kwargs):
        news_cat_forms = NewsCategoryForm(request.POST,request.FILES)
        if news_cat_forms.is_valid():
            news_cat_forms.save()
        else:
            return render(request, self.template_name, {'form': news_cat_forms, 'msg_error': 'sorry! invalid'})
        return redirect('backendapp:admin_categorynews_list')


#News Category Update
class NewsCategoryUpdateView(TemplateView):
    template_name = "admintemplates/newscategory/newscategorycreate.html"

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_id = self.kwargs.get('id')
        news_cat = NewsCategory.objects.get(id=cat_id)
        context['form'] = NewsCategoryForm(instance=news_cat)

        return context

    def post(self, request, *args, **kwargs):
        cat_id = self.kwargs.get('id')
        news_cat = NewsCategory.objects.get(id=cat_id)
        news_cat_form = NewsCategoryForm(request.POST, request.FILES, instance=news_cat)
        if news_cat_form.is_valid():
            news_cat_form.save()
            return redirect('backendapp:admin_categorynews_list')
        else:
            return render(request, self.template_name, {'form': news_cat_form, 'errors_message': 'sorry!!!Not valid'})


#News Category Delete
class NewsCategoryDeleteView(TemplateView):
    template_name = "admintemplates/newscategory/newscategorydelete.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        news_id = self.kwargs.get('id')

        try:
            context['news_cat_delete'] = NewsCategory.objects.get(id=news_id)
        except NewsCategory.DoesNotExist:
            raise Http404("newscategory does not exist")
        return context

    def post(self, request, *args, **kwargs):
        news_id = self.kwargs.get('id')
        try:
            news_delete = NewsCategory.objects.get(id=news_id)
            news_delete.delete()
            # trek_delete.delete(hard=True) we can do it delete parmanent

        except Exception as e:
            print(e, '#############')
            raise Http404("news does not exist")
        return redirect('backendapp:admin_categorynews_list')


#News Category Detail
class NewsCategoryDetailView(TemplateView):
    template_name = "admintemplates/newscategory/newscatdetail.html"

    # model = News
    # context_object_name = "admin_detail_news"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        news_cat_id = self.kwargs.get('id')
        news_cat = NewsCategory.objects.get(id=news_cat_id)
        context['news_cat_detail'] = news_cat

        return context


######NEWS####
#News Detail
class AdminNewsDetailView(TemplateView):
    template_name = "admintemplates/news/newsdetail.html"
    # model = News
    # context_object_name = "admin_detail_news"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        news_id = self.kwargs.get('id')
        news = News.objects.get(id=news_id)
        context['admin_detail_news'] = news

        return context


##News Create
class AdminNewsCreateView(TemplateView):
    template_name = "admintemplates/news/newscreate.html"

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NewsForm

        return context

    def post(self,request,*args,**kwargs):
        news_forms = NewsForm(request.POST,request.FILES)
        # print(news_forms,'*********************')
        if news_forms.is_valid():
            news_forms.save()
        else:
            return render(request, self.template_name, {'form': news_forms, 'msg_error': 'sorry! invalid'})
        return redirect('backendapp:admin_news_list')


#News List

class AdminNewsListView(LoginRequiredMixin, TemplateView):
    template_name = "admintemplates/news/newslist.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # Fetch all news items
            news_list = News.objects.all().order_by("-id")
            
            # Implement pagination
            paginator = Paginator(news_list, 5)  # Show 5 news items per page
            page_number = self.request.GET.get('page')  # Get the page number from the request
            paginated_news = paginator.get_page(page_number)  # Get paginated results
            total_pages = paginated_news.paginator.num_pages  # Get total number of pages
            
            # Add data to the context
            context['news_list'] = paginated_news  # Paginated news list
            context['lastpage'] = total_pages
            context['totalpagelist'] = [n + 1 for n in range(total_pages)]  # List of total pages

        except News.DoesNotExist:
            context['news_list'] = None
            context['error'] = "No news items found."
            messages.error(self.request, "No news items found.")
        except Exception as e:
            context['news_list'] = None
            context['error'] = f"An error occurred: {str(e)}"
            messages.error(self.request, f"An error occurred: {str(e)}")

        return context


## News Update
class AdminNewsUpdateView(TemplateView):
    template_name = "admintemplates/news/newscreate.html"
    # form_class = NewsForm
    # model = News
    # success_url = reverse_lazy("backendapp:admin_news_list")

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        news_id = self.kwargs.get('id')
        news = News.objects.get(id=news_id)
        context['form'] = NewsForm(instance=news)

        return context

    def post(self,request,*args,**kwargs):
        news_id = self.kwargs.get('id')
        news = News.objects.get(id=news_id)
        news_update = NewsForm(request.POST,request.FILES,instance=news)
        if news_update.is_valid():
            news_update.save()
            return redirect('backendapp:admin_news_list')
        else:
            return render(request,self.template_name,{'form': news_update,'msg_errors':'sorry! invalid'})


##News Delete
class AdminNewsDeleteView(TemplateView):
    template_name = "admintemplates/news/newsdelete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news_id = self.kwargs.get('id')
        try:
            context['news_delete'] = News.objects.get(id=news_id)
        except News.DoesNotExist:
            raise Http404("news does not exist")
        return context

    def post(self, request, *args, **kwargs):
        news_id = self.kwargs.get('id')
        try:
            trip_delete = News.objects.get(id=news_id)
            trip_delete.delete()
            # trek_delete.delete(hard=True) we can do it delete parmanent

        except Exception as e:
            print(e, '#############')
            raise Http404("news does not exist")
        return redirect('backendapp:admin_news_list')


####NEWS###COMMENT##
class NewsCommentDetailView(TemplateView):
    template_name = "admintemplates/newscomment/newscommentdetail.html"
    # model = News
    # context_object_name = "admin_detail_news"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        news_id = self.kwargs.get('id')
        news_comment = NewsComment.objects.get(id=news_id)
        context['news_comment_detail'] = news_comment

        return context


##NewsComment Create
class NewsCommentCreateView(TemplateView):
    template_name = "admintemplates/newscomment/newscommentcreate.html"

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NewsCommentForm

        return context

    def post(self, request, *args, **kwargs):
        news_comment_forms = NewsCommentForm(request.POST,request.FILES)
        if news_comment_forms.is_valid():
            news_comment_forms.save()
        else:
            return render(request, self.template_name, {'form': news_comment_forms, 'msg_error': 'sorry! invalid'})
        return redirect('backendapp:news_comment_list')


#NewsComment#List
class NewsCommentListView(TemplateView):
    template_name = "admintemplates/newscomment/newscommentlist.html"

    # queryset = News.objects.all().order_by("-id")
    # context_object_name = "newslist"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["news_comment_list"] = NewsComment.objects.all().order_by("id")

        return context


##NewsComment Update
class NewsCommentUpdateView(TemplateView):
    template_name = "admintemplates/newscomment/newscommentcreate.html"
    # form_class = NewsForm
    # model = News
    # success_url = reverse_lazy("backendapp:admin_news_list")

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        news_id = self.kwargs.get('id')
        news_comment = NewsComment.objects.get(id=news_id)
        context['form'] = NewsCommentForm(instance=news_comment)

        return context


    def post(self,request,*args,**kwargs):
        news_id = self.kwargs.get('id')
        news = NewsComment.objects.get(id=news_id)
        news_comment_update = NewsCommentForm(request.POST,request.FILES,instance=news)
        if news_comment_update.is_valid():
            news_comment_update.save()
            return redirect('backendapp:admin_news_list')
        else:
            return render(request,self.template_name,{'form': news_comment_update,'msg_errors':'sorry! invalid'})


##News Comment Delete
class NewsCommentDeleteView(TemplateView):
    template_name = "admintemplates/newscomment/newscommentdelete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news_id = self.kwargs.get('id')
        try:
            context['news_comment_delete'] = NewsComment.objects.get(id=news_id)
        except NewsComment.DoesNotExist:
            raise Http404("NewsComment does not exist")
        return context

    def post(self, request, *args, **kwargs):
        news_id = self.kwargs.get('id')
        try:
            news_comment_delete = NewsComment.objects.get(id=news_id)
            news_comment_delete.delete()
            # trek_delete.delete(hard=True) we can do it delete parmanent

        except Exception as e:
            print(e, '#############')
            raise Http404("news does not exist")
        return redirect('backendapp:news_comment_list')


      ###OUR###Contact###
class OurContactCreateView(TemplateView):
    template_name = "admintemplates/contact/ourcontact.html"

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OurContactForm

        return context

    def post(self, request, *args, **kwargs):
        our_contact_form = OurContactForm(request.POST,request.FILES)

        if our_contact_form.is_valid():
            our_contact_form.save()
        else:
            return render(request, self.template_name, {'form': our_contact_form, 'msg_error': 'sorry! invalid'})
        return redirect('frontendapp:contact')


    ####CONTACT###LIST##
class ContactListView(TemplateView):
    template_name = "admintemplates/contact/contactlist.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contact_list"] = Contact.objects.all().order_by("id")
        return context


    #####STAFF####
class StaffCreateView(TemplateView):
    template_name = 'admintemplates/staff/staffcreate.html'

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = StaffForm

        return context

    def post(self, request, *args, **kwargs):
        staff_form = StaffForm(request.POST, request.FILES)
        if staff_form.is_valid():
            staff_form.save()
            return redirect('backendapp:staff_lists')
        else:
            return render(request, self.template_name, {'form': staff_form, 'msg_error': 'sorry! invalid'})


#Staff#List
class StaffListView(TemplateView):
    template_name = 'admintemplates/staff/stafflist.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # Fetch all staff members
            staff_list = Staff.objects.all().order_by('id')
            
            # Implement pagination
            paginator = Paginator(staff_list, 5)  # Show 5 staff members per page
            page_number = self.request.GET.get('page')  # Get the page number from the request
            paginated_staff = paginator.get_page(page_number)  # Get paginated results
            total_pages = paginated_staff.paginator.num_pages  # Get total number of pages
            
            # Add data to the context
            context['staff_list'] = paginated_staff  # Paginated staff list
            context['lastpage'] = total_pages
            context['totalpagelist'] = [n + 1 for n in range(total_pages)]  # List of total pages

        except Staff.DoesNotExist:
            context['staff_list'] = None
            context['error'] = "No staff members found."
            messages.error(self.request, "No staff members found.")
        except Exception as e:
            context['staff_list'] = None
            context['error'] = f"An error occurred: {str(e)}"
            messages.error(self.request, f"An error occurred: {str(e)}")

        return context


##Staff Update
class StaffUpdateView(TemplateView):
    template_name = "admintemplates/staff/staffcreate.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_id = self.kwargs.get('id')
        staff = Staff.objects.get(id=staff_id)
        context['form'] = StaffForm(instance=staff)

        return context

    def post(self, request, *args, **kwargs):
        staff_id = self.kwargs.get('id')
        staff = Staff.objects.get(id=staff_id)
        staff_form = StaffForm(request.POST, request.FILES, instance=staff)
        if staff_form.is_valid():
            staff_form.save()
            return redirect('backendapp:staff_lists')
        else:
            return render(request, self.template_name, {'form': staff_form, 'msg_errors': 'sorry! invalid'})


##Staff Delete
class StaffDeleteView(TemplateView):
    template_name = "admintemplates/staff/staffdelete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_id = self.kwargs.get('id')
        try:
            context['staff_delete'] = Staff.objects.get (id=staff_id)
        except Staff.DoesNotExist:
            raise Http404("staff does not exist")
        return context

    def post(self, request, *args, **kwargs):
        staff_id = self.kwargs.get('id')
        try:
            staff_delete = Staff.objects.get(id=staff_id)
            staff_delete.delete()

        except Exception as e:
            print(e, '#############')
            raise Http404("staff does not exist")
        return redirect('backendapp:staff_lists')


##Staff##
class StaffDetailView(TemplateView):
    template_name = "admintemplates/staff/staffdetail.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_id = self.kwargs.get('id')
        try:
            staff_obj = Staff.objects.get(id=staff_id)
            context['staff_detail'] = staff_obj
        except Staff.DoesNotExist:
            context['staff_detail'] = None

        return context


###Signup
class UserAddView(TemplateView):
    template_name = 'admintemplates/user/add.html'

    def get(self, request, *args, **kwargs):
        form = UserRegisterForm()
        return render(request, self.template_name, {'forms': form})

    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)  # Create user instance but don't save it to the database yet
                user.set_password(form.cleaned_data['password'])  # Set the password
                user.username = form.cleaned_data['email'] 
                user.save()  # Now save the user to the database
                login(self.request, user)
                # messages.success(request, 'Your account has been created! You can now log in.')
                return redirect('backendapp:dashboard')  
            
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
        else:
        # Print form errors for debugging
            print(form.errors)  # Add this line to log errors in the console
            messages.error(request, 'Form submission failed. Please correct the errors.')

        return render(request, self.template_name, {'forms': form})


# User List View


class UserListView(TemplateView):
    template_name = "admintemplates/user/list.html"

    def get(self, request, *args, **kwargs):
        try:
            # Fetch all users with selected fields
            users = CustomUser.objects.all().only('id', 'username', 'email', 'first_name', 'last_name', 'phone', 'dob', 'gender', 'address')
            
            # Implement pagination
            paginator = Paginator(users, 10)  # Show 10 users per page
            page_number = request.GET.get('page')  # Get the page number from the request
            paginated_users = paginator.get_page(page_number)  # Get paginated results

            # Create a list of total pages for pagination
            total_pages = paginator.num_pages
            totalpagelist = list(range(1, total_pages + 1))

        except Exception as e:
            messages.error(request, "Error fetching user list.")
            paginated_users = []  # Fallback to an empty list on error
            totalpagelist = []

        return render(request, self.template_name, {
            'users': paginated_users,
            'totalpagelist': totalpagelist,
            'lastpage': total_pages,
        })

# User Update View
class UserUpdateView(TemplateView):
    template_name = "admintemplates/user/add.html"

    def get(self, request, *args, **kwargs):
        try:
            user = get_object_or_404(CustomUser, id=self.kwargs.get('id'))
            form = UserUpdateForm(instance=user)
        except Exception as e:
            messages.error(request, "Error fetching user details.")
            form = None
        return render(request, self.template_name, {'forms': form})

    def post(self, request, *args, **kwargs):
        try:
            user = get_object_or_404(CustomUser, id=self.kwargs.get('id'))
            form = UserUpdateForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "User updated successfully.")
                return redirect('backendapp:user_list')
        except IntegrityError as e:
            messages.error(request, "Error updating user: Integrity error.")
        except Exception as e:
            messages.error(request, "Error updating user.")
        return render(request, self.template_name, {'forms': form})


# User Delete View
class UserDeleteView(TemplateView):
    template_name = "admintemplates/user/delete.html"

    def get(self, request, *args, **kwargs):
        try:
            user = get_object_or_404(User, id=self.kwargs.get('id'))
        except Exception as e:
            messages.error(request, "Error fetching user details.")
            user = None
        return render(request, self.template_name, {'obj': user})

    def post(self, request, *args, **kwargs):
        try:
            user = get_object_or_404(User, id=self.kwargs.get('id'))
            user.delete()
            messages.success(request, "User deleted successfully.")
        except Exception as e:
            messages.error(request, "Error deleting user.")
        return redirect('backendapp:user_list')
