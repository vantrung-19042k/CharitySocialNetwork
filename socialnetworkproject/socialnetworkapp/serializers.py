from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from .models import *

from rest_framework import serializers


class UserSerializer(ModelSerializer):
    birthday = serializers.DateTimeField(format="%d-%m-%Y", input_formats=['%Y-%m-%d', ], default_timezone=None)
    avatar = SerializerMethodField()

    def get_avatar(self, user):
        request = self.context['request']
        name = user.avatar.name
        if name.startswith("static/"):
            path = '/%s' % name
        else:
            path = '/static/%s' % name

        return request.build_absolute_uri(path)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'birthday', 'username', 'password', 'avatar', 'date_joined',
                  'phone', 'gender']

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
    creator = SerializerMethodField()

    def get_creator(self, comment):
        return UserSerializer(comment.creator, context={"request": self.context.get('request')}).data

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_date', 'updated_date', 'creator', 'post']


class AuctionItemSerializer(ModelSerializer):
    # user_sell = UserSerializer()
    # auction_price = AuctionPriceSerializer(many=True, required=False)

    class Meta:
        model = AuctionItem
        fields = ['id', 'name', 'image', 'price', 'user_sell', 'post']


class AuctionPriceSerializer(ModelSerializer):
    class Meta:
        model = AuctionPrice
        fields = ['id', 'price', 'auction_item', 'bidder']


class PostSerializer(ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    creator = UserSerializer()
    image = SerializerMethodField()

    def get_image(self, post):
        request = self.context['request']
        name = post.image.name
        if name.startswith("static/"):
            path = '/%s' % name
        else:
            path = '/static/%s' % name

        return request.build_absolute_uri(path)

    class Meta:
        model = Post
        fields = ['id', 'content', 'created_date', 'updated_date', 'image', 'active', 'tags', 'creator']


class ReportSerializer(ModelSerializer):
    # user_create_report = UserSerializer()
    # user_is_reported = UserSerializer()

    class Meta:
        model = Report
        fields = ['id', 'image', 'reason', 'reported_date', 'updated_date', 'creator', 'user_is_reported']


class TransactionSerializer(ModelSerializer):
    # user_buy = UserSerializer()

    class Meta:
        model = Transaction
        fields = ['id', 'transaction_date', 'updated_date', 'started_price', 'last_price', 'item', 'user_buy']
