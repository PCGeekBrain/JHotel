from .models import UserProfile
from social_core.backends.google import GoogleOAuth2

def save_profile(backend, user, response, *args, **kwargs):
    # print(backend.name, user)
    # print(response)
    if UserProfile.objects.filter(user=user).exists():
        current_user = UserProfile.objects.get(user=user)
        if backend.name == "google-oauth2":
            current_user.avatar_social=response['image']['url']
            current_user.save()
    else:
        new_user = UserProfile(user=user)
        if backend.name == "google-oauth2":
            print(response['image']['url'])
            new_user.avatar_social=response['image']['url']
        new_user.save()