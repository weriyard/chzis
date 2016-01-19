import datetime

from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect
from django.http import HttpResponse

from chzis.school.models import SchoolTask
from chzis.school.forms import SchoolTaskForm, SchoolTaskViewForm
from chzis.meetings.models import MeetingTask
from chzis.meetings.forms import MeetingTaskSchoolForm, MeetingTaskSchoolViewForm


class Tasks(View):
    def get(self, request):
        tasks = SchoolTask.objects.all()

        context = dict()
        context['tasks'] = tasks
        return render(request, 'tasks.html', context)


class AddTasks(View):
    def get(self, request):

        context = dict()
        context['task_form'] = MeetingTaskSchoolForm()
        context['school_task_form'] = SchoolTaskForm()

        return render(request, 'add_task.html', context)

    def post(self, request):
        task_form = MeetingTaskSchoolForm(request.POST)
        school_task_form = SchoolTaskForm(request.POST)

        if task_form.is_valid():
            if school_task_form.is_valid():
                task_form.instance.description = school_task_form.instance.description
                task = task_form.save()
                school_task_form.instance.task = task
                school_task = school_task_form.save()
            return redirect('/school/tasks/{}'.format(school_task.id))
        else:
            context = dict()
            context['task_form'] = task_form
            context['school_task_form'] = school_task_form
            return render(request, "add_task.html", context)



class TaskView(View):
    def get(self, request, task_id):
        school_task = SchoolTask.objects.get(id=task_id)
        context = dict()
        context['task_form'] = MeetingTaskSchoolViewForm(instance=school_task.task, initial={'meeting_item': school_task.task.meeting_item.full_name if school_task.task is not None else None,
                                                                                             'person': str(school_task.task.person) if school_task.task is not None else None})
        context['school_task_form'] = SchoolTaskViewForm(instance=school_task, initial={'lesson': school_task.lesson.name,
                                                                                        'background': school_task.background.name if school_task.background is not None else None})
        return render(request, "task.html", context)


class SchoolPlanDetails(View):
    def get(self, request, year, month, week_start):

        year = int(year)
        month = int(month)
        week_start = datetime.datetime(year=year, month=month, day=int(week_start))
        week_end = week_start + datetime.timedelta(days=6)

        prev_date = week_start - datetime.timedelta(days=7)
        next_date = week_start + datetime.timedelta(days=7)

        tasks = SchoolTask.objects.filter(task__presentation_date__gte=week_start,
                                          task__presentation_date__lte=week_end)

        context = dict()
        context['tasks'] = tasks
        context['current_week'] = dict(week_start=week_start, week_end=week_end)
        context['prev_plan_date'] = "{year}/{month}/{day}".format(year=prev_date.year, month=prev_date.month, day=prev_date.day);
        context['next_plan_date'] = "{year}/{month}/{day}".format(year=next_date.year, month=next_date.month, day=next_date.day);
        return render(request, "school_plan.html", context)


def school_plan(request):
    dt = datetime.datetime.now()
    week_day = dt.isocalendar()[2]
    week_start_day = dt.day - week_day + 1
    return redirect("/school/plan/{year}/{month}/{week_start_day}".format(year=dt.year,
                                                                          month=dt.month,
                                                                          week_start_day=week_start_day))

def set_task_result(request, task_id):
    if 'result' in request.POST:
        if request.POST.get('result', None) == 'ok':
            result = True
        else:
            result = False

        task_result = SchoolTask.objects.get(task__id=int(task_id))
        task_result.lesson_passed = result
        task_result.save()
    return HttpResponse("alal")
