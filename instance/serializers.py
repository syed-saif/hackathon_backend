import base64
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from instance import models, helpers


class DetectHandWrittenSerializer(serializers.ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    last_updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image = Base64ImageField(required=False)

    class Meta:
        model = models.DetecHandWritten
        fields = ('id', 'name', 'created_by', 'result', 'status', 'last_updated_by', 'image', 'is_correct')

    def create(self, validated_data):
        detect_handwritten = models.DetecHandWritten.objects.create(**validated_data)
        result, status = helpers.detect_handwritten_image(detect_handwritten)
        detect_handwritten.result = result
        detect_handwritten.status = status
        detect_handwritten.save()
        return detect_handwritten

    def to_representation(self, instance):
        data = super(DetectHandWrittenSerializer, self).to_representation(instance)
        data['created_at'] = instance.created_at
        if instance.image:
            data['image'] = self.context['request'].build_absolute_uri(instance.image.url)
        else:
            data['image'] = None
        return data