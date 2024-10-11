from rest_framework import generics
from .models import *
from Bank.models import Soal
from Bank.models import *
from auth_user.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework import status
from django.utils.crypto import get_random_string
from django.db.models import Count ,Q
from django.shortcuts import get_object_or_404
from .serializers import *
from Bank.views import SoalView


class Classview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self ,request):
        my_user = request.user
        name = request.data.get('name')
        description = request.data.get('description')
        capacity = request.data.get('capacity')
        permision = request.data.get('permision')
        password = request.data.get('password')
        join_time = request.data.get('join_time')

        if not name and not permision:
            return Response({'required':['name','permision'] ,'optional':['description','capacity','password','join_time']},status=status.HTTP_400_BAD_REQUEST)
        my_forum = Forum.objects.create(name = f"{name} forum")
        my_forum.participents.add(my_user)
        my_class = Classes.objects.create(name=name,description=description,shenase=get_random_string(20),capacity=capacity,
                           permision=permision,password=password,join_time=join_time,forum=my_forum)
        ClassRoles.objects.create(user=my_user, kelas=my_class, role='O')
        my_forum.save()
        return Response({'detail': 'Class created successfully'}, status=status.HTTP_201_CREATED)


    def get(self ,request):
        my_user = request.user
        classes = Classes.objects.filter(classroles__user = my_user)
        serializer = ClassSerializer(classes ,many=True)
        return Response(serializer.data ,status=status.HTTP_200_OK)
    


class ClassDetail(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, shenase):
        my_user = request.user
        my_class = get_object_or_404(Classes ,shenase=shenase ,classroles__user = my_user)
        serializer = ClassSerializer(my_class, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def get(self, request ,shenase):
        my_user = request.user
        my_class = get_object_or_404(Classes ,shenase=shenase ,classroles__user = my_user)
        serializer = ClassSerializer(my_class)
        return Response(serializer.data , status=status.HTTP_200_OK)



class JoinClass(APIView):
    permission_classes = [IsAuthenticated]
    def get(self ,request ,shenase):
        my_user = request.user
        try:
            my_class = Classes.objects.get(shenase=shenase)
        except:
            return Response('class not found' ,status=status.HTTP_404_NOT_FOUND)
        if my_class.permision == 'pri':
            return Response('this class is private' ,status=status.HTTP_403_FORBIDDEN)
        if ClassRoles.objects.filter(kelas=my_class ,user=my_user).exists():
            return Response('you are already in this class' ,status=status.HTTP_403_FORBIDDEN)
        my_class.forum.participents.add(my_user)

        ClassRoles.objects.create(kelas=my_class ,user=my_user ,role='S')
        my_class.save()

        return Response('you joined the class successfully' ,status=status.HTTP_200_OK)


    def post(self ,request ,shenase):
        my_user = request.user
        password = request.data.get('password')
        if not password:
            return Response('password is required' ,status=status.HTTP_403_FORBIDDEN)
        try:
            my_class = Classes.objects.get(shenase=shenase)
        except:
            return Response('class not found' ,status=status.HTTP_404_NOT_FOUND)
        if my_class.permision == 'pub':
            return Response('post method is not allowed' ,status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if my_class.password != password:
            return Response('wrong password' ,status=status.HTTP_403_FORBIDDEN)

        my_forum = my_class.forum
        my_forum.participents.add(my_user)

        ClassRoles.objects.create(kelas=my_class ,user=my_user ,role='S')
        my_forum.save()
        return Response('you joined the class successfully' ,status=status.HTTP_200_OK)
        
         

class JoinClassByInvitation(APIView):
    permission_classes = [IsAuthenticated]
    def get(self ,request ,invite_id):
        my_user = request.user
        try:
            my_invite = Invite.objects.get(invite_id=invite_id)
        except:
            return Response('invite id is wrong or expired' ,status=status.HTTP_404_NOT_FOUND)
        if my_invite.reciver != my_user:
            return Response('this link is not valid on your account' ,status=status.HTTP_403_FORBIDDEN)
        my_class = my_invite.target_class
        my_forum = my_class.forum
        my_forum.participents.add(my_user)    
        ClassRoles.objects.create(kelas=my_class ,user=my_user ,role='S')
        my_forum.save()
        my_invite.delete()
        return Response('you joined the class successfully' ,status=status.HTTP_200_OK)
    

class SendInvitation(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request ,shenase):
        username_list = request.data.get('username_list')
        my_user = request.user
        my_class = get_object_or_404(Classes ,shenase=shenase)
        if not ClassRoles.objects.filter(kelas=my_class ,user=my_user ,role='O').exists():
            return Response("you dont have permision on this class" ,status=status.HTTP_403_FORBIDDEN)
        if not username_list:
            return Response('username_list field is required' ,status=status.HTTP_403_FORBIDDEN)
        error_log = []
        for item in username_list:
            try:
                user = QueraUser.objects.get(username=item)
            except:
                error_log.append({'user_not_found':{item}})
                continue
            invite_id = get_random_string(20)
            Invite.objects.create(reciver=user,target_class=my_class,invite_id=invite_id)
            email_text = 'http//:127.0.0.1/private/'+invite_id
            #---------------------------------------------------------------------------------------------------------------------------email-
        if error_log:
            return Response(error_log)
        return Response('invitations were sent successfully' ,status=status.HTTP_200_OK)
    

class InClassMessage(APIView):
    permission_classes = [IsAuthenticated]
    def post(self ,request ,shenase):
        my_user = request.user
        text = request.data.get('text')
        my_class = get_object_or_404(Classes ,shenase=shenase)
        my_forum = my_class.forum
        if my_forum.participents.filter(id=my_user.id).exists():
            Message.objects.create(sender=my_user,room=my_forum,text=text)
            return Response('your message was sent',status=status.HTTP_200_OK)
        return Response('you dont have access to the selected chatroom' ,status=status.HTTP_403_FORBIDDEN)
    

class ChatBox(APIView):
    permission_classes = [IsAuthenticated]
    def get(self ,request ,shenase):
        my_user = request.user
        my_class = get_object_or_404(Classes ,shenase=shenase)
        my_forum = my_class.forum
        if my_forum.participents.filter(id=my_user.id).exists():
            return Response(Message.objects.filter(room=my_forum).order_by("send_time").values_list("sender__username","text","send_time") ,status=status.HTTP_200_OK)
        return Response('you dont have access to the selected chatroom' ,status=status.HTTP_403_FORBIDDEN)


class AssignmentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self ,request ,shenase):
        name = request.data.get("name")
        contribution_type = request.data.get("contribution_type")
        marking_type = request.data.get("marking_type")
        if not name or not contribution_type or not marking_type:
            return Response("name , contribution_type and marking_type are required ")
        my_user = request.user
        my_class = get_object_or_404(Classes ,shenase=shenase)
        try:
            if ClassRoles.objects.get(user=my_user, kelas=my_class).role == 'S':
                return Response("students dont have permission to add assignment",status=status.HTTP_403_FORBIDDEN)
        except:
            return Response("no permissions" ,status=status.HTTP_403_FORBIDDEN)
        
        Assignment.objects.create(name=name,contribution_type=contribution_type,marking_type=marking_type,for_class=my_class)
        return Response("assignment added",status=status.HTTP_201_CREATED)
        
    def get(self ,request ,shenase):
        my_user = request.user
        my_class = get_object_or_404(Classes ,shenase=shenase)
        try:
            ClassRoles.objects.get(user=my_user, kelas=my_class)
        except:
            return Response("no permissions" ,status=status.HTTP_403_FORBIDDEN)
        
        assignemnts = Assignment.objects.filter(for_class=my_class)
        serializer = AssignmentSerializer(assignemnts ,many=True)
        return Response(serializer.data ,status=status.HTTP_200_OK)
    

class AddGroup(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self ,request ,shenase):
        group_list = request.data.get('group_list',[])
        assignment_id = request.data.get('assignment_id')

        my_assignment = get_object_or_404(Assignment, id=assignment_id)
        my_user = request.user
        my_class = get_object_or_404(Classes ,shenase=shenase)

        if len(group_list) > 10:
            return Response('maximum number of groups is 10' ,status=status.HTTP_400_BAD_REQUEST)
        if my_assignment.for_class != my_class:
            return Response("no permission", status=status.HTTP_403_FORBIDDEN)
        try:
            if ClassRoles.objects.get(user=my_user ,kelas=my_class).role == 'S':
                return Response("students dont have permission to add group",status=status.HTTP_403_FORBIDDEN)
        except:
            return Response("no permission", status=status.HTTP_403_FORBIDDEN)
        
        combined_lists = [item for lst in group_list for item in lst]
        seen = set()
        duplicates = set()
        try:
            for value in combined_lists:
                if not ClassRoles.objects.filter(user=QueraUser.objects.get(id=value),kelas=my_class,role='S').exists():
                    return Response(f"user {value} is not student of {my_class.name}")
                if value in seen:
                    duplicates.add(value)
                else:
                    seen.add(value)
            if duplicates:
                return Response({"Duplicate values found.": list(duplicates)})
        except:
            return Response(f"no user found with {value} value")

        my_assignment.teams.clear()
        for team in group_list:
            my_team = Team.objects.create()
            students = QueraUser.objects.filter(id__in=team)
            my_assignment.teams.add(my_team.members.add(*students))
            my_assignment.save()
            my_team.save()
        return Response("group was created" ,status=status.HTTP_201_CREATED)
    


class AddQuestionFromBank(APIView):
    permission_classes = [IsAuthenticated]
    def post(self ,request ,shenase):
        assignment_id = request.data.get('assignment_id')
        question_id = request.data.get('question_id')
        deadline = request.data.get('deadline')
        send_limit = request.data.get('send_limit')
        mark = request.data.get('mark')
        late_penalty = request.data.get('late_penalty')

        if not assignment_id or not question_id or not deadline or not send_limit or not mark or not late_penalty:
            return Response("assignment_id , question_id , deadline , send_limit , mark and late_penalty are required")
        my_assignment = get_object_or_404(Assignment, id=assignment_id)
        my_soal =  get_object_or_404(Soal, id=question_id)
        my_user = request.user
        my_class = get_object_or_404(Classes ,shenase=shenase)

        if my_assignment.for_class != my_class:
            return Response("no permission", status=status.HTTP_403_FORBIDDEN)
        try:
            if ClassRoles.objects.get(user=my_user ,kelas=my_class).role == 'S':
                return Response("students dont have permission to add group",status=status.HTTP_403_FORBIDDEN)
        except:
            return Response("no permission", status=status.HTTP_403_FORBIDDEN)
        
        my_question = my_assignment.questions.create(soal=my_soal,deadline=deadline,send_limit=send_limit,mark=mark,late_penalty=late_penalty)
        serializer = QuestionSerializer(my_question)
        return Response(serializer.data ,status=status.HTTP_201_CREATED)
    

class AddCreatedQuestion(APIView):
    permission_classes = [IsAuthenticated]
    def get(self ,request):
        view = SoalView.as_view()
        responce = view(request)
        return Response(responce.data)
                


        




        

    

    


        

    





