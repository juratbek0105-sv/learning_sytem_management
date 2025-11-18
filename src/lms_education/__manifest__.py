# -*- coding: utf-8 -*-
{
    'name': " LMS education",

    'depends': ['user_management', 'mail', 'uom'],

    'data': [
        'security/ir.model.access.csv',
        'views/assignment.xml',
        'views/course.xml',
        'views/group.xml',
        'views/language.xml',
        'views/lesson.xml',
        'views/result.xml',
        'views/submission.xml',
        'views/task.xml',
        'views/schedule_table.xml',
        'views/schedule_lesson.xml',
        'views/inherit_views/student_inherit.xml',
        'views/inherit_views/teacher_inherit.xml',
        'views/menu.xml',

        'data/uom_data.xml',
        'data/weekday_data.xml',
        'data/group_sequence.xml',
         #'data/sequence_schedule_lesson.xml',

        'wizard/lesson_date_wizard.xml',
    ],
}

