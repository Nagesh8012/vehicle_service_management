"""
vehicle
"""
from django.contrib import admin
from django.urls import path
from vehicle import views
from django.contrib.auth.views import LoginView,LogoutView

class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post']

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.home_view,name=''),

    path('adminclick', views.adminclick_view),
    path('customerclick', views.customerclick_view),
    path('staffclick', views.staffclick_view),

    path('customersignup', views.customer_signup_view,name='customersignup'),
    path('staffsignup', views.staff_signup_view,name='staffsignup'),

    path('customerlogin', LoginView.as_view(template_name='vehicle/customerlogin.html'),name='customerlogin'),
    path('stafflogin', LoginView.as_view(template_name='vehicle/stafflogin.html'),name='stafflogin'),
    path('adminlogin', LoginView.as_view(template_name='vehicle/adminlogin.html'),name='adminlogin'),



    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-customer', views.admin_customer_view,name='admin-customer'),
    path('admin-view-customer',views.admin_view_customer_view,name='admin-view-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),
    path('admin-add-customer', views.admin_add_customer_view,name='admin-add-customer'),
    path('admin-view-customer-enquiry', views.admin_view_customer_enquiry_view,name='admin-view-customer-enquiry'),
    path('admin-view-customer-invoice', views.admin_view_customer_invoice_view,name='admin-view-customer-invoice'),


    path('admin-request', views.admin_request_view,name='admin-request'),
    path('admin-view-request',views.admin_view_request_view,name='admin-view-request'),
    path('change-status/<int:pk>', views.change_status_view,name='change-status'),
    path('admin-delete-request/<int:pk>', views.admin_delete_request_view,name='admin-delete-request'),
    path('admin-add-request',views.admin_add_request_view,name='admin-add-request'),
    path('admin-approve-request',views.admin_approve_request_view,name='admin-approve-request'),
    path('approve-request/<int:pk>', views.approve_request_view,name='approve-request'),
    
    path('admin-view-service-cost',views.admin_view_service_cost_view,name='admin-view-service-cost'),
    path('update-cost/<int:pk>', views.update_cost_view,name='update-cost'),

    path('admin-staff', views.admin_staff_view,name='admin-staff'),
    path('admin-view-staff',views.admin_view_staff_view,name='admin-view-staff'),
    path('delete-staff/<int:pk>', views.delete_staff_view,name='delete-staff'),
    path('update-staff/<int:pk>', views.update_staff_view,name='update-staff'),
    path('admin-add-staff',views.admin_add_staff_view,name='admin-add-staff'),
    path('admin-approve-staff',views.admin_approve_staff_view,name='admin-approve-staff'),
    path('approve-staff/<int:pk>', views.approve_staff_view,name='approve-staff'),
    path('delete-staff/<int:pk>', views.delete_staff_view,name='delete-staff'),
    path('admin-view-staff-salary',views.admin_view_staff_salary_view,name='admin-view-staff-salary'),
    path('update-salary/<int:pk>', views.update_salary_view,name='update-salary'),

    path('admin-staff-attendance', views.admin_staff_attendance_view,name='admin-staff-attendance'),
    path('admin-take-attendance', views.admin_take_attendance_view,name='admin-take-attendance'),
    path('admin-view-attendance', views.admin_view_attendance_view,name='admin-view-attendance'),
    path('admin-feedback', views.admin_feedback_view,name='admin-feedback'),

    path('admin-report', views.admin_report_view,name='admin-report'),

    path('staff-dashboard', views.staff_dashboard_view,name='staff-dashboard'),
    path('staff-work-assigned', views.staff_work_assigned_view,name='staff-work-assigned'),
    path('staff-update-status/<int:pk>', views.staff_update_status_view,name='staff-update-status'),
    path('staff-feedback', views.staff_feedback_view,name='staff-feedback'),
    path('staff-salary', views.staff_salary_view,name='staff-salary'),
    path('staff-profile', views.staff_profile_view,name='staff-profile'),
    path('edit-staff-profile', views.edit_staff_profile_view,name='edit-staff-profile'),

    path('staff-attendance', views.staff_attendance_view,name='staff-attendance'),



    path('customer-dashboard', views.customer_dashboard_view,name='customer-dashboard'),
    path('customer-request', views.customer_request_view,name='customer-request'),
    path('customer-add-request',views.customer_add_request_view,name='customer-add-request'),

    path('customer-profile', views.customer_profile_view,name='customer-profile'),
    path('edit-customer-profile', views.edit_customer_profile_view,name='edit-customer-profile'),
    path('customer-feedback', views.customer_feedback_view,name='customer-feedback'),
    path('customer-invoice', views.customer_invoice_view,name='customer-invoice'),
    path('customer-view-request',views.customer_view_request_view,name='customer-view-request'),
    path('customer-delete-request/<int:pk>', views.customer_delete_request_view,name='customer-delete-request'),
    path('customer-view-approved-request',views.customer_view_approved_request_view,name='customer-view-approved-request'),
    path('customer-view-approved-request-invoice',views.customer_view_approved_request_invoice_view,name='customer-view-approved-request-invoice'),


    path('generate-invoice-pdf/<int:request_id>/', views.generate_invoice_pdf, name='generate-invoice-pdf'),
   
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout/', views.logout_view, name='logout'),

    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),
]
