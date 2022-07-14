from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('profiles/', views.profiles_index, name='index'),
    path('profiles/<int:profile_id>/', views.profiles_detail, name='detail'),
    path('profiles/create/', views.ProfileCreate.as_view(), name='profiles_create'),
    path('profiles/<int:pk>/update/', views.ProfileUpdate.as_view(), name='profiles_update'),
    path('profiles/<int:pk>/delete/', views.ProfileDelete.as_view(), name='profiles_delete'),
    path('profiles/<int:profile_id>/add_posting/', views.add_posting, name='add_posting'),
    path('profiles/<int:profile_id>/assoc_contact/<int:contact_id>/', views.assoc_contact, name='assoc_contact'),
    path('profiles/<int:profile_id>/assoc_contact/<int:contact_id>/delete', views.assoc_contact_delete, name='assoc_contact_delete'),
    path('contacts/', views.ContactList.as_view(), name='contacts_index'),
    path('contacts/<int:pk>/', views.ContactDetail.as_view(), name='contacts_detail'),
    path('contacts/create/', views.ContactCreate.as_view(), name='contacts_create'),
    path('contacts/<int:pk>/update/', views.ContactUpdate.as_view(), name='contacts_update'),
    path('contacts/<int:pk>/delete/', views.ContactDelete.as_view(), name='contacts_delete'),
    path('profiles/<int:profile_id>/add_photo/', views.add_photo, name='add_photo'),
    path('accounts/signup/', views.signup, name='signup'),
]
