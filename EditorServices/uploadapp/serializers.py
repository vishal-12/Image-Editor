
from rest_framework import serializers
from uploadapp.models import BgFileToolModel

class BgFileSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    file_ext = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()


    class Meta():
        model = BgFileToolModel
        fields = ('id',
                  'name',
                  'file',
                  'url',
                  'file_ext',
                  'content_type',
                  'created_at'
        )

    def get_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.file.url
        return request.build_absolute_uri(photo_url)

    def get_file_ext(self,obj):
        return obj.extension()

    def get_content_type(self,obj):
        return obj.file_type()

    def get_name(self, obj):
        return obj.name
