from rest_framework import serializers
from .models import CheckManuscriptModel,ReviewManuscriptModel

class CheckManuscriptModelSerializer(serializers.ModelSerializer):
    """
    稿件检测模型序列化
    """
    class Meta:
        model=CheckManuscriptModel
        fields="__all__"

class ReviewManuscriptModelSerializer(serializers.ModelSerializer):
    """
    稿件审核模型序列化
    """
    class Meta:
        model=ReviewManuscriptModel
        fields="__all__"


        