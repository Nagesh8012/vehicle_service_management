from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.db.models import Sum, Q
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.contrib.auth import logout
from django.template.loader import get_template
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from vehicle import models



def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'vehicle/index.html')


#for showing signup/login button for customer
def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'vehicle/customerclick.html')

#for showing signup/login button for staff
def staffclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'vehicle/staffclick.html')


#for showing signup/login button for ADMIN(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


def customer_signup_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request,'vehicle/customersignup.html',context=mydict)


def staff_signup_view(request):
    userForm=forms.StaffUserForm()
    staffForm=forms.StaffForm()
    mydict={'userForm':userForm,'staffForm':staffForm}
    if request.method=='POST':
        userForm=forms.StaffUserForm(request.POST)
        staffForm=forms.StaffForm(request.POST,request.FILES)
        if userForm.is_valid() and staffForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            staff=staffForm.save(commit=False)
            staff.user=user
            staff.save()
            my_staff_group = Group.objects.get_or_create(name='STAFF')
            my_staff_group[0].user_set.add(user)
        return HttpResponseRedirect('stafflogin')
    return render(request,'vehicle/staffsignup.html',context=mydict)


#for checking user customer, staff or admin(by sumit)
def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()
def is_staff(user):
    return user.groups.filter(name='STAFF').exists()


def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('customer-dashboard')
    elif is_staff(request.user):
        accountapproval=models.Staff.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('staff-dashboard')
        else:
            return render(request,'vehicle/staff_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')



#============================================================================================
# ADMIN RELATED views start
#============================================================================================

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    dict={
    'total_customer':models.Customer.objects.all().count(),
    'total_staff':models.Staff.objects.all().count(),
    'total_request':models.Request.objects.all().count(),
    'total_feedback':models.Feedback.objects.all().count(),
    'data':zip(customers,enquiry),
    }
    return render(request,'vehicle/admin_dashboard.html',context=dict)


@login_required(login_url='adminlogin')
def admin_customer_view(request):
    return render(request,'vehicle/admin_customer.html')

@login_required(login_url='adminlogin')
def admin_view_customer_view(request):
    customers=models.Customer.objects.all()
    return render(request,'vehicle/admin_view_customer.html',{'customers':customers})


@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('admin-view-customer')


@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,request.FILES,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('admin-view-customer')
    return render(request,'vehicle/update_customer.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_add_customer_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('/admin-view-customer')
    return render(request,'vehicle/admin_add_customer.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_view_customer_enquiry_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    return render(request,'vehicle/admin_view_customer_enquiry.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminlogin')
def admin_view_customer_invoice_view(request):
    enquiry=models.Request.objects.values('customer_id').annotate(Sum('cost'))
    print(enquiry)
    customers=[]
    for enq in enquiry:
        print(enq)
        customer=models.Customer.objects.get(id=enq['customer_id'])
        customers.append(customer)
    return render(request,'vehicle/admin_view_customer_invoice.html',{'data':zip(customers,enquiry)})

@login_required(login_url='adminlogin')
def admin_staff_view(request):
    return render(request,'vehicle/admin_staff.html')


@login_required(login_url='adminlogin')
def admin_approve_staff_view(request):
    staff=models.Staff.objects.all().filter(status=False)
    return render(request,'vehicle/admin_approve_staff.html',{'staff':staff})

@login_required(login_url='adminlogin')
def approve_staff_view(request,pk):
    staffSalary=forms.StaffSalaryForm()
    if request.method=='POST':
        staffSalary=forms.StaffSalaryForm(request.POST)
        if staffSalary.is_valid():
            staff=models.Staff.objects.get(id=pk)
            staff.salary=staffSalary.cleaned_data['salary']
            staff.status=True
            staff.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-approve-staff')
    return render(request,'vehicle/admin_approve_staff_details.html',{'staffSalary':staffSalary})


@login_required(login_url='adminlogin')
def delete_staff_view(request,pk):
    staff=models.Staff.objects.get(id=pk)
    user=models.User.objects.get(id=staff.user_id)
    user.delete()
    staff.delete()
    return redirect('admin-approve-staff')


@login_required(login_url='adminlogin')
def admin_add_staff_view(request):
    userForm=forms.StaffUserForm()
    staffForm=forms.StaffForm()
    staffSalary=forms.StaffSalaryForm()
    mydict={'userForm':userForm,'staffForm':staffForm,'staffSalary':staffSalary}
    if request.method=='POST':
        userForm=forms.StaffUserForm(request.POST)
        staffForm=forms.StaffForm(request.POST,request.FILES)
        staffSalary=forms.StaffSalaryForm(request.POST)
        if userForm.is_valid() and staffForm.is_valid() and staffSalary.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            staff=staffForm.save(commit=False)
            staff.user=user
            staff.status=True
            staff.salary=staffSalary.cleaned_data['salary']
            staff.save()
            my_staff_group = Group.objects.get_or_create(name='STAFF')
            my_staff_group[0].user_set.add(user)
            return HttpResponseRedirect('admin-view-staff')
        else:
            print('problem in form')
    return render(request,'vehicle/admin_add_staff.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_view_staff_view(request):
    staff=models.Staff.objects.all()
    return render(request,'vehicle/admin_view_staff.html',{'staff':staff})


@login_required(login_url='adminlogin')
def delete_staff_view(request,pk):
    staff=models.Staff.objects.get(id=pk)
    user=models.User.objects.get(id=staff.user_id)
    user.delete()
    staff.delete()
    return redirect('admin-view-staff')


@login_required(login_url='adminlogin')
def update_staff_view(request,pk):
    staff=models.Staff.objects.get(id=pk)
    user=models.User.objects.get(id=staff.user_id)
    userForm=forms.StaffUserForm(instance=user)
    staffForm=forms.StaffForm(request.FILES,instance=staff)
    mydict={'userForm':userForm,'staffForm':staffForm}
    if request.method=='POST':
        userForm=forms.StaffUserForm(request.POST,instance=user)
        staffForm=forms.StaffForm(request.POST,request.FILES,instance=staff)
        if userForm.is_valid() and staffForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            staffForm.save()
            return redirect('admin-view-staff')
    return render(request,'vehicle/update_staff.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_view_staff_salary_view(request):
    staff=models.Staff.objects.all()
    return render(request,'vehicle/admin_view_staff_salary.html',{'staff':staff})

@login_required(login_url='adminlogin')
def update_salary_view(request,pk):
    staffSalary=forms.StaffSalaryForm()
    if request.method=='POST':
        staffSalary=forms.StaffSalaryForm(request.POST)
        if staffSalary.is_valid():
            staff=models.Staff.objects.get(id=pk)
            staff.salary=staffSalary.cleaned_data['salary']
            staff.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-staff-salary')
    return render(request,'vehicle/admin_approve_staff_details.html',{'staffSalary':staffSalary})


@login_required(login_url='adminlogin')
def admin_request_view(request):
    return render(request,'vehicle/admin_request.html')

@login_required(login_url='adminlogin')
def admin_view_request_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    return render(request,'vehicle/admin_view_request.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminlogin')
def change_status_view(request,pk):
    adminenquiry=forms.AdminApproveRequestForm()
    if request.method=='POST':
        adminenquiry=forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.staff=adminenquiry.cleaned_data['staff']
            enquiry_x.cost=adminenquiry.cleaned_data['cost']
            enquiry_x.status=adminenquiry.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-request')
    return render(request,'vehicle/admin_approve_request_details.html',{'adminenquiry':adminenquiry})


@login_required(login_url='adminlogin')
def admin_delete_request_view(request,pk):
    requests=models.Request.objects.get(id=pk)
    requests.delete()
    return redirect('admin-view-request')



@login_required(login_url='adminlogin')
def admin_add_request_view(request):
    enquiry=forms.RequestForm()
    adminenquiry=forms.AdminRequestForm()
    mydict={'enquiry':enquiry,'adminenquiry':adminenquiry}
    if request.method=='POST':
        enquiry=forms.RequestForm(request.POST)
        adminenquiry=forms.AdminRequestForm(request.POST)
        if enquiry.is_valid() and adminenquiry.is_valid():
            enquiry_x=enquiry.save(commit=False)
            enquiry_x.customer=adminenquiry.cleaned_data['customer']
            enquiry_x.staff=adminenquiry.cleaned_data['staff']
            enquiry_x.cost=adminenquiry.cleaned_data['cost']
            enquiry_x.status='Approved'
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('admin-view-request')
    return render(request,'vehicle/admin_add_request.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_approve_request_view(request):
    enquiry=models.Request.objects.all().filter(status='Pending')
    return render(request,'vehicle/admin_approve_request.html',{'enquiry':enquiry})

@login_required(login_url='adminlogin')
def approve_request_view(request,pk):
    adminenquiry=forms.AdminApproveRequestForm()
    if request.method=='POST':
        adminenquiry=forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.staff=adminenquiry.cleaned_data['staff']
            enquiry_x.cost=adminenquiry.cleaned_data['cost']
            enquiry_x.status=adminenquiry.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-approve-request')
    return render(request,'vehicle/admin_approve_request_details.html',{'adminenquiry':adminenquiry})




@login_required(login_url='adminlogin')
def admin_view_service_cost_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    print(customers)
    return render(request,'vehicle/admin_view_service_cost.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminlogin')
def update_cost_view(request,pk):
    updateCostForm=forms.UpdateCostForm()
    if request.method=='POST':
        updateCostForm=forms.UpdateCostForm(request.POST)
        if updateCostForm.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.cost=updateCostForm.cleaned_data['cost']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-service-cost')
    return render(request,'vehicle/update_cost.html',{'updateCostForm':updateCostForm})



@login_required(login_url='adminlogin')
def admin_staff_attendance_view(request):
    return render(request,'vehicle/admin_staff_attendance.html')


@login_required(login_url='adminlogin')
def admin_take_attendance_view(request):
    staff=models.Staff.objects.all().filter(status=True)
    aform=forms.AttendanceForm()
    if request.method=='POST':
        form=forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel=models.Attendance()
                
                AttendanceModel.date=date
                AttendanceModel.present_status=Attendances[i]
                print(staff[i].id)
                print(int(staff[i].id))
                staff=models.Staff.objects.get(id=int(staff[i].id))
                AttendanceModel.staff=staff
                AttendanceModel.save()
            return redirect('admin-view-attendance')
        else:
            print('form invalid')
    return render(request,'vehicle/admin_take_attendance.html',{'staff':staff,'aform':aform})

@login_required(login_url='adminlogin')
def admin_view_attendance_view(request):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            attendancedata=models.Attendance.objects.all().filter(date=date)
            staffdata=models.Staff.objects.all().filter(status=True)
            mylist=zip(attendancedata,staffdata)
            return render(request,'vehicle/admin_view_attendance_page.html',{'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'vehicle/admin_view_attendance_ask_date.html',{'form':form})

@login_required(login_url='adminlogin')
def admin_report_view(request):
    reports=models.Request.objects.all().filter(Q(status="Repairing Done") | Q(status="Released"))
    dict={
        'reports':reports,
    }
    return render(request,'vehicle/admin_report.html',context=dict)


@login_required(login_url='adminlogin')
def admin_feedback_view(request):
    feedback=models.Feedback.objects.all().order_by('-id')
    return render(request,'vehicle/admin_feedback.html',{'feedback':feedback})

#============================================================================================
# ADMIN RELATED views END
#============================================================================================


#============================================================================================
# CUSTOMER RELATED views start
#============================================================================================

from django.shortcuts import render
from django.db.models import Count, Sum
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from . import models
import json

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_dashboard_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    
    # Request Status Distribution for Pie Chart
    status_data = models.Request.objects.filter(customer=customer).values('status').annotate(count=Count('status'))
    status_labels = [entry['status'] for entry in status_data]
    status_counts = [entry['count'] for entry in status_data]

    # Monthly Requests for Bar Chart
    monthly_data = models.Request.objects.filter(customer=customer).values_list('date__month').annotate(count=Count('id'))
    months = [entry[0] for entry in monthly_data]
    request_counts = [entry[1] for entry in monthly_data]

    # Cost Distribution for Donut Chart
    cost_data = models.Request.objects.filter(customer=customer).values('status').annotate(total_cost=Sum('cost'))
    cost_labels = [entry['status'] for entry in cost_data]
    cost_values = [entry['total_cost'] for entry in cost_data]

    dict = {
        'work_in_progress': models.Request.objects.filter(customer=customer, status='Repairing').count(),
        'work_completed': models.Request.objects.filter(customer=customer).filter(Q(status="Repairing Done") | Q(status="Released")).count(),
        'new_request_made': models.Request.objects.filter(customer=customer).filter(Q(status="Pending") | Q(status="Approved")).count(),
        'bill': models.Request.objects.filter(customer=customer).filter(Q(status="Repairing Done") | Q(status="Released")).aggregate(Sum('cost'))['cost__sum'],
        'customer': customer,
        'status_labels': json.dumps(status_labels),
        'status_counts': json.dumps(status_counts),
        'months': json.dumps(months),
        'request_counts': json.dumps(request_counts),
        'cost_labels': json.dumps(cost_labels),
        'cost_values': json.dumps(cost_values),
    }
    
    return render(request, 'vehicle/customer_dashboard.html', context=dict)



@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'vehicle/customer_request.html',{'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id , status="Pending")
    return render(request,'vehicle/customer_view_request.html',{'customer':customer,'enquiries':enquiries})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_delete_request_view(request,pk):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiry=models.Request.objects.get(id=pk)
    enquiry.delete()
    return redirect('customer-view-request')

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_approved_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'vehicle/customer_view_approved_request.html',{'customer':customer,'enquiries':enquiries})

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_approved_request_invoice_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'vehicle/customer_view_approved_request_invoice.html',{'customer':customer,'enquiries':enquiries})



@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_add_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiry=forms.RequestForm()
    if request.method=='POST':
        enquiry=forms.RequestForm(request.POST)
        if enquiry.is_valid():
            customer=models.Customer.objects.get(user_id=request.user.id)
            enquiry_x=enquiry.save(commit=False)
            enquiry_x.customer=customer
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('customer-dashboard')
    return render(request,'vehicle/customer_add_request.html',{'enquiry':enquiry,'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'vehicle/customer_profile.html',{'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def edit_customer_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm,'customer':customer}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('customer-profile')
    return render(request,'vehicle/edit_customer_profile.html',context=mydict)


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_invoice_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'vehicle/customer_invoice.html',{'customer':customer,'enquiries':enquiries})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_feedback_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    feedback=forms.FeedbackForm()
    if request.method=='POST':
        feedback=forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request,'vehicle/feedback_sent_by_customer.html',{'customer':customer})
    return render(request,'vehicle/customer_feedback.html',{'feedback':feedback,'customer':customer})



from io import BytesIO
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from vehicle.models import Request, Customer , Staff

@login_required(login_url='customerlogin')
@user_passes_test(lambda user: hasattr(user, 'customer'))  # Ensure only customers access
def generate_invoice_pdf(request, request_id):
    try:
        enquiry = Request.objects.get(id=request_id, customer__user=request.user)
    except Request.DoesNotExist:
        return HttpResponse("Unauthorized")

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=50, rightMargin=50, topMargin=60, bottomMargin=50)
    elements = []  # List to store PDF elements

    styles = getSampleStyleSheet()
    primary_color = colors.HexColor("#2E86C1")  # Blue
    
    # **Title**
    title = Paragraph("<b><font size=30 color='#2E86C1'>VEHICLE SERVICE INVOICE</font></b>", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 80))
    

    # **Invoice Info**
    invoice_data = [
        ["Invoice ID:", f"INV-{enquiry.id}", "Date:", enquiry.date.strftime('%d-%m-%Y')],
    ]
    invoice_table = Table(invoice_data, colWidths=[60, 150, 30, 150])
    invoice_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
    ]))
    elements.append(invoice_table)
    elements.append(Spacer(1, 40))

    # **Customer Details (Expanded)**
    customer = enquiry.customer  # Fetch customer details
    customer_data = [
        ["Customer Name:", customer.user.get_full_name()],
        ["Email:", customer.email],
        ["Phone:", customer.mobile],
        ["Address:", customer.address],
    ]
    customer_table = Table(customer_data, colWidths=[150, 300])
    customer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), primary_color),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(customer_table)
    elements.append(Spacer(1, 60))

    # **Vehicle Details**
    staff_name = enquiry.staff.user.get_full_name() if enquiry.staff else "Not Assigned"
    vehicle_data = [
        ["Vehicle Category:", enquiry.category],
        ["Vehicle Name:", enquiry.vehicle_name],
        ["Vehicle Number:", enquiry.vehicle_no],
        ["Vehicle Model:", enquiry.vehicle_model],
        ["Vehicle Brand:", enquiry.vehicle_brand],
        ["Problem Description:", enquiry.problem_description],
        ["Assigned Staff:", staff_name]
        
    ]
    vehicle_table = Table(vehicle_data, colWidths=[150, 300])
    vehicle_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), primary_color),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(vehicle_table)
    elements.append(Spacer(1, 20))

    # **Service Cost**
    cost_data = [
        ["Service Cost:", f"₹ {enquiry.cost}"]
    ]
    cost_table = Table(cost_data, colWidths=[150, 300])
    cost_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.red),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(cost_table)
    elements.append(Spacer(1, 40))

    # **Footer**
    footer = Paragraph("<font size=20 color='black'>Thank you for choosing our service !!</font>", styles["Normal"])
    elements.append(footer)
    elements.append(Spacer(1, 20))

    contact_info = Paragraph("<b><font size=15 color='#2E86C1'>For queries, contact us: support@vehicleserviceManagement.com</font></b>", styles["Normal"])
    elements.append(contact_info)

    # **Build PDF**
    doc.build(elements)
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

#============================================================================================
# CUSTOMER RELATED views END
#============================================================================================






#============================================================================================
# STAFF RELATED views start
#============================================================================================


from django.db.models.functions import ExtractMonth
from django.db.models import Count
import json

@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_dashboard_view(request):
    staff = models.Staff.objects.get(user_id=request.user.id)

    work_in_progress = models.Request.objects.filter(staff_id=staff.id, status='Repairing').count()
    work_completed = models.Request.objects.filter(staff_id=staff.id, status='Repairing Done').count()
    new_work_assigned = models.Request.objects.filter(staff_id=staff.id, status='Approved').count()

    # Work status breakdown for Pie Chart
    status_labels = ['New Assigned', 'In Progress', 'Completed']
    status_counts = [new_work_assigned, work_in_progress, work_completed]

    # Monthly Repairs for Bar Chart
    monthly_repair_data = models.Request.objects.filter(staff_id=staff.id).annotate(
        month=ExtractMonth('date')  
    ).values('month').annotate(count=Count('id')).order_by('month')

    months = [entry['month'] for entry in monthly_repair_data]
    request_counts = [entry['count'] for entry in monthly_repair_data]

    # Salary Distribution for Donut Chart (Assuming staff have varying salaries)
    salary_labels = ['Current Salary']
    salary_values = [staff.salary]

    context = {
        'work_in_progress': work_in_progress,
        'work_completed': work_completed,
        'new_work_assigned': new_work_assigned,
        'salary': staff.salary,
        'staff': staff,
        'status_labels': json.dumps(status_labels),
        'status_counts': json.dumps(status_counts),
        'months': json.dumps(months),
        'request_counts': json.dumps(request_counts),
        'salary_labels': json.dumps(salary_labels),
        'salary_values': json.dumps(salary_values),
    }

    return render(request, 'vehicle/staff_dashboard.html', context)


@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_work_assigned_view(request):
    staff=models.Staff.objects.get(user_id=request.user.id)
    works=models.Request.objects.all().filter(staff_id=staff.id)
    return render(request,'vehicle/staff_work_assigned.html',{'works':works,'staff':staff})


@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_update_status_view(request,pk):
    staff=models.Staff.objects.get(user_id=request.user.id)
    updateStatus=forms.StaffUpdateStatusForm()
    if request.method=='POST':
        updateStatus=forms.StaffUpdateStatusForm(request.POST)
        if updateStatus.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.status=updateStatus.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/staff-work-assigned')
    return render(request,'vehicle/staff_update_status.html',{'updateStatus':updateStatus,'staff':staff})

@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_attendance_view(request):
    staff=models.Staff.objects.get(user_id=request.user.id)
    attendaces=models.Attendance.objects.all().filter(staff=staff)
    return render(request,'vehicle/staff_view_attendance.html',{'attendaces':attendaces,'staff':staff})





@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_feedback_view(request):
    staff=models.Staff.objects.get(user_id=request.user.id)
    feedback=forms.FeedbackForm()
    if request.method=='POST':
        feedback=forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request,'vehicle/feedback_sent.html',{'staff':staff})
    return render(request,'vehicle/staff_feedback.html',{'feedback':feedback,'staff':staff})

@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_salary_view(request):
    staff=models.Staff.objects.get(user_id=request.user.id)
    workdone=models.Request.objects.all().filter(staff_id=staff.id).filter(Q(status="Repairing Done") | Q(status="Released"))
    return render(request,'vehicle/staff_salary.html',{'workdone':workdone,'staff':staff})

@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_profile_view(request):
    staff=models.Staff.objects.get(user_id=request.user.id)
    return render(request,'vehicle/staff_profile.html',{'staff':staff})

@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def edit_staff_profile_view(request):
    staff=models.Staff.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=staff.user_id)
    userForm=forms.StaffUserForm(instance=user)
    staffForm=forms.StaffForm(request.FILES,instance=staff)
    mydict={'userForm':userForm,'staffForm':staffForm,'staff':staff}
    if request.method=='POST':
        userForm=forms.StaffUserForm(request.POST,instance=user)
        staffForm=forms.StaffForm(request.POST,request.FILES,instance=staff)
        if userForm.is_valid() and staffForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            staffForm.save()
            return redirect('staff-profile')
    return render(request,'vehicle/edit_staff_profile.html',context=mydict)






#============================================================================================
# STAFF RELATED views start
#============================================================================================




# for aboutus and contact
def aboutus_view(request):
    return render(request,'vehicle/aboutus.html')

from django.core.mail import send_mail

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'vehicle/contactussuccess.html')
    return render(request, 'vehicle/contactus.html', {'form':sub})


def logout_view(request):
    logout(request)
    return redirect('/')

