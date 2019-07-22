from rest_framework import viewsets, status
from rest_framework.response import Response

from movies.models.comment import Comment
from movies.serializers.comment import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    filterset_fields = ('movie__id', 'deleted')

    serializers = {
        'default': CommentSerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
