from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect

from chzis.school.models import SchoolTask
from chzis.school.forms import SchoolTaskForm


class Tasks(View):
    def get(self, request):
        tasks = SchoolTask.objects.all()

        context = dict()
        context['tasks'] = tasks
        return render(request, 'tasks.html', context)


class AddTasks(View):
    def get(self, request):

        context = dict()
        context['form'] = SchoolTaskForm()
        return render(request, 'add_task.html', context)

    def post(self, request):
        print request.POST

        form = SchoolTaskForm(request.POST)
        if form.is_valid():
            task = form.save()
        else:
            context = dict()
            context['form'] = form
            return render(request, "add_task.html", context)
        return redirect('/school/tasks/{}'.format(task.id))


class TaskView(View):
    def get(self, request, task_id):
        task = SchoolTask.objects.get(id=task_id)
        form = SchoolTaskForm(instance=task)
        context = dict()
        context['form'] = form
        return render(request, "task.html", context)