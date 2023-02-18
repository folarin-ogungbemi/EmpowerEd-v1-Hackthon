from django.contrib import admin
from .models import Conversation, Message


admin.site.register(Message)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """
    Admin class for the Conversation model.
    """
    fields = ('name', 'members')
    list_display = ('name',)
    readonly_fields = ('members',)
    search_fields = ('members',)

    def name(self, obj):
        """
        String representation of a conversation instance:
        the name including members of the conversation.
        """
        return f"{obj.name} {obj.members}"

    def id(self, obj):
        """
        String representation of the id of the conversation object.
        """
        return f"{obj.id}"
