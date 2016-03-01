# -*- coding: utf-8 -*-

import datetime
import os

from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from wsgiref.util import FileWrapper
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import exceptions
from django.db.models import Q

from chzis.school.models import SchoolTask, Lesson
from chzis.school.forms import SchoolTaskForm, SchoolTaskViewForm, SchoolTaskFilterForm, PassedLessonImportForm
from chzis.congregation.models import CongregationMember
from chzis.meetings.forms import MeetingTaskSchoolForm, MeetingTaskSchoolViewForm
from chzis.meetings.models import MeetingTask, MeetingItem
from chzis.utils.pdf import schooltask


class Tasks(View):
    def get(self, request):
        date_now = datetime.datetime.now()
        month_days = datetime.datetime(year=date_now.year, month=date_now.month + 1, day=1) - datetime.datetime(
                year=date_now.year, month=date_now.month, day=1)
        tasks = SchoolTask.objects.all().exclude(task__meeting_item__name='Old school')

        action = request.GET.get('action')
        if action == "filter":
            task_filter_form = SchoolTaskFilterForm(request.GET)
            if task_filter_form.is_valid():
                start = task_filter_form.cleaned_data['start']
                end = task_filter_form.cleaned_data['end']

                if start is not None:
                    tasks = tasks.filter(task__presentation_date__gte=start)
                else:
                    task_filter_form.fields['start'].widget.attrs['disabled'] = True
                if end is not None:
                    tasks = tasks.filter(task__presentation_date__lte=end)
                else:
                    task_filter_form.fields['end'].widget.attrs['disabled'] = True
        elif action == "filter_month_now":
            start = datetime.datetime(year=date_now.year, month=date_now.month, day=1)
            end = datetime.datetime(year=date_now.year, month=date_now.month, day=month_days.days)
            task_filter_form = SchoolTaskFilterForm(initial={"start": start,
                                                             "end": end,
                                                             'start_active': True,
                                                             'end_active': True})
            tasks = tasks.filter(task__presentation_date__gte=start,
                                 task__presentation_date__lte=end)
        else:
            task_filter_form = SchoolTaskFilterForm()
            task_filter_form.fields['start'].widget.attrs['disabled'] = True
            task_filter_form.fields['end'].widget.attrs['disabled'] = True

        paginator = Paginator(tasks, 25)
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
        context['filter_form'] = task_filter_form
        return render(request, 'tasks.html', context)


class AddTasks(TemplateView):
    template_name = "add_task.html"

    def get_context_data(self):
        context = dict()
        context['task_form'] = MeetingTaskSchoolForm(
                congregation=self.request.user.profile.default_congregation.id,
                initial={'presentation_date': self.request.session.get('last_schooltask_date', None)})
        context['school_task_form'] = SchoolTaskForm(congregation=self.request.user.profile.default_congregation.id)
        return context

    def post(self, request):
        task_form = MeetingTaskSchoolForm(request.POST, congregation=request.user.profile.default_congregation.id)
        school_task_form = SchoolTaskForm(request.POST, congregation=request.user.profile.default_congregation.id)

        if task_form.is_valid():
            if school_task_form.is_valid():
                task_form.instance.description = school_task_form.instance.description
                task = task_form.save()
                school_task_form.instance.task = task
                try:
                    # school_task_form.instance.supervisor = CongregationMember.objects.get(id=request.user.id)
                    school_task_form.instance.creator = CongregationMember.objects.get(id=request.user.id)
                except exceptions.ObjectDoesNotExist:
                    pass

                school_task = school_task_form.save()
                request.session['last_schooltask_date'] = str(task.presentation_date)
                return redirect('/school/tasks/{}'.format(school_task.task.id))

        context = dict()
        context['task_form'] = task_form
        context['school_task_form'] = school_task_form
        return render(request, "add_task.html", context)


class TaskView(TemplateView):
    template_name = "task.html"

    def get_context_data(self, task_id):
        school_task = SchoolTask.objects.get(task__id=task_id)
        context = dict()
        context['task_form'] = MeetingTaskSchoolViewForm(instance=school_task.task, initial={
            'meeting_item': school_task.task.meeting_item.full_name if school_task.task is not None else None,
            'person': str(school_task.task.person) if school_task.task is not None else None})
        context['school_task_form'] = SchoolTaskViewForm(instance=school_task,
                                                         congregation=self.request.user.profile.default_congregation.id,
                                                         initial={'slave': str(
                                                                 school_task.slave) if school_task.slave is not None else "",
                                                                  'supervisor': str(
                                                                          school_task.supervisor) if school_task.supervisor is not None else "",
                                                                  'creator': str(
                                                                          school_task.creator) if school_task.creator is not None else "",
                                                                  'lesson': school_task.lesson.name,
                                                                  'background': school_task.background.name if school_task.background is not None else None})
        return context


class EditTask(TemplateView):
    template_name = "edit_task.html"

    def get_context_data(self, task_id):
        school_task = SchoolTask.objects.get(task__id=task_id)
        context = dict()
        context['task_form'] = MeetingTaskSchoolForm(instance=school_task.task, congregation=self.request.user.profile.default_congregation.id)
        context['school_task_form'] = SchoolTaskForm(instance=school_task, congregation=self.request.user.profile.default_congregation.id)
        context['task_id'] = school_task.task.id
        context['school_task_id'] = school_task.id
        return context

    def post(self, request, task_id):
        context = dict()
        task_form = MeetingTaskSchoolForm(request.POST, congregation=request.user.profile.default_congregation.id)
        school_task_form = SchoolTaskForm(request.POST, congregation=request.user.profile.default_congregation.id)

        if task_form.is_valid():
            if school_task_form.is_valid():
                task_form.instance.description = school_task_form.instance.description
                task_form.instance.id = request.POST['task_id']
                task = task_form.save()
                school_task_form.instance.task = task
                school_task_form.instance.id = request.POST['school_task_id']
                school_task = school_task_form.save()
                return redirect('/school/tasks/{}'.format(school_task.task.id))

        context['task_id'] = request.POST['task_id']
        context['school_task_id'] = request.POST['school_task_id']

        context['task_form'] = task_form
        context['school_task_form'] = school_task_form
        return render(request, "edit_task.html", context)


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
    week_start = dt - datetime.timedelta(days=week_day)
    return redirect("/school/plan/{year}/{month}/{week_start_day}".format(year=week_start.year,
                                                                          month=week_start.month,
                                                                          week_start_day=week_start.day + 1))


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
    passed_lessons = {}
    for lesson_passed in member_passsed_lessons:
        if lesson_passed.lesson_passed_date is not None:
            passed_dates = passed_lessons.setdefault(lesson_passed.lesson.number, [])
            passed_dates.append(lesson_passed.lesson_passed_date)
            passed_dates.sort()

    if request.GET.get('action', None) == "edit":
        template_name = 'edit_task_school.inc.html'
    else:
        template_name = 'add_task_school.inc.html'

    tpl = loader.get_template(template_name)
    context = {'school_task_form': SchoolTaskForm(congregation=request.user.profile.default_congregation.id),
               'passed_lessons': passed_lessons
               }
    return HttpResponse(tpl.render(context))


def school_tasks_print(request):
    task_list = request.POST.getlist('print')
    tasks_to_print = []
    for task in task_list:
        t = SchoolTask.objects.get(id=task)
        task_param = {"name": u"{fullname}".format(fullname=t.task.person.member_fullname),
                      "slave": u"{fullname}".format(fullname=t.slave.member_fullname if t.slave is not None else u""),
                      "date": t.task.presentation_date,
                      "lesson": u"({lesson_number}){lesson_name}".format(lesson_name=t.lesson.name,
                                                                         lesson_number=t.lesson.number),
                      "task_type": t.task.meeting_item.name,
                      "class": 1
                      }
        tasks_to_print.append(task_param)

    response = HttpResponse("Please select least one task in order to generate pdf.")

    if tasks_to_print:
        min_date = min(tasks_to_print, key=lambda x: x['date'])
        max_date = max(tasks_to_print, key=lambda x: x['date'])

        file_name = u"{min_date}-{max_date}_{task_name}_[{counter}].pdf".format(
                min_date=min_date['date'].strftime("%d.%m.%y"),
                max_date=max_date['date'].strftime("%d.%m.%y"),
                task_name=_("school_tasks"),
                counter=len(task_list))
        schooltask.generate_school_task_cards(tasks_to_print, filename=os.path.join('/tmp', file_name))
        wrapper = FileWrapper(file(os.path.join('/tmp', file_name)))
        response = HttpResponse(wrapper, content_type='application/octet-stream')
        response['Content-Length'] = os.path.getsize(os.path.join('/tmp', file_name))
        response['Content-Disposition'] = 'attachment; filename={filename}'.format(filename=file_name.encode('utf-8'))

    return response


def school_member_history(request, member_id):
    member_history = SchoolTask.objects.filter(Q(task__person__id=member_id) | Q(slave__id=member_id)).exclude(
            task__meeting_item__name='Old school')
    p = reversed(sorted(member_history,
                        key=lambda x: x.task.presentation_date if x.task.presentation_date else datetime.date(1900, 1,
                                                                                                              1)))
    b = [a for a in p][:5]
    tpl = loader.get_template('add_task_mamber_history.inc.html')
    context = {'member_history': b}
    return HttpResponse(tpl.render(context))


def school_task_delete(request, task_id):
    SchoolTask.objects.get(task__id=task_id).delete()
    return redirect(request.GET.get('ref', '/school/tasks'))


class SchoolLessonImport(TemplateView):
    template_name = "lesson_import.html"

    def get_context_data(self):
        context = dict()
        context['passed_lesson_form'] = PassedLessonImportForm()
        return context

    def post(self, request):
        imported_lessons = []
        cong_memeber = None
        lesson_passed_form = PassedLessonImportForm(request.POST)

        if lesson_passed_form.is_valid():
            member = lesson_passed_form.cleaned_data['members']
            passed_lessons = lesson_passed_form.cleaned_data['passed_lessons']
            cong_memeber = CongregationMember.objects.get(id=member)
            try:
                creator = CongregationMember.objects.get(user__id=request.user.id)
            except exceptions.ObjectDoesNotExist:
                creator = None
            lessons = Lesson.objects.all()
            for lesson_number in passed_lessons:
                meeting_task = MeetingTask()
                meeting_task.person = cong_memeber
                meeting_task.meeting_item = MeetingItem.objects.get(name='Old school')
                meeting_task.presentation_date = datetime.datetime(1900, 1, 1)
                meeting_task.save()
                school_task = SchoolTask()
                school_task.creator = creator
                school_task.lesson = lessons.get(number=lesson_number)
                school_task.lesson_passed = True
                school_task.lesson_passed_date = datetime.datetime(1900, 1, 1)
                school_task.task = meeting_task
                school_task.save()
                imported_lessons.append(lesson_number)

        context = dict()
        context['passed_lesson_form'] = lesson_passed_form
        context['imported_lessons'] = imported_lessons
        context['school_member'] = cong_memeber
        return render(request, "lesson_import.html", context)
