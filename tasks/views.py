from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from base_model.models import Task, User

@login_required
def show_all_task(request, user_id):
    print("suiii")
    if request.method == 'POST':

        tasks = Task.objects.all()

        for task in tasks:
            assigned_user_id = task.assigned_user_id
            assigned_user = get_object_or_404(User, id=assigned_user_id)
            task.assigned_user_name = assigned_user.name  # Assuming 'name' is the field in the User model

        return render(request, 'tasks/alltasks.html', {
            'tasks': tasks,
            'user_id': user_id 
        })

    else:
        print("suii2")
        filter_by = request.GET.get('filter')
        print("filter_by", filter_by)

        sort_by = request.GET.get('sort')
        print("sort_by", sort_by)
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
            # You can add more priority levels if needed
        }


        # Apply sorting based on sort_by
        if sort_by == 'priority':
            tasks = sorted(tasks, key=lambda x: priority_order.get(x.priority, float('inf')))
        elif sort_by == 'due_date':
            tasks = sorted(tasks, key=lambda x: x.due_date)

        for task in tasks:
            assigned_user_id = task.assigned_user_id
            assigned_user = get_object_or_404(User, id=assigned_user_id)
            task.assigned_user_name = assigned_user.name  # Assuming 'name' is the field in the User model

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
        # Optionally, you can redirect to a specific page after creating the task
        # return redirect('tasks:task_detail', pk=task.pk)  # Adjust the URL name and parameters
        
        # Or return a JSON response if it's an AJAX request
        # return JsonResponse({'success': True, 'task_id': task.pk})
        # If it's a GET request or the form wasn't valid, render the template with the form

        redirect_url = request.POST.get('redirect_url')  # Get the redirect URL from the form
        return redirect(redirect_url)  # Redirect to the specified URL after add
    
    users_data = User.objects.all().values('id', 'name', 'email')
    return render(request, 'tasks/add.html',{"users_data": users_data})


@login_required
def detail(request, project_id, todolist_id, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    todolist = Todolist.objects.filter(project=project).get(pk=todolist_id)
    task = Task.objects.filter(project=project).filter(todolist=todolist).get(pk=pk)

    if request.GET.get('is_done', '') == 'yes':
        task.is_done = True
        task.save()

    return render(request, 'task/detail.html', {
        'task': task
    })


@login_required
def edit(request, project_id, todolist_id, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    todolist = Todolist.objects.filter(project=project).get(pk=todolist_id)
    task = Task.objects.filter(project=project).filter(todolist=todolist).get(pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')

        if name:
            task.name = name

        task.description = description
        task.save()

        return redirect(f'/projects/{project_id}/{todolist_id}/{pk}/')

    return render(request, 'task/edit.html', {
        'task': task
    })


@login_required
def delete(request, project_id, todolist_id, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    todolist = Todolist.objects.filter(project=project).get(pk=todolist_id)
    task = Task.objects.filter(project=project).filter(todolist=todolist).get(pk=pk)
    task.delete()

    return redirect(f'/projects/{project_id}/{todolist_id}/')