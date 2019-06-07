from django.shortcuts import render,redirect
from .models import Post
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

# def home(request):
#     context={
#         'posts':Post.objects.all()
#     }
#     return render(request,'home.html',context)

def about(request):
    return render(request,'about.html',{'title':'About'})

class PostListview(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailview(DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreativeview(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']
    template_name = 'post_form.html'
    def form_valid(self, form):
        form.instance.name=self.request.user
        return super().form_valid(form)

class PostUpdateview(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']
    template_name = 'post_form.html'
    def form_valid(self, form):
        form.instance.name=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.name:
            return True
        return False

class PostDeleteview(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    template_name = 'post_confirm_delete.html'
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.name:
            return True
        return False

def register(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'You have registerd successfully!,you can login now')
            return redirect('login')
    else:
         form=UserRegisterForm()
         return render(request,'register.html',{'form':form})

@login_required
def profile(request):
    if request.method=='POST':
          u_form=UserUpdateForm(request.POST,instance=request.user)
          p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
          if u_form.is_valid() and p_form.is_valid():
              u_form.save()
              p_form.save()
              messages.success(request,f'your account has been updated')
              return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context={
             'u_form':u_form,
              'p_form':p_form
        }
        return render(request,'profile.html',context)

