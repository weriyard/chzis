import datetime

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


class SchoolPlanDetails(View):
    def get(self, request, year, month, week_start_day):

        year = int(year)
        month = int(month)
        week_start_day = int(week_start_day)
        week_end_day = week_start_day + 6
        date = datetime.datetime(year,month, week_start_day)
        tasks = SchoolTask.objects.filter(presentation_date__gte=datetime.datetime(year, month, week_start_day),
                                          presentation_date__lte=datetime.datetime(year, month, week_end_day))

        prev_plan_date = date - datetime.timedelta(days=7)
        next_plan_date = date + datetime.timedelta(days=7)
        context = dict()
        context['tasks'] = tasks
        context['current_week'] = dict(week_start_day=week_start_day, week_end_day=week_end_day)
        context['date'] = dict(year=date.year, month=date.month, month_name=date.strftime("%B"))
        context['prev_plan_date'] = "{year}/{month}/{day}".format(year=prev_plan_date.year, month=prev_plan_date.month, day=prev_plan_date.day);
        context['next_plan_date'] = "{year}/{month}/{day}".format(year=next_plan_date.year, month=next_plan_date.month, day=next_plan_date.day);
        return render(request, "school_plan.html", context)


def school_plan(request):
    dt = datetime.datetime.now()
    week_day = dt.isocalendar()[2]
    week_start_day = dt.day - week_day + 1
    return redirect("/school/plan/{year}/{month}/{week_start_day}".format(year=dt.year,
                                                                          month=dt.month,
                                                                          week_start_day=week_start_day))