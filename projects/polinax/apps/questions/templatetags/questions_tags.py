from django.db.models import get_model
from django.template import Library, Node, TemplateSyntaxError, Variable, resolve_variable
from django.utils.translation import ugettext as _

from questions.models import Question

register = Library()

class QuestionsForUserNode(Node):
    def __init__(self, user, context_var):
        self.user_var = user
        self.context_var = context_var

    def render(self, context):
        user = context[self.user_var]
        if user is None:
            raise TemplateSyntaxError(_('questions_for_user tag was given an invalid user: %s') % self.user_var)
        context[self.context_var] = user.questions.filter(public=True)
        return ''

def do_questions_for_user(parser, token):
    """
    Retrieves a list of ``Questions`` added by the the given user
    and stores them in a context variable.

    Usage::

       {% questions_for_user [user] as [varname] %}

    """
    bits = token.contents.split()
    len_bits = len(bits)
    if len_bits!=4:
        raise TemplateSyntaxError(_('%s tag requires threearguments') % bits[0])
    if bits[2] != 'as':
        raise TemplateSyntaxError(_("second argument to %s tag must be 'as'") % bits[0])
    return QuestionsForUserNode(bits[1], bits[3])

register.tag('questions_for_user', do_questions_for_user)
