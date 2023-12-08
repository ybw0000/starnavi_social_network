from django.db import models
from django.db.models import Count
from django.db.models import Q

from user.models import User


class Post(models.Model):
    text = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    @classmethod
    def get_posts_by_likes_date_range(cls, date_from, date_to):
        liked_posts = Like.get_likes_in_date_range(date_from, date_to)
        return [like.post for like in liked_posts]


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'post']

    @classmethod
    def get_likes_in_date_range(cls, date_from, date_to):
        filter_condition = Q()

        if date_from and date_to:
            if date_from > date_to:
                filter_condition &= (
                        Q(created_at__gte=date_from) | Q(created_at__lte=date_to)
                )
            else:
                filter_condition &= Q(created_at__range=(date_from, date_to))
        elif date_from:
            filter_condition &= Q(created_at__gte=date_from)
        elif date_to:
            filter_condition &= Q(created_at__lte=date_to)

        return (
            cls.objects.filter(filter_condition)
            .values('created_at__date')
            .annotate(likes_count=Count('id'))
            .order_by('created_at__date')
        )
