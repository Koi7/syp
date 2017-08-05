from django.core.management.base import BaseCommand, CommandError
from posts.models import Post, Like
from django.db.models import Q

class Command(BaseCommand):
    help = 'Add random amount of likes to post with id.'

    def add_arguments(self, parser):
        parser.add_argument('post_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for post_id in options['post_id']:
            try:
                post = Post.objects.get(pk=post_id)
            except Post.DoesNotExist:
                raise CommandError('Post "%s" does not exist' % post_id)
            likes = post.liked
            for like in likes:
                like.delete()
            self.stdout.write(self.style.SUCCESS('Successfully deleted likes, post: "%s"' % post_id))