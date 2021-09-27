from rest_framework.serializers import ModelSerializer
from .models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'avatar', 'date_joined']

        # hide password when get data
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }

        def create(self, validated_data):
            user = User(**validated_data)
            user.set_password(validated_data['password'])
            user.save()

            return user


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = ['value', 'updated_date', 'user', 'post']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_date', 'updated_date', 'creator', 'post']


class PostSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    # author = UserSerializer()

    class Meta:
        model = Post
        fields = ['title', 'content', 'created_date', 'updated_date', 'image', 'tags', 'author']


class ReportSerializer(ModelSerializer):
    user_create_report = UserSerializer()
    user_is_reported = UserSerializer()

    class Meta:
        model = Report
        fields = ['image', 'reason', 'reported_date', 'user_create_report', 'user_is_reported']


class AuctionItemSerializer(ModelSerializer):
    user_sell = UserSerializer()

    class Meta:
        model = AuctionItem
        fields = ['name', 'description', 'image', 'user_sell']


class TransactionSerializer(ModelSerializer):
    user_buy = UserSerializer()
    items = AuctionItemSerializer()

    class Meta:
        model = Transaction
        fields = ['transaction_date', 'started_price', 'last_price', 'items', 'user_buy']
