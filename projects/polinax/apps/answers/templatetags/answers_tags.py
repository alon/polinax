from django import template
from django.utils.html import escape

from answers.models import Answer
register = template.Library()

class CountAnswersForNode(template.Node):
    def __init__(self, objects, context_var):
        self.objects = objects
        self.context_var = context_var

    def render(self, context):
        try:
            objects = template.resolve_variable(self.objects, context)
        except template.VariableDoesNotExist:
            return ''
        context[self.context_var] = Answer.objects.count_for(objects)
        return ''

def do_count_answers_for(parser, token):
    """
    Retrieves the total number of answers scores for a list of questions
    and stores them in a context variable.

    Example usage::

        {% answers_for question_list as answer_count_dict %}
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes exactly three arguments" % bits[0])
    if bits[2] != 'as':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
    return CountAnswersForNode(bits[1], bits[3])


register.tag('count_answers_for', do_count_answers_for)
