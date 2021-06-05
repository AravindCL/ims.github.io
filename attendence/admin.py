from django.contrib import admin
from . models import Student, Teacher, Class, Count, Feedback, Subject, Item, Type


admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Class)
admin.site.register(Count)
admin.site.register(Feedback)
# admin.site.register(Tutorial)
admin.site.register(Subject)
# admin.site.register(ImportantQuestions)
# admin.site.register(Note)
# admin.site.register(QuestionPaper)
admin.site.register(Item)
admin.site.register(Type)
