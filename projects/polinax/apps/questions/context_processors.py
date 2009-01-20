from questions.models import Question, CATEGORY_CHOICES

def questions (request):
    ''' a Django context processor that added the user's own questions and the questions he voted for
    '''
    if request.user.is_authenticated():
        c = dict (user_qs = request.user.questions.all().order_by('-added'),
                # user_voted_qs = Vote.objects.filter(user=request.user).values_list('object', flat=True).order_by("-added")
                )
    else:
        c = dict (user_qs = [], user_voted_qs=[])
    c.update({"categories": CATEGORY_CHOICES})
    return c 

