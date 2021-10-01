

from rest_framework.serializers import ModelSerializer
from .models import User, Tag, Action, Comment, Post, Report, AuctionItem, Transaction

from rest_framework import serializers


class UserSerializer(ModelSerializer):
    birthday = serializers.DateTimeField(format="%d/%m/%Y", input_formats=['%d/%m/%Y', ], default_timezone=None)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'birthday', 'username', 'password', 'avatar', 'date_joined']

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
        fields = ['id', 'name']


class ActionSerializer(ModelSerializer):
    class Meta:
        model = Action
        fields = ['id', 'type', 'updated_date', 'creator', 'post']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_date', 'updated_date', 'creator', 'post']


class PostSerializer(ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    creator = UserSerializer()

    class Meta:
        model = Post
        fields = ['id', 'content', 'created_date', 'updated_date', 'image', 'active', 'tags', 'creator']


class ReportSerializer(ModelSerializer):
    # user_create_report = UserSerializer()
    # user_is_reported = UserSerializer()

    class Meta:
        model = Report
        fields = ['id', 'image', 'reason', 'reported_date', 'updated_date', 'creator', 'user_is_reported']


class AuctionItemSerializer(ModelSerializer):
    # user_sell = UserSerializer()

    class Meta:
        model = AuctionItem
        fields = ['id', 'name', 'image', 'price', 'user_sell', 'post']


class TransactionSerializer(ModelSerializer):
    # user_buy = UserSerializer()

    class Meta:
        model = Transaction
        fields = ['id', 'transaction_date', 'updated_date', 'started_price', 'last_price', 'item', 'user_buy']
