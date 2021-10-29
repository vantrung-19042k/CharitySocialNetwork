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
        return Response(self.serializer_class(request.user, context={"request": self.request}).data,
                                                            status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        gender = request.data.get('gender')
        email = request.data.get('email')
        phone = request.data.get('phone')
        birthday = request.data.get('birthday')
        username = request.data.get('username')
        password = request.data.get('password')
        avatar = request.FILES.get('avatar')

        user = User.objects.create(username=username, password=password,
                                   email=email, first_name=first_name,
                                   last_name=last_name, gender=gender,
                                   phone=phone, avatar=avatar, birthday=birthday)
        user.save()

        return Response(self.serializer_class(user, context={"request": self.request}).data,
                        status=status.HTTP_201_CREATED)


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
    page_size = 30


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
        content = request.data.get('content')
        image = request.FILES.get('image')
        tags = request.data.get('tags')
        creator = self.request.user

        if content is None or content == "":
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if tags is None or tags == "":
                post = Post.objects.create(creator=creator, content=content, image=image)
                post.save()
                return Response(self.serializer_class(post, context={"request": self.request}).data,
                                status=status.HTTP_201_CREATED)
            else:
                post = Post.objects.create(creator=creator, content=content, image=image)
                tag = Tag.objects.get_or_create(name=tags)
                t = Tag.objects.get(name=tags)
                post.tags.add(t)
                post.save()
                return Response(self.serializer_class(post, context={"request": self.request}).data,
                                status=status.HTTP_201_CREATED)


class PostViewSet(viewsets.ViewSet, generics.RetrieveAPIView, generics.DestroyAPIView,
                  generics.UpdateAPIView):
    queryset = Post.objects.filter(active=True)
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_permissions(self):
        if self.action in ['add_comment', 'take_action', 'add_item']:
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

    # @action(methods=['post'], detail=True, url_path="add-tags")
    # def add_tag(self, request, pk):
    #     try:
    #         post = self.get_object()
    #     except Http404:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     else:
    #         tags = request.data.get("tags")
    #         if tags is not None:
    #             for tag in tags:
    #                 t, _ = Tag.objects.get_or_create(name=tag)
    #                 post.tags.add(t)
    #             post.save()
    #
    #             return Response(self.serializer_class(post, context={"request": self.request}).data,
    #                                                             status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path="add-tags")
    def add_tag(self, request, pk):
        try:
            post = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            tags = request.data.get("tags")
            if tags is not None:
                t = Tag.objects.create(name=tags)
                post.tags.add(t)
                post.save()

                return Response(self.serializer_class(post, context={"request": self.request}).data,
                                status=status.HTTP_201_CREATED)

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

    @action(methods=['post'], detail=True, url_path='take-action')
    def take_action(self, request, pk):
        try:
            action_type = int(request.data['type'])
        except IndexError | ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            action_post = Action.objects.create(type=action_type, creator=request.user, post=self.get_object())
            return Response(ActionSerializer(action_post).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='get-comments')
    def get_comments(self, request, pk):
        post = self.get_object()
        return Response(CommentSerializer(post.comments.order_by('-id').all(), many=True,
                                          context={"request": self.request}).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path='add-item')
    def add_item(self, request, pk):
        name = request.data.get('name')
        image = request.FILES.get('image')
        price = request.data.get('price')
        if name:
            item = AuctionItem.objects.create(name=name,
                                              image=image,
                                              price=price,
                                              user_sell=request.user,
                                              post=self.get_object())
            return Response(AuctionItemSerializer(item).data,
                            status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ReportViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.DestroyAPIView, generics.RetrieveAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy', 'retrieve']:
            return [permissions.IsAuthenticated(), ]

        return [permissions.AllowAny()]

    def retrieve(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            return super().retrieve(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        try:
            reason = request.data.get('reason')
            image = request.FILES.get('image')
            creator = self.request.user
            user_id = request.data.get('user_id')
            user_is_reported = User.objects.get(pk=user_id)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            report = Report.objects.create(reason=reason, image=image, creator=creator,
                                           user_is_reported=user_is_reported)
            report.save()
            return Response(self.serializer_class(report).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            return super().destroy(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)


class AuctionItemViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = AuctionItem.objects.all()
    serializer_class = AuctionItemSerializer

    def get_permissions(self):
        if self.action in ['add_price', ]:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['post'], detail=True, url_path='add-price')
    def add_price(self, request, pk):
        price = request.data.get('price')
        if price:
            auction_price = AuctionPrice.objects.create(price=price,
                                                        bidder=request.user,
                                                        auction_item=self.get_object())

            return Response(AuctionPriceSerializer(auction_price).data,
                            status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


# # # #


class TagViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ActionViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class TransactionViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated(), ]
        return [permissions.AllowAny()]

    def create(self, request, *args, **kwargs):
        try:
            started_price = request.data.get('started_price')
            last_price = request.data.get('last_price')
            user_id = request.data.get('user_id')
            item_id = request.data.get('item_id')
            user_buy = User.objects.get(pk=user_id)
            item = AuctionItem.objects.get(pk=item_id)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            transaction = Transaction.objects.create(started_price=started_price, last_price=last_price,
                                                     user_buy=user_buy,
                                                     item=item)
            transaction.save()
            return Response(self.serializer_class(transaction).data, status=status.HTTP_201_CREATED)
