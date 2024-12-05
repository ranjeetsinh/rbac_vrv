from rest_framework import serializers
from .models import CustomUser, Profile, Task
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'date_of_birth', 'phone_number']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'summary', 'remind_at', 'created_by', 'created_by_system', 'is_complete', 'created_at', 'assignee']


    def create(self, validated_data):
        request = self.context.get('request')
        assignee = CustomUser.objects.filter(id=validated_data['assignee']).first()
        if assignee:
            other_tasks_for_same_time = Task.objects.filter(
            assignee_id=assignee, remind_at=validated_data['remind_at']
            )

            if other_tasks_for_same_time.exists():
                raise BaseException(
                        409, 'You have another task to complete at the same time. Please choose a different timestamp.' 
                )
                
        return Task.objects.create(**validated_data, created_by=request.user)
