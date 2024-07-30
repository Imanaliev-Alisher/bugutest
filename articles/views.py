from django.http import Http404
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .permission import IsAuthorOrReadOnly
from .models import Article
from .serializers import ArticleSerializer

class ArticleListView(generics.ListCreateAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):

        if self.request.user.is_authenticated:
            if self.request.user.role == 'subscriber':
                return Article.objects.all()
            if self.request.user.role == 'author':
                return Article.objects.all()

        if not self.request.user.is_authenticated:
            return Article.objects.filter(is_public=True)

    def perform_create(self, serializer):

        if not self.request.user.is_authenticated:
            raise PermissionDenied("You are not logged in, please log into your account!")

        if self.request.user.role != 'author':
            raise PermissionDenied("Only authors can create articles.")
        serializer.save(author=self.request.user)


class ArticleDetailView(APIView):
    permission_classes = [IsAuthorOrReadOnly]

    def get(self, request, pk, format=None):

        if not self.request.user.is_authenticated:
            raise PermissionDenied("You are not logged in, please log into your account!")

        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        article = self.get_object(pk)
        self.check_object_permissions(request, article)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        article = self.get_object(pk)
        self.check_object_permissions(request, article)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404
