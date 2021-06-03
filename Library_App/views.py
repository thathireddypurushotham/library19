
from django.shortcuts import render,redirect
from Library_App.forms import UsForm,ComplaintForm,UtupForm,ChPwdForm,Books_AvailForm,Books_AvailForm_admin,Expire_date,Usperm,ImForm
from django.core.mail import send_mail
from Library import settings
from django.contrib import messages
from django.contrib.auth.models import User
from Library_App.models import Books_Avail,st_admin_data,AbstractUser,User
from django.contrib.auth.decorators import login_required
import sys
from time import gmtime, strftime
from datetime import date
from django.core import mail
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.http import HttpResponse,JsonResponse



# Create your views here.
def home(rq):
	return render(rq,'html/home.html')

def about(request):
	return render(request,'html/about.html')

def contact(request):
	return render(request,'html/contact.html')

def regi(request):
	if request.method=="POST":
		t=UsForm(request.POST)
		if t.is_valid():
			t.save()
			return redirect('/lg')
	p=UsForm()
	return render(request,'html/register.html',{'u':p})

	
@login_required

def dashboard(rq):
	l=[]
	e2=Books_Avail.objects.all()
	for i in e2:
		l.append(i.Book_Updatedcount-i.Book_count)
	return render(rq,'html/dashboard.html',{'t':e2 ,"a":l})


def profile(request):
	return render(request,'html/profile.html')

def Books(request):
	return render(request,'html/Books.html')

def complaint(request):
	if request.method=="POST":
		data=ComplaintForm(request.POST)
		if data.is_valid():
			subject='Confirmation_Complaint'
			body="Successfully_complainted by "+request.POST['p_name']
			receiver=request.POST['p_email']
			sender=settings.EMAIL_HOST_USER
			send_mail(subject,body,sender,[receiver])
			data.save()
			messages.success(request,"Successfully sent complaint" )
			return redirect('/')
	form=ComplaintForm()
	return render(request,'html/complaint.html',{'p':form})

'''def complaint(request):
	if request.method=="POST":
		subject=request.POST['p_subject']
		body=request.POST['p_body']
		receiver=request.POST['p_email']
		sender=settings.EMAIL_HOST_USER
		send_mail(subject,body,sender,[receiver])
		messages.success(request,"Successfully sent complaint ")
		return redirect('/')
	form=ComplaintForm()
	return render(request,'html/complaint.html',{'p':form})'''
def updf(request):
	if request.method == "POST":
		u=UtupForm(request.POST,instance=request.user)
		i=ImForm(request.POST,request.FILES,instance=request.user)
		if u.is_valid() and i.is_valid():
			u.save()
			i.save()
			return redirect('/pro')
	u=UtupForm(instance=request.user)
	i=ImForm(instance=request.user)
	return render(request,'html/updateprofile.html',{'us':u,"imp":i})

def Bookedit(up,id):
	t= Books_Avail.objects.get(id=id)
	if up.method=="POST":
		d=Books_AvailForm_admin(up.POST,instance=t)
		if d.is_valid():
			d.save()
			return redirect('/ba')
	d=Books_AvailForm_admin(instance=t)
	return render(up,'html/bookupdate.html',{'us':d})
@login_required


def cgf(request):
	if request.method=="POST":
		c=ChPwdForm(user=request.user,data=request.POST)
		if c.is_valid():
			c.save()
			return redirect('/lgo')
	c=ChPwdForm(user=request)
	return render(request,'html/changepassword.html',{'p':c})
def Books_AvailF(rq):
	if rq.method=="POST":
		k=rq.POST['Book_count']
		a=rq.POST['Book_author']
		b=rq.POST['Book_name']
		notes=Books_Avail.objects.all()
		f=0
		for i in notes:
			if i.Book_name==b and i.Book_author==a:
				m=i.Book_count+int(k)
				i.Book_count=m
				i.Book_Updatedcount=i.Book_Updatedcount+int(k)
				i.Books_Rem=i.Book_Updatedcount-i.Book_count
				i.save()
				f=1
		if f==0:
			e=Books_AvailForm_admin(rq.POST)
			if e.is_valid():
				q=e.save(commit=False)
				q.Book_Updatedcount=k
				q.up_id=rq.user.id
				q.save()
	e=Books_AvailForm_admin()
	e2=Books_Avail.objects.all()

	

	return render(rq,"html/Books_Avail.html",{'t':e2,'t1':e})
@login_required
def sendrequest(rq,id):
	k= Books_Avail.objects.get(id=id)
	if rq.method=="POST":
		a=rq.POST['Book_name']
		c=rq.POST['Book_author']
		b=rq.POST['browser']
		if b=='Book_Retrun':
			notes=st_admin_data.objects.filter(Book_name=a)
			for i in notes:
				if i.Book_author==c and i.issue_status==1:

					i.issue_status='3'
					showtime = strftime("%Y-%m-%d")
					print(showtime)
					i.Return_Date=showtime
					l=str(showtime).split("-")
					l1=str(i.Expire_date).split("-")
					d1 = date(int(l[0]), int(l[1]), int(l[2]))
					d0 = date(int(l1[0]), int(l1[1]), int(l1[2]))
					delta = d1 - d0
					i.Fine=delta.days*2
					if i.Fine>0:
						subject='Fine Info'
						body="Hi +{{rq.user.username}}+ Your fine amount is "
						receiver=rq.user.email
						sender=settings.EMAIL_HOST_USER
						t=EmailMessage(subject,body,sender,[receiver])
						t.send()
						return httpResponse(" Successfully_Sent")



					print(delta.days)

					print(l)
					i.save()
					k.save()
		else:
			print(a)
			book_name=[]
			e=Books_AvailForm(rq.POST)
			notes=Books_Avail.objects.all()
			for i in notes:
				if i.Book_name==a:
					k=i.Book_count
			print(book_name)

			if e.is_valid():
				q=e.save(commit=False)
				q.uid_id=rq.user.id
				q.Book_count=k
				q.Name=rq.user.username
				q.Rg_No=rq.user.Rg_No
				q.Branch=rq.user.Branch
				q.save()

		
	e=Books_AvailForm(instance=k)
	return render(rq,"html/sendrequest.html",{'t':e})





def studentbooks_avail(rq):
	e2=Books_Avail.objects.all()
	return render(rq,'html/studentbook_avail.html',{'t':e2})
@login_required
def myreq(req):
	notes=st_admin_data.objects.filter(uid_id=req.user.id)
	return render(req,'html/myres.html',{'data':notes})
def datadelete(req,id):
	obj=st_admin_data.objects.get(id=id)
	obj.delete()
	return redirect('/notipending')
def Bookdelete(req,id):
	obj=Books_Avail.objects.get(id=id)
	obj.delete()
	return redirect('/ba')

@login_required
def viewnt(req):
	accept=st_admin_data.objects.filter(issue_status=1).count()
	allnotes=st_admin_data.objects.all().count()
	re=st_admin_data.objects.filter(issue_status=2).count()
	return render(req,'html/adminpage.html',{'ac':accept,'all':allnotes,'a':re})
def notipending(req):
	pending2=st_admin_data.objects.all()
	data=Books_Avail.objects.filter()
	return render(req,'html/noti_pendingdata.html',{'p':pending2})
def rejecting(req):
	pending2=st_admin_data.objects.all()
	data=Books_Avail.objects.filter()
	return render(req,'html/noti_rejectingdata.html',{'p':pending2})

def accepting(req):
	pending2=st_admin_data.objects.all()
	data=Books_Avail.objects.filter()
	return render(req,'html/noti_acceptingdata.html',{'p':pending2})

def acceptadmin(req,id):
	if req.method=='POST':
		ac=st_admin_data.objects.get(id=id)
		a=req.POST.get('issue')
		b=req.POST.get('Expire')
		ac.Issue_date=a
		ac.Expire_date=b
		ac.save()
		return redirect('/notipending')
	else:
		ac=st_admin_data.objects.get(id=id)
		nam=ac.Book_name
		k=Books_Avail.objects.get(Book_name=nam)
		m=k.Book_count
		if m>0:
			m=m-1
			k.Book_count=m
			ac.Book_count=m
			ac.issue_status='1'
			ac.save()
			k.save()
			return render(req,'html/expiredate.html')
		else:
			ac.issue_status='2'
			ac.save()
		return redirect('/viewn')

def rejectadmin(req,id):
	rc=st_admin_data.objects.get(id=id)
	rc.issue_status='2'
	rc.save()
	return redirect('/viewn')

def books_return(request):
	rc=st_admin_data.objects.all()
	print(rc)
	return render(request,'html/Books_return.html',{'rc':rc})

def issue_book(request):
	rc=st_admin_data.objects.all()
	print(rc)
	return render(request,'html/issue_book.html',{'rc':rc})


def return_accept(rq,id):
	rc=st_admin_data.objects.get(id=id)
	rc.issue_status='4'
	rc.save()
	return redirect('/books_return')
# def requestform(rq):
# 	e2=User.objects.get(id=rq.user.id)
# 	if rq.method=='POST':
# 		print(e2)
# 		e2.Rg_No=rq.POST['rollno']
# 		e2.Branch=rq.POST['dept']
# 		e2.email=rq.POST['email']
# 		e2.address=rq.POST['ad']
# 		e2.phone_no=rq.POST['pn']
# 		e2.save()
# 		return redirect('/lg')
# 	return render(rq,'html/requestp.html')

def requestform(request):
	if request.method=="POST":
		
		e=request.POST.get('email')
		ut=request.POST.get('utype')
		ud=request.POST.get('uid')
		ms=request.POST.get('msg')
		f=request.FILES['fe']
		a="Hi welcome" "Your Requested Dept."  +ut
		t = EmailMessage("UserRole Change",a,settings.EMAIL_HOST_USER,[settings.ADMINS[0][1],e])
	
		t.attach(f.name,f.read(),f.content_type)
		t.send()
		if t==1:
			return redirect('/reqp')
		else:
			return redirect('/lg')



	
	return render(request,'html/requestp.html')
def adminpermissions(request):
	ty=User.objects.all()
	return render(request,'html/adminpermissions.html',{'q':ty})

def updatepermissions(request,k):
	r=User.objects.get(id=k)
	if request.method == "POST":
		k=Usperm(request.POST,instance=r)
		if k.is_valid():
			k.save()
			return redirect('/gper')
	k2= Usperm(instance=r)
	return render(request,'html/updatepermissions.html',{'y':k2})
def books_st_have(rq):
	k2=st_admin_data.objects.filter(uid_id=rq.user.id)
	print(k2)
	return render(rq,'html/books_st_have.html',{'y':k2})


def fine(rq):
	fine1=st_admin_data.objects.all()
	data=Books_Avail.objects.filter()
	return render(rq,'html/fine.html',{'f':fine1})
def autocomplete(rq):
	if 'term' in rq.GET:
		a=data=Books_Avail.objects.filter(Book_author__istartswith=rq.GET.get('term'))
		l=list()
		for i in a:
			l.append(i.Book_author)
		print(l)
		return JsonResponse(l,safe=False)
		







	

