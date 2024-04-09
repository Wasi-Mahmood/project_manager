from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from base_model.models import Task, User

@login_required
def show_all_task(request, user_id):
    if request.method == 'POST':

        tasks = Task.objects.all()

        for task in tasks:
            assigned_user_id = task.assigned_user_id
            assigned_user = get_object_or_404(User, id=assigned_user_id)
            task.assigned_user_name = assigned_user.name 

        return render(request, 'tasks/alltasks.html', {
            'tasks': tasks,
            'user_id': user_id 
        })

    else:
        filter_by = request.GET.get('filter')

        sort_by = request.GET.get('sort')
        tasks = Task.objects.all()

        # Apply filtering based on filter_by

        if filter_by == 'To-Do':
            tasks = tasks.filter(status='To-Do')
        elif filter_by == 'In-Progress':
            tasks = tasks.filter(status='In-Progress')
        elif filter_by == 'Done':
            tasks = tasks.filter(status='Done')
        print("tasks", [task for task in tasks])
    

        # Define the priority order dictionary
        priority_order = {
            'Highest': 1,
            'High': 2,
            'Medium': 3,
            'Low': 4,
            'Lowest': 5,
           
        }


        # Apply sorting based on sort_by
        if sort_by == 'priority':
            tasks = sorted(tasks, key=lambda x: priority_order.get(x.priority, float('inf')))
        elif sort_by == 'due_date':
            tasks = sorted(tasks, key=lambda x: x.due_date)

        for task in tasks:
            assigned_user_id = task.assigned_user_id
            assigned_user = get_object_or_404(User, id=assigned_user_id)
            task.assigned_user_name = assigned_user.name  
        return render(request, 'tasks/alltasks.html', {
            'tasks': tasks,
            'user_id': user_id 
        })




@login_required
def add(request, user_id):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        due_date = request.POST.get('due_date', '')  
        assigned_user_uuid = request.POST.get('assigned_user', '')
        status = request.POST.get('status', '')
        priority = request.POST.get('priority', '')
        label = request.POST.get('label', '')
        sprint = request.POST.get('sprint', '')

        assigned_user = get_object_or_404(User, id=assigned_user_uuid)
        created_by = get_object_or_404(User,id=user_id)

        task = Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            assigned_user=assigned_user,
            status=status,
            priority=priority,
            label=label,
            sprint=sprint,
            created_by=created_by
        )

        redirect_url = request.POST.get('redirect_url')   
        return redirect(redirect_url) 
    
    users_data = User.objects.all().values('id', 'name', 'email')
    return render(request, 'tasks/add.html',{"users_data": users_data})


@login_required
def detail(request, user_id, task_id):

    if request.method == 'POST':
        task = Task.objects.get(id=task_id)

        task.title = request.POST.get('title', '')
        task.description = request.POST.get('description', '')
        task.due_date = request.POST.get('due_date', '')  
        assigned_user_uuid = request.POST.get('assigned_user', '')
        task.status = request.POST.get('status', '')
        task.priority = request.POST.get('priority', '')
        task.label = request.POST.get('label', '')
        task.sprint = request.POST.get('sprint', '')
    
        
        task.assigned_user = get_object_or_404(User, id=assigned_user_uuid)
        task.created_by = get_object_or_404(User,id=user_id)

        task.save()


    task = Task.objects.get(id=task_id)

    assigned_user_id = task.assigned_user_id
    assigned_user = get_object_or_404(User, id=assigned_user_id)
    task.assigned_user_name = assigned_user.name

    return render(request, 'tasks/detail.html', {
        'task': task
    })


@login_required
def edit(request, user_id,task_id):

    if request.method == 'POST':
        print("suiii")
        print("request.POST.get('description', '')>>>>: ", request.POST.get('description', ''))
        task = Task.objects.get(id=task_id)

        task.title = request.POST.get('title', '')
        task.description = request.POST.get('description', '')
        task.due_date = request.POST.get('due_date', '')  
        assigned_user_uuid = request.POST.get('assigned_user', '')
        task.status = request.POST.get('status', '')
        task.priority = request.POST.get('priority', '')
        task.label = request.POST.get('label', '')
        task.sprint = request.POST.get('sprint', '')
    
        
        task.assigned_user = get_object_or_404(User, id=assigned_user_uuid)
        task.created_by = get_object_or_404(User,id=user_id)

        task.save()

    task = Task.objects.get(id=task_id)
    return render(request, 'tasks/edit.html', {
        'task': task
    })


@login_required
def delete(request, user_id, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()

    tasks = Task.objects.all()

    for task in tasks:
    
        assigned_user_id = task.assigned_user_id
        assigned_user = get_object_or_404(User, id=assigned_user_id)
        task.assigned_user_name = assigned_user.name  

    return redirect('tasks:alltasks',user_id=user_id)
