from rest_framework import serializers
from .models import Classes ,ClassRoles ,Assignment ,Question



class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoles
        fields = ['user', 'role']

class ClassSerializer(serializers.ModelSerializer):
    owner_users = serializers.SerializerMethodField()
    teacher_users = serializers.SerializerMethodField()
    mentor_users = serializers.SerializerMethodField()
    student_users = serializers.SerializerMethodField()

    def validate(self, data):
        instance = self.instance

        if instance:
            current_attendent = instance.attendent()
            if 'capacity' in data and data['capacity'] is not None:
                if current_attendent > data['capacity']:
                    raise serializers.ValidationError(f"Capacity cannot be less than the current attendance ({current_attendent}).")
        return data
    

    def get_owner_users(self, obj):
        return RoleSerializer(obj.classroles_set.filter(role='O'), many=True).data

    def get_teacher_users(self, obj):
        return RoleSerializer(obj.classroles_set.filter(role='T'), many=True).data

    def get_mentor_users(self, obj):
        return RoleSerializer(obj.classroles_set.filter(role='M'), many=True).data

    def get_student_users(self, obj):
        return RoleSerializer(obj.classroles_set.filter(role='S'), many=True).data
    
    class Meta:
        model = Classes
        exclude = ["id"]


class AssignmentSerializer(serializers.ModelSerializer):
    
    for_class = serializers.StringRelatedField()
    
    class Meta:
        model = Assignment
        exclude = ["id"]



class QuestionSerializer(serializers.ModelSerializer):

    soal = serializers.StringRelatedField()
    class Meta:
        model = Question
        exclude = ['id']
