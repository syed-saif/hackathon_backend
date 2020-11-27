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
        fields = ('id', 'name', 'created_by', 'last_updated_by', 'image', 'is_correct')

    def create(self, validated_data):
        detect_handwritten = models.DetecHandWritten.objects.create(**validated_data)
        success, is_correct = helpers.detect_handwritten_image(detect_handwritten)
        if success:
            detect_handwritten.is_correct = is_correct
            detect_handwritten.save()
        else:
            msg="Not able to parse this image. Try again with some other image"
            detect_handwritten.delete()
            raise serializers.ValidationError({
                'message': msg
            })
        return detect_handwritten

    def to_representation(self, instance):
        data = super(DetectHandWrittenSerializer, self).to_representation(instance)
        if instance.image:
            data['image'] = self.context['request'].build_absolute_uri(instance.image.url)
        else:
            data['image'] = None
        return data