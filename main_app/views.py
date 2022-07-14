from ast import Del
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Contact, Photo
from .forms import PostingForm

import uuid
import boto3

S3_BASE_URL = 'https://s3.us-west-1.amazonaws.com/'
BUCKET = 'devlife-24'

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def profiles_index(request):
    profiles = Profile.objects.filter(user=request.user)
    return render(request, 'profiles/index.html', { 'profiles': profiles })

@login_required
def profiles_detail(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    contacts_profile_doesnt_have = Contact.objects.exclude(id__in = profile.contacts.all().values_list('id'))
    posting_form = PostingForm()
    return render(request, 'profiles/detail.html', { 'profile': profile, 'posting_form': posting_form, 'contacts': contacts_profile_doesnt_have })

@login_required
def add_posting(request, profile_id):
    form = PostingForm(request.POST)
    if form.is_valid():
        new_posting = form.save(commit=False)
        new_posting.profile_id = profile_id
        new_posting.save()
    return redirect('detail', profile_id=profile_id)

@login_required
def assoc_contact(request, profile_id, contact_id):
    Profile.objects.get(id=profile_id).contacts.add(contact_id)
    return redirect('detail', profile_id=profile_id)

@login_required
def assoc_contact_delete(request, profile_id, contact_id):
    Profile.objects.get(id=profile_id).contacts.remove(contact_id)
    return redirect('detail', profile_id=profile_id)

@login_required
def add_photo(request, profile_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, profile_id=profile_id)
            photo.save()
        except Exception as error:
            print("Error uploading photo: ", error)
            return redirect('detail', profile_id=profile_id)
    return redirect('detail', profile_id=profile_id)

def signup(request):
    error_messages = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_messages = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_messages': error_messages}
    return render(request, 'registration/signup.html', context)
        

class ProfileCreate(LoginRequiredMixin, CreateView):
    model = Profile
    fields = ['name', 'username', 'occupation', 'age', 'aboutme']
    success_url = '/profiles/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['username', 'occupation', 'age', 'aboutme']

class ProfileDelete(LoginRequiredMixin, DeleteView):
    model = Profile
    success_url = '/profiles/'

class ContactList(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'contacts/index.html'

class ContactDetail(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = 'contacts/detail.html'

class ContactCreate(LoginRequiredMixin, CreateView):
    model = Contact
    fields = ['name', 'email', 'company', 'notes']

class ContactUpdate(LoginRequiredMixin, UpdateView):
    model = Contact
    fields = ['name', 'email', 'company', 'notes']

class ContactDelete(LoginRequiredMixin, DeleteView):
    model = Contact
    success_url = '/contacts/'