from datetime import timedelta

from django.utils.timezone import now
from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(required=False, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'author')


class AnalyticsQueryParamsSerializer(serializers.Serializer):
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)

    def validate(self, data):
        date_from = data.get('date_from')
        date_to = data.get('date_to')

        if not date_from and not date_to:
            data['date_from'] = now().date()
            data['date_to'] = (now() + timedelta(days=1)).date()  # because it compares time also in DB
        elif date_from == date_to:
            data['date_to'] = date_to + timedelta(days=1)  # because it compares time also in DB
        return data
