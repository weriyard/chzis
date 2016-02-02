# -*- coding: utf-8 -*-

import datetime
import simplejson

from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader, Context
from wsgiref.util import FileWrapper
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from chzis.school.models import SchoolTask
from chzis.school.forms import SchoolTaskForm, SchoolTaskViewForm
from chzis.meetings.models import MeetingTask
from chzis.meetings.forms import MeetingTaskSchoolForm, MeetingTaskSchoolViewForm
from chzis.utils.pdf import schooltask

import os


class Tasks(View):
    def get(self, request):
        tasks = SchoolTask.objects.all()

        paginator = Paginator(tasks, 5)
        page = request.GET.get('page')

        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            tasks = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            tasks = paginator.page(paginator.num_pages)

        context = dict()
        context['tasks'] = tasks
        return render(request, 'tasks.html', context)


class AddTasks(TemplateView):
    template_name = "add_task.html"

    def get_context_data(self):
        context = dict()
        context['task_form'] = MeetingTaskSchoolForm()
        context['school_task_form'] = None
        return context

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

        context = dict()
        context['task_form'] = task_form
        context['school_task_form'] = school_task_form
        return render(request, "add_task.html", context)


class TaskView(TemplateView):
    template_name = "task.html"

    def get_context_data(self, task_id):
        school_task = SchoolTask.objects.get(id=task_id)
        context = dict()
        context['task_form'] = MeetingTaskSchoolViewForm(instance=school_task.task, initial={
            'meeting_item': school_task.task.meeting_item.full_name if school_task.task is not None else None,
            'person': str(school_task.task.person) if school_task.task is not None else None})
        context['school_task_form'] = SchoolTaskViewForm(instance=school_task,
                                                         initial={'lesson': school_task.lesson.name,
                                                                  'background': school_task.background.name if school_task.background is not None else None})
        return context


class SchoolPlanDetails(View):
    def get(self, request, year, month, week_start):
        week_start = datetime.datetime(year=int(year), month=int(month), day=int(week_start))
        week_end = week_start + datetime.timedelta(days=6)

        prev_date = week_start - datetime.timedelta(days=7)
        next_date = week_start + datetime.timedelta(days=7)

        tasks = SchoolTask.objects.filter(task__presentation_date__gte=week_start,
                                          task__presentation_date__lte=week_end)

        context = dict()
        context['tasks'] = tasks
        context['current_week'] = dict(week_start=week_start, week_end=week_end)
        context['prev_plan_date'] = "{year}/{month}/{day}".format(year=prev_date.year, month=prev_date.month,
                                                                  day=prev_date.day);
        context['next_plan_date'] = "{year}/{month}/{day}".format(year=next_date.year, month=next_date.month,
                                                                  day=next_date.day);
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


def school_member_lesson_passed(request, member_id):
    member_passsed_lessons = SchoolTask.objects.filter(task__person__id=member_id).only('lesson', 'lesson_passed_date')
    print '-->', member_passsed_lessons
    passed_lessons = {}
    for lesson_passed in member_passsed_lessons:
        passed_dates = passed_lessons.setdefault(lesson_passed.lesson.number, [])
        passed_dates.append(lesson_passed.lesson_passed_date)
        passed_dates.sort()

    print passed_lessons
    tpl = loader.get_template('add_task_school.inc.html')
    context = {'school_task_form': SchoolTaskForm(),
               'passed_lessons': passed_lessons
               }
    return HttpResponse(tpl.render(context))


def school_tasks_print(request):
    task_list = request.POST.getlist('print')
    tasks_to_print = []
    for task in task_list:
        t = SchoolTask.objects.get(id=task)
        task_param = {"name": u"{firstname} {lastname}".format(firstname=t.task.person.user.first_name,
                                                               lastname=t.task.person.user.last_name),
                      "slave": "",
                      "date": t.task.presentation_date,
                      "lesson": t.lesson.name,
                      "task_type": t.task.meeting_item.name,
                      "class": 1
                      }
        tasks_to_print.append(task_param)

    if tasks_to_print:
        min_date = min(tasks_to_print, key=lambda x: x['date'])
        max_date = max(tasks_to_print, key=lambda x: x['date'])

        file_name = "{min_date}-{max_date}_{task_name}_[{counter}].pdf".format(min_date=min_date['date'].strftime("%d.%m.%y"),
                                                               max_date=max_date['date'].strftime("%d.%m.%y"),
                                                               task_name=_("school_tasks"),
                                                               counter=len(task_list))
        schooltask.generate_school_task_cards(tasks_to_print, filename=os.path.join('/tmp', file_name))
        wrapper = FileWrapper(file(os.path.join('/tmp', file_name)))
        response = HttpResponse(wrapper, content_type='application/octet-stream')
        response['Content-Length'] = os.path.getsize(os.path.join('/tmp', file_name))
        response['Content-Disposition'] = 'attachment; filename="{filename}"'.format(filename=file_name)
    else:
        respone = HttpResponse("Please select least one task in order to generate pdf.")

    return response
