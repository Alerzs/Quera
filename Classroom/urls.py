from django.urls import path
from .views import *


urlpatterns = [
    path('join/<str:shenase>',JoinClass.as_view()),
    path('private/<str:invite_id>',JoinClassByInvitation.as_view()),
    path('message/<str:shenase>',InClassMessage.as_view()),
    path('invite/<str:shenase>' ,SendInvitation.as_view()),
    path('my_class/',Classview.as_view()),
    path('class_detail/<str:shenase>' ,ClassDetail.as_view()),
    path('chat_box/<str:shenase>',ChatBox.as_view()),
    path('assignment/<str:shenase>',AssignmentView.as_view()),
    path('add_group/<str:shenase>' ,AddGroup.as_view()),
    path('add_question/<str:shenase>' ,AddQuestionFromBank.as_view()),
    path('add_create_question/' ,AddCreatedQuestion.as_view()),
]