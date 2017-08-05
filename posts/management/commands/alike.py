from django.core.management.base import BaseCommand, CommandError
from posts.models import Post, Like
from django.db.models import Q

class Command(BaseCommand):
    help = 'Add random amount of likes to post with id.'

    def add_arguments(self, parser):
        parser.add_argument('post_id', nargs='+', type=int)
        parser.add_argument('sex', nargs='+', type=int)

    def handle(self, *args, **options):
        for post_id in options['post_id']:
            try:
                post = Post.objects.get(pk=post_id)
            except Post.DoesNotExist:
                raise CommandError('Post "%s" does not exist' % post_id)
            import random
            from django.contrib.auth.models import User
            like_amount = random.randint(0, 35)
            ids = []
            sex = options['sex'][0]
            print sex
            for i in range(like_amount):
                ids.append(random.randint(5, 126))
            if sex == 2 or sex == 1:
                q = Q(id__in=ids, vkuser__sex=sex, is_superuser=False)
            else:
                q = Q(id__in=ids, is_superuser=False)
            for user in User.objects.filter(q):
                like_obj, created = Like.objects.get_or_create(user=user, post_id=post_id)
                like_obj.save()
            self.stdout.write(self.style.SUCCESS('Successfully added likes to post: "%s"' % post_id))