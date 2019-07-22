from rest_framework import serializers

from movies.models.comment import Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'body', 'movie', 'created', 'updated')
