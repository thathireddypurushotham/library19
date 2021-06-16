from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User
from django.db.models.signals import post_save



class User(AbstractUser):
	t = (
		(1,'student'),
		(2,'guest'),
		(3,'Staff'),
		)
	r=[('CSE','CSE'),('ECE','ECE'),('CIVIL','CIVIL'),('Mechanical','Mechanical'),('EEE','EEE'),('MBA','MBA')]
	role = models.IntegerField(default=2,choices=t)
	g=[('M',"Male"),('F','Female')]
	age=models.IntegerField(default=10)
	gender=models.CharField(max_length=10,choices=g,default="F")
	impf=models.ImageField(upload_to='profiles/',default="profile.jpg")
	Rg_No=models.CharField(max_length=120,default="")
	Branch=models.CharField(choices=r,max_length=120,default="")
	phone_no=models.CharField(null=True,default="1234567890",max_length=10)
	address=models.CharField(max_length=200,default="Tirupathi")



# Create your models here.
class ComplaintBox(models.Model):
	p_name=models.CharField(max_length=120)
	p_email=models.EmailField(max_length=120)
	p_complaint=models.CharField(max_length=10000)

class st_admin_data(models.Model):
	Rg_No=models.CharField(max_length=120)
	Branch=models.CharField(max_length=120)
	Name=models.CharField(max_length=120)
	issue_status=models.IntegerField(default=0)
	Book_name=models.CharField(max_length=120)
	Book_author=models.CharField(max_length=120)
	Book_Edition=models.CharField(max_length=120,default="")
	Book_count=models.IntegerField(default=0)
	Issue_date=models.DateField(blank=True,null=True)
	Expire_date=models.DateField(blank=True,null=True)
	Return_Date=models.DateField(blank=True,null=True)
	Fine=models.IntegerField(default=0)

	uid=models.ForeignKey(User,on_delete=models.CASCADE)

# @receiver(post_save,sender=User)
# def CreateProfile(sender,instance,created,**kwargs):
# 	if created:
# 		st_admin_data.objects.create(uid=instance)
	#p_subject=models.CharField(max_length=100)
	#p_body=models.CharField(max_length=1000)
class Books_Avail(models.Model):
	Book_name=models.CharField(max_length=120, unique=True)
	def __str__(self):
			return self.Book_name
	class Meta:
		db_table ="Library_App_books_avail"

	Book_author=models.CharField(max_length=120,default="")
	Book_Edition=models.CharField(max_length=120,default="")
	Book_Category=models.CharField(max_length=120,default="")
	Book_count=models.IntegerField(default=0)
	Book_Updatedcount=models.IntegerField(default=0)
	Book_Rem=models.IntegerField(default=0)
	Book_Enterdate=models.DateField(blank=True,null=True)
	Time=models.CharField(max_length=120,default="")

	


class ImProfile(models.Model):
	g = [('M',"Male"),('F','Female')]
	age = models.IntegerField(default=10)
	impf = models.ImageField(upload_to='Profiles/',default="profile.png")
	gender = models.CharField(max_length=10,choices=g,default="Male")
	uid = models.OneToOneField(User,on_delete=models.CASCADE)