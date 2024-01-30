from typing import Any
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse,response
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.views.generic import *
from yousta.forms import *
from yousta.models import *
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404



def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session!!!")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper



def is_admin(fn):
    def wrapper(request,*args,**Kwargs):
        if not request.user.is_superuser:
            messages.error(request,"permission denied for current user !!!")
            return redirect("signin")
        else:
           return fn(request,*args,**Kwargs)
    return wrapper



decs=[signin_required,is_admin]


class IndexView(TemplateView):
    template_name="yousta/index.html"




class SignUpView(CreateView):

    template_name="yousta/register.html"
    form_class=RegistrationForm
    model=User
    success_url=reverse_lazy("signin")

    def form_valid(self, form):
         messages.success(self.request,"Account created")
         return super().form_valid(form)
    def form_invalid(self,form):
         messages.error(self.request,"failed to create")
         return super().form_invalid(form)
    
    
# class SignInView(FormView):
#     template_name="yousta/login.html"
#     form_class=LoginForm

#     def post(self,request,*args,**kwargs):
#         form=LoginForm(request.POST)

#         if form.is_valid():
#             uname=form.cleaned_data.get("username")
#             pwd=form.cleaned_data.get("password")
#             usr=authenticate(request,username=uname,password=pwd)
#             if usr:
#                 login(request,usr)
#                 messages.success(request,"login successfully")
#                 return redirect("index")
#             else:
#                 messages.error(request,"invalid creadential")
#                 return render(request,self.template_name,{"form":form})  

def is_adminn(user):
    return user.is_authenticated and user.is_staff

class SignInView(FormView):
    template_name = "yousta/login.html"
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            uname = form.cleaned_data.get("username")
            pwd = form.cleaned_data.get("password")
            usr = authenticate(request, username=uname, password=pwd)

            if usr:
                login(request, usr)

                if is_adminn(usr):
                    messages.success(request, "Admin login successful")
                    return redirect("index")
                else:
                    messages.success(request, "User login successful")
                    return redirect("user-index")
            else:
                messages.error(request, "Invalid credentials")

        return self.form_invalid(form)







@method_decorator(decs,name="dispatch")
class CategoryCreateView(CreateView,ListView):
    template_name="yousta/category_add.html"
    form_class= CategoryCreateForm
    model=Category
    context_object_name="categories"
    success_url=reverse_lazy("category-add")

    def form_valid(self, form):
        messages.success(self.request,"category added successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"category adding failed")
        return super().form_invalid(form)
    
    def get_queryset(self):
        return Category.objects.filter(is_active=True)
    

def remove_category(request,*args,**kwargs):
    id=kwargs.get("pk")
    Category.objects.filter(id=id).update(is_active=False)
    messages.success(request,"category removed")
    return redirect("category-add")


@method_decorator(decs,name="dispatch")

class ClothCreateView(CreateView):
    template_name="yousta/cloth_add.html"
    model=Cloths
    form_class=ClothAddForm
    success_url=reverse_lazy("cloth-list")
    def form_valid(self, form):
        messages.success(self.request,"cloth has been added")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"cloth adding failed")
        return super().form_invalid(form)
    
@method_decorator(decs,name="dispatch")
class ClothListView(ListView):
    template_name="yousta/cloth_list.html"
    model=Cloths
    context_object_name="cloths"

@method_decorator(decs,name="dispatch")
class ClothUpdateView(UpdateView):
    template_name="yousta/cloth_edit.html"
    model=Cloths
    form_class=ClothAddForm
    success_url=reverse_lazy("cloth-list")
    def form_valid(self, form):
        messages.success(self.request,"cloth added successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"cloth updating failed")
        return super().form_invalid(form)
    

@signin_required
@is_admin
def remove_clothView(request,*args,**kwrags):
    id=kwrags.get("pk")
    Cloths.objects.filter(id=id).delete()
    return redirect("cloth-list")
     
@method_decorator(decs,name="dispatch")
class ClothVarientCreateView(CreateView):
    template_name="yousta/clothvarient_add.html"
    form_class=ClothVarientForm
    model=ClothVarients
    success_url=reverse_lazy("cloth-list")
    def form_valid(self, form):
        id=self.kwargs.get("pk")
        obj=Cloths.objects.get(id=id)
        form.instance.cloth=obj
        messages.success(self.request,"cloth varient has been added")
        return super().form_valid(form)
    
@method_decorator(decs,name="dispatch")
class ClothDetailView(DetailView):
    template_name="yousta/cloth_detail.html"
    model=Cloths
    context_object_name="cloth"
    

@method_decorator(decs,name="dispatch")
class ClothVarientUpdateView(UpdateView):
    template_name="yousta/varient_edit.html"
    form_class=ClothVarientForm
    model=ClothVarients
    success_url=reverse_lazy("cloth-list")
    def form_valid(self, form):
        messages.success(self.request,"cloth varient updated successfully")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"cloth varent updating failed")
        return super().form_invalid(form)
    
    def get_success_url(self):
        id=self.kwargs.get("pk")
        cloth_varient_object=ClothVarients.objects.get(id=id)
        cloth_id=cloth_varient_object.cloth.id

        return reverse("cloth-detail",kwargs={"pk":cloth_id})

@signin_required
@is_admin  
def remove_varient(request,*args,**kwargs):
    id=kwargs.get("pk")
    ClothVarients.objects.filter(id=id).delete()
    return redirect("cloth-list")

@method_decorator(decs,name="dispatch")
class OfferCreateView(CreateView):
    template_name="yousta/offer_add.html"
    model=Offers
    form_class=OfferAddForm
    success_url=reverse_lazy("cloth-list")
    def form_valid(self, form):
        id=self.kwargs.get("pk")
        obj=ClothVarients.objects.get(id=id)
        form.instance.clothvarient=obj
        messages.success(self.request,"added successfully")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.success(self.request," not added")
        return super().form_invalid(form)
    

    def get_success_url(self):
        id=self.kwargs.get("pk")
        cloth_varient_object=ClothVarients.objects.get(id=id)
        cloth_id=cloth_varient_object.cloth.id
        return reverse("cloth-detail",kwargs={"pk":cloth_id})
    
@signin_required
@is_admin
def remove_offer(request,*args,**kwargs):
    id=kwargs.get("pk")
    offer_object=Offers.objects.get(id=id)
    cloth_id=offer_object.clothvarient.cloth.id
    offer_object.delete()
    return redirect("cloth-detail",pk=cloth_id)
        
@signin_required

def sign_out_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")  

    
###########################################################USER############################################################################


class UserIndexView(ListView):
    template_name="user/base.html"
    model=Cloths
    context_object_name="cloths"
  

class ProfileView(DetailView):
    template_name="user/profilenew.html"
    model=User
    context_object_name="data"


    #     path('linkshpere/profile/<int:pk>/',views.ProfileDetailView.as_view(),name="profile-details"),

class ClothUserDetailView(DetailView):
    template_name="user/cloth_detail.html"
    model=Cloths
    context_object_name="cloth"
    

# class CartAddView(View):
#     def post(self, request, *args, **kwargs):
#         vid = kwargs.get("pk")
#         varient_obj = ClothVarients.objects.get(id=vid)
#         user = request.user
#         form = CartForm(data=request.POST)
#         if form.is_valid():
#             cart_instance = form.save(commit=False)
#             cart_instance.clothvarient = varient_obj
#             cart_instance.user = user
#             cart_instance.save()
#             messages.success(request, 'Item added to the cart successfully.')
#             return redirect('user-index') 
#         else:
#             messages.error(request, 'Error adding item to the cart. Please check the form.')
#             return redirect('user-profile')  
    
# class CartAddView(CreateView):
#     model = Carts
#     form_class = CartForm
#     template_name = 'user/cart_form.html'

#     def form_valid(self, form):
#         variant_id = self.kwargs.get("pk")
#         varient_obj = ClothVarients.objects.get(id=variant_id)
#         form.instance.clothvariant = varient_obj
#         form.instance.user = self.request.user
#         messages.success(self.request, 'Item added to the cart successfully.')
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy('user-index')  # Replace with your actual success URL

#     def form_invalid(self, form):
#         messages.error(self.request, 'Error adding item to the cart. Please check the form.')
#         return super().form_invalid(form)
    




class CartAddView(View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse_lazy('user-index'))

    def post(self, request, *args, **kwargs):
        form = CartForm(request.POST)
        if form.is_valid():
            vid = self.kwargs.get("pk")
            varient_obj = ClothVarients.objects.get(id=vid)
            existing_cart_item = Carts.objects.filter(clothvarient=varient_obj, user=self.request.user, status='in-cart').first()
            if existing_cart_item:
                messages.warning(self.request, 'Item is already in the cart.')
            else:
                Carts.objects.create(clothvarient=varient_obj, user=self.request.user, status='in-cart')
                messages.success(self.request, 'Item added to the cart successfully.')
        else:
            messages.error(self.request, 'Error adding item to the cart. Please check the form.')

        return redirect(reverse_lazy('user-index'))



class CartView(DetailView):
    template_name="user/carts.html"
    model=Carts
    context_object_name="data"