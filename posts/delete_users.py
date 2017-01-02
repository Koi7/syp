from django.contrib.auth.models import User

all_users = User.objects.all()
for user in all_users:
    user.delete()
