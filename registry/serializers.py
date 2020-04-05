from rest_framework import serializers


class CreateUserSerializer(serializers.Serializer):
    firstNames = serializers.CharField()
    middleNames = serializers.CharField()
    lastNames = serializers.CharField()

    birthDate = serializers.DateField()
    email = serializers.EmailField()

    memberType = serializers.ChoiceField(choices=['alum', 'friend', 'faculty'])
    memberTier = serializers.ChoiceField(choices=['starter', 'regular', 'patron'])

    tos = serializers.BooleanField(required=True)


    def create(self, validated_data):
        return validated_data