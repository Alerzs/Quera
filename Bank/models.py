from django.db import models
from auth_user.models import QueraUser
from rest_framework.exceptions import ValidationError

class Soal(models.Model):

    ANSWER_CHOICE = [
        ('F','file'),
        ('C','code'),
        ('T','text')
    ]
    LEVEL_CHOICE =[
        ('E','easy'),
        ('M','medium'),
        ('H','hard')
    ]

    name = models.CharField(max_length=25)
    creator = models.ForeignKey(QueraUser ,on_delete=models.CASCADE)
    category =models.CharField(max_length=20)
    level = models.CharField(max_length=1 ,choices=LEVEL_CHOICE)
    soorat = models.TextField()
    answer_type = models.CharField(max_length=1, choices=ANSWER_CHOICE ,default="C")
    test_case = models.TextField(blank=True ,null=True)
    test_case_answer = models.TextField(blank=True ,null=True)


    def __str__(self) -> str:
        return self.name


    def clean(self) -> None:
        if self.answer_type != 'C' and (self.test_case is not None or self.test_case_answer is not None):
            raise ValidationError('questions with file or text answering type should not have test case')
        if self.answer_type == 'C' and (self.test_case is None or self.test_case_answer is None): 
            raise ValidationError('questions with code answering type should have test case')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class SubmitedAnswer(models.Model):
    user = models.ForeignKey(QueraUser ,on_delete=models.CASCADE)
    soal = models.ForeignKey(Soal ,on_delete=models.CASCADE)
    submited_file = models.FileField(blank=True ,null=True)
    submited_code = models.TextField(blank=True ,null=True)
    submited_text = models.TextField(blank=True ,null=True)
    result = models.TextField(editable=False ,blank=True ,null=True)
    

    def clean(self) -> None:
        if self.soal.answer_type == 'C' and (self.submited_file is not None or self.submited_text is not None):
            raise ValidationError("code answering type needs submited_code only")
        if self.soal.answer_type == 'F' and (self.submited_code is not None or self.submited_text is not None):
            raise ValidationError("file answering type needs submited_file only")
        if self.soal.answer_type == 'T' and (self.submited_file is not None or self.submited_code is not None):
            raise ValidationError("text answering type needs submited_text only")
    
    def save(self, *args, **kwargs):
        self.clean()
        # api to a site and put the results in self.results fields
        super().save(*args, **kwargs)







