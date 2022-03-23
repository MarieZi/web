from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext\_lazy as \_


class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT\_TYPE\_CHOICES = (
        (DIALOG, \_('Dialog')),
        (CHAT, \_('Chat'))
    )


type = models.CharField(
    \_('Тип'),
    max\_length = 1,
    choices = CHAT\_TYPE\_CHOICES,
    default = DIALOG
    )
    members = models.ManyToManyField(User, verbose\_name =\_("Участник"))

    @models.permalink
    def get\_absolute\_url(self):
        return 'users:messages', (), {'chat\_id': self.pk}


class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose\_name =\_("Чат"))
    author = models.ForeignKey(User, verbose\_name =\_("Пользователь"))
    message = models.TextField(\_("Сообщение"))
    pub\_date = models.DateTimeField(\_('Дата сообщения'), default = timezone.now)
    is \_readed = models.BooleanField(\_('Прочитано'), default = False)

class Meta:
    ordering = ['pub\_date']

def  \_\_str\_\_(self):
    return self.message

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}

class DialogsView(View):
    def get(self, request):
        chats = Chat.objects.filter(members\_\_in=[request.user.id])
        return render(request, 'users/dialogs.html', {'user\_profile': request.user, 'chats': chats})

class MessagesView(View):
    def get(self, request, chat\_id):
        try:
            chat = Chat.objects.get(id=chat\_id)
            if request.user in chat.members.all():
                chat.message\_set.filter( is\_readed = False).exclude(author=request.user).update( is\_readed = True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None

        return render(
            request,
            'users/messages.html',
            {
                'user\_profile': request.user,
                'chat': chat,
                'form': MessageForm()
            }
        )

    def post(self, request, chat\_id):
    form = MessageForm(data=request.POST)
    if form. is\_valid():
        message = form.save(commit=False)
        message.chat\_id = chat\_id
        message.author = request.user
        message.save()
    return redirect(reverse('users:messages', kwargs={'chat\_id': chat\_id}))
