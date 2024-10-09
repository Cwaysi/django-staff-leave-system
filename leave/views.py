from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import *
from django.contrib.auth.decorators import login_required
from . models import *
from datetime import datetime, timedelta, date
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from . serializers import LeaveSpentSerializer
from django.db.models import Max, F
from django.core.mail import send_mail
from django.conf import settings
from django.views import View

class BirthdayCelebrantView(View):
    template_name = 'birthday_celebrants.html'

    def get(self, request, *args, **kwargs):
        # Get the start and end date for the current week
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Query the database for users with birthdays in the current week
        birthday_celebrants = CustomUser.objects.filter(
            date_of_birth__range=[start_of_week, end_of_week]
        ).order_by('date_of_birth')

        context = {'birthday_celebrants': birthday_celebrants}
        return render(request, self.template_name, context)


@login_required(login_url='/')
def home (request):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Query the database for users with birthdays in the current week
    birthday_celebrants = CustomUser.objects.filter(
        date_of_birth__range=[start_of_week, end_of_week]
    ).order_by('date_of_birth')
    current_user = request.user
    current_year = datetime.now().year
    total_days_spent = LeaveSpent.objects.filter(user=current_user, year=current_year, leave_type='Annual Leave').aggregate(Sum('days_spent'))['days_spent__sum']
    if not total_days_spent:
        total_days_spent = 0
    total_days_spenty = LeaveSpent.objects.filter(user=current_user, year=current_year).aggregate(Sum('days_spent'))['days_spent__sum']
    if not total_days_spenty:
        total_days_spenty = 0
    posi = request.user.position
    number_of_days_object = Numberofdays.objects.get(leave_type='Annual Leave', position=posi)
    actualdays = number_of_days_object.days
    left = actualdays-total_days_spent
    leave_requests = LeaveRequest.objects.all()
    positio = current_user.position
    department = current_user.department
    context ={
        'department' : department,
        'position': positio,
        'all': total_days_spenty,
        'left': left,
        'year': current_year,
        'days': actualdays,
        'spent': total_days_spent,
        'leave_requests': leave_requests,
        'birthday_celebrants': birthday_celebrants
    }
    return render (request, 'home.html', context)

@login_required
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')  # Replace 'home' with your desired home page URL
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Replace 'home' with your desired home page URL
        else:
            # Display SweetAlert error message
            error_message = "Invalid login credentials. Please try again."
            return render(request, 'login.html', {'form': form, 'error_message': error_message})
    
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='/')
def logout_view(request):
    logout(request)
    return redirect('login')  # Replace 'login' with your login page URL

def count_weekdays(start_date, end_date):
    num_days = 0
    current_date = start_date
    current_year = date.today().year
    holidays = Holidays.objects.filter(year=current_year)
    holidays = [holiday.date for holiday in holidays]
    while current_date <= end_date:
        # Check if the current day is a weekday (Monday to Friday) and not a holiday
        if current_date.weekday() < 5 and current_date not in holidays:
            num_days += 1

        current_date += timedelta(days=1)

    return num_days


@login_required(login_url='/')
def apply(request):
    current_user = request.user
    current_year = datetime.now().year
    total_days_spent = LeaveSpent.objects.filter(user=current_user, year=current_year, leave_type='Annual Leave').aggregate(Sum('days_spent'))['days_spent__sum']
    if not total_days_spent:
        total_days_spent = 0
    total_days_spenty = LeaveSpent.objects.filter(user=current_user, year=current_year).aggregate(Sum('days_spent'))['days_spent__sum']
    if not total_days_spenty:
        total_days_spenty = 0
    posi = request.user.position
    number_of_days_object = Numberofdays.objects.get(leave_type='Annual Leave', position=posi)
    actualdays = number_of_days_object.days
    left = actualdays-total_days_spent
    if request.method == 'POST':
        form = LeaveForm(data=request.POST)
        if form.is_valid():
            user = request.user
            leavetype = form.cleaned_data.get('leave_type')
            relieve = form.cleaned_data.get('relieving_Officer')
            reason= form.cleaned_data.get('reason')
            stat = "Pending"
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            if start_date < datetime.today().date():
                error_message = "Please check your start date, you cannot request leave for past date"
                return render(request, 'apply.html', {'form': form, 'error_message': error_message})
            num_days = count_weekdays(start_date, end_date)
            try:
                posi = request.user.position
                number_of_days_object = Numberofdays.objects.get(leave_type=leavetype, position=posi)
                actualdays = number_of_days_object.days
            except ObjectDoesNotExist:
                # Handle the case where the Numberofdays object does not exist
                actualdays = 1000 

            current_user = request.user
            current_year = datetime.now().year
            total_days_spent = LeaveSpent.objects.filter(user=current_user, year=current_year).aggregate(Sum('days_spent'))['days_spent__sum']
            
            if not total_days_spent:
                total_days_spent = 0
            dysp = total_days_spent + num_days
            if actualdays < num_days :
                error_message = "The number of leave days assigned to '" + leavetype + "' is " + str(actualdays) +"days you cannot apply for " + str(num_days) + "days, please try again"
                return render(request, 'apply.html', {'form': form, 'error_message': error_message})
            elif dysp > actualdays:
                error_message = "You have already spent '" + str(total_days_spent) + "' days of your leave you cannot apply for " + str(num_days) + "days in addition, please try again"
                return render(request, 'apply.html', {'form': form, 'error_message': error_message})

            leave_request = form.save(commit=False)
            leave_request.user = user
            leave_request.leave_type = leavetype
            leave_request.days = num_days 
            leave_request.relieving_Officer = relieve
            leave_request.start_date = start_date
            leave_request.end_date = end_date
            leave_request.status = stat
            leave_request.reason = reason
            leave_request.save()

            # Send email notification
            subject = 'Leave Request Submitted'
            message = f"Your leave request for {num_days} days has been submitted successfully."
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.email]  # Add the user's email or any other desired recipient
            send_mail(subject, message, from_email, to_email, fail_silently=True)

            return redirect('home')  # Replace 'home' with your desired home page URL
        else:
            # Display SweetAlert error message
            error_message = "There is an issue with the fields. Please try again."
            return render(request, 'apply.html', {'form': form, 'error_message': error_message})
    else:
        form = LeaveForm()

    context = {
        'all': total_days_spenty,
        'left': left,
        'year': current_year,
        'days': actualdays,
        'spent': total_days_spent,
        'form': form,
    }
    return render(request, 'apply.html', context)

@login_required(login_url='/')
def approvelist(request):
    listt = LeaveRequest.objects.filter(verted=True, status='Pending').order_by('-date_requested')
    lsta = LeaveRequest.objects.filter(status='Approved').order_by('-date_requested')
    context = {
        'lst':listt,
        'lsta':lsta
    }
    return render(request, 'approve.html', context)

@login_required(login_url='/')
def approve(request, id):
    
    requ = LeaveRequest.objects.get(pk=id)
    requ.status = "Approved"
    comment = request.GET.get('comment', '')
    existing_comments = requ.comment
    if comment:
        comment_with_user = f"{comment} by - {request.user.get_full_name()}  "
        if existing_comments:
            existing_comments += f"\n{comment_with_user}"
        else:
            existing_comments = comment_with_user
    requ.comment = existing_comments
    requ.save()
    usr = requ.user
    lvs = LeaveSpent()
    lvs.user= usr
    lvs.leave_type = requ.leave_type
    lvs.days_spent = requ.days
    lvs.year = datetime.now().year
    lvs.save()
    return redirect('approve')

@login_required(login_url='/')
def rejectleave(request, id):
    requ = LeaveRequest.objects.get(pk=id)
    comment = request.GET.get('comment', '')
    existing_comments = requ.comment
    if comment:
        comment_with_user = f"{comment} by - {request.user.get_full_name()}  "
        if existing_comments:
            existing_comments += f"\n{comment_with_user}"
        else:
            existing_comments = comment_with_user
    requ.comment = existing_comments
    requ.status = "Rejected"
    requ.save()
    return redirect('approve')

@login_required(login_url='/')
def vetlist(request):
    current_year = datetime.now().year
    dep = CustomUser.objects.get(id=request.user.id).department
    last_leaves = LeaveSpent.objects.filter(
        user__department=dep,
        year=current_year
    ).values('user').annotate(
        latest_leave=Max('id')
    ).values('latest_leave')
    last_leave_entries = LeaveSpent.objects.filter(id__in=last_leaves)
    listt = LeaveRequest.objects.filter(user__department=request.user.department,verted=False, status='Pending').order_by('-date_requested')
    lsta = LeaveRequest.objects.filter(user__department=request.user.department,verted=True).order_by('-date_requested')
    context = {
        'lst':listt,
        'lsta':lsta,
        'last':last_leave_entries
    }
    return render(request, 'vet.html', context)

@login_required(login_url='/')
def vet(request, id):
    requ = LeaveRequest.objects.get(pk=id)
    comment = request.GET.get('comment', '')
    existing_comments = requ.comment
    if comment:
        comment_with_user = f"{comment} by - {request.user.get_full_name()}  "
        if existing_comments:
            existing_comments += f"\n{comment_with_user}"
        else:
            existing_comments = comment_with_user
    requ.comment = existing_comments
    requ.verted = True
    requ.verted_By = str(request.user.get_full_name())
    requ.save()
    
    return redirect('vet')

@login_required(login_url='/')
def rejectvet(request, id):
    requ = LeaveRequest.objects.get(pk=id)
    requ.delete()
    
    return redirect('vet')


@login_required(login_url='/')
def myleave(request):
    mylr = LeaveRequest.objects.filter(user=request.user).order_by('id')
   
    context={
        'requests': mylr
    }
    return render(request, 'myleave.html', context)

@login_required(login_url='/')
def stats(request):
    # Query to get the sum of days_spent for each user, year, and leave type
    current_year = datetime.now().year
    summary_data = (
        LeaveSpent.objects.values('user__surname','user__firstname','user__department','user__position', 'year', 'leave_type')
        .annotate(total_days_spent=Sum('days_spent'))
    )

    aprrovedleave = LeaveRequest.objects.filter(start_date__year=current_year,verted=True,status='Approved').count()
    rejectedleave = LeaveRequest.objects.filter(start_date__year=current_year,verted=True,status='Rejected').count()
    vetpendingleave  = LeaveRequest.objects.filter(start_date__year=current_year,verted=True,status='Pending').count()
    unvetpendingleave = LeaveRequest.objects.filter(start_date__year=current_year,verted=False,status='Pending').count()
    context = {
        'current_year':current_year,
        'summary_data': summary_data,
        'aprrovedleave':aprrovedleave,
        'rejectedleave':rejectedleave,
        'vetpendingleave': vetpendingleave ,
        'unvetpendingleave':unvetpendingleave,
    }
    return render(request, 'stats.html', context )

def get_leave_spent(request, user_id):
    # Fetch leave spent information for the user with ID user_id
    current_year = datetime.now().year
    user = get_object_or_404(CustomUser, id=user_id)
    leave_spent_data = LeaveSpent.objects.filter(user=user, year=current_year)

    # Serialize the data using a serializer (you need to create one)
    serializer = LeaveSpentSerializer(leave_spent_data, many=True)
    serialized_data = serializer.data
    print(serialized_data)
    return JsonResponse(serialized_data, safe=False)


@login_required(login_url='/')
def holidays(request):
    holidays = Holidays.objects.all().order_by('-date')
    form = HolidayForm()
    if request.method == 'POST':
        form = HolidayForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect("holiday")
        else:
            form = HolidayForm()

    context = {
        'holidays' : holidays,
        'form' : form,
    }

    return render(request, "holiday.html", context)

@login_required(login_url='/')
def delholiday (request, id):
    hol = get_object_or_404(Holidays, id=id)
    hol.delete()
    return redirect("holiday")