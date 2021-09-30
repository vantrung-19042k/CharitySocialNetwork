from django.conf import settings
from django.http import Http404

from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class AuthInfo(APIView):
    def get(self, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    # check user info to get detail user info
    def get_permissions(self):
        if self.action == 'get_current_user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False, url_path="current-user")
    def get_current_user(self, request):
        return Response(self.serializer_class(request.user).data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            return super().destroy(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            return super().partial_update(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)


class PostPagination(PageNumberPagination):
    page_size = 2


class PostListCreateViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView):
    queryset = Post.objects.filter(active=True)
    serializer_class = PostSerializer
    pagination_class = PostPagination

    # permission_classes = [permissions.IsAuthenticated, ]

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    def create(self, request, *args, **kwargs):
        title = request.data.get('title')
        content = request.data.get('content')
        image = request.FILES.get('image')
        creator = self.request.user

        if title is None or title == "" or content is None or content == "":
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            post = Post.objects.create(title=title, creator=creator, content=content, image=image)
            post.save()
            return Response(self.serializer_class(post).data, status=status.HTTP_201_CREATED)


class PostViewSet(viewsets.ViewSet, generics.RetrieveAPIView, generics.DestroyAPIView,
                  generics.UpdateAPIView):
    queryset = Post.objects.filter(active=True)
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_permissions(self):
        if self.action in ['add_comment', 'take_action']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    def partial_update(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            return super().partial_update(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            post = self.get_object()
            post.active = False
            post.save()
            return Response(self.serializer_class(post).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @action(methods=['post'], detail=True, url_path="add-tags")
    def add_tag(self, request, pk):
        try:
            post = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            tags = request.data.get("tags")
            if tags is not None:
                for tag in tags:
                    t, _ = Tag.objects.get_or_create(name=tag)
                    post.tags.add(t)
                post.save()

                return Response(self.serializer_class(post).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path='add-comment')
    def add_comment(self, request, pk):
        content = request.data.get('content')
        if content:
            c = Comment.objects.create(content=content,
                                       post=self.get_object(),
                                       creator=request.user)
            return Response(CommentSerializer(c).data,
                            status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, url_path='like')
    def take_action(self, request, pk):
        try:
            action_type = int(request.data['type'])
        except IndexError | ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            action_post = Action.objects.create(type=action_type, creator=request.user, post=self.get_object())
            return Response(ActionSerializer(action_post).data, status=status.HTTP_200_OK)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class AuctionItemViewSet(viewsets.ModelViewSet):
    queryset = AuctionItem.objects.all()
    serializer_class = AuctionItemSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
