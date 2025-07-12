from django.contrib import admin
from .models import User,Expense
from django.contrib.auth.admin import UserAdmin

class NewUserAdmin(UserAdmin):
    list_display = ('id','email','name','phone','is_active')
    list_filter = ('id','is_active')
    fieldsets = (
        ('User Credentials',{'fields':('email','password')}),
        ('Personal info',{'fields':('name','phone')}),
        ('Permissions',{'fields':('is_superuser',)}),
    )
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('email','name','phone','password1','password2'),
        }),

    )
    search_fields  = ('email',)
    ordering = ('email','id')
    filter_horizontal = ()

admin.site.register(User,NewUserAdmin)
admin.site.register(Expense)

# Register your models here.
