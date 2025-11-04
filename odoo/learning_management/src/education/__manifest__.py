# -*- coding: utf-8 -*-
{
    'name': " LMS education",

    'depends': ['user_management', 'mail.thread', 'mail.activity.mixin'],

    'data': [
        'security/ir.model.access.csv',
        'views/assignment.xml',
        'views/course.xml',
        'views/group.xml',
        'views/language.xml',
        'views/lesson.xml',
        'views/performance.xml',
        'views/subject.xml',
        'views/submission.xml',
        'views/task.xml',
        'views/timetable.xml',
        'views/menu.xml',
    ],
}

