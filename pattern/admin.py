from django.contrib import admin
from models import (
    Language,
    Pattern,
    Comment
)

class LanguageAdmin(admin.ModelAdmin):
    pass

class PatternAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Language, LanguageAdmin)
admin.site.register(Pattern, PatternAdmin)
admin.site.register(Comment, CommentAdmin)
