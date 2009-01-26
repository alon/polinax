from django.template import Library, Node, TemplateSyntaxError
from django.utils.translation import ugettext as _

from groups.models import Membership

register = Library()

class GetUserPartyNode(Node):
    def __init__(self, user, context_var):
        self.user_var = user
        self.context_var = context_var

    def render(self, context):
        user = context[self.user_var]
        if user is None:
            raise TemplateSyntaxError(_('questions_for_user tag was given an invalid user: %s') % self.user_var)
        try:
            context[self.context_var] = Membership.objects.get(user=user, role__title='candidate').group.name
        except Membership.DoesNotExist:
            context[self.context_var] = None
        print self.context_var
        print context[self.context_var]
        return ''

def do_get_user_party(parser, token):
    """
    Retrieves a list of ``Questions`` added by the the given user
    and stores them in a context variable.

    Usage::

       {% get_user_party for [user] as [varname] %}

    """
    bits = token.contents.split()
    len_bits = len(bits)
    if len_bits!=5:
        raise TemplateSyntaxError(_('%s tag requires threearguments') % bits[0])
    if bits[1] != 'for':
        raise TemplateSyntaxError(_("first argument to %s tag must be 'as'") % bits[0])
    if bits[3] != 'as':
        raise TemplateSyntaxError(_("third argument to %s tag must be 'as'") % bits[0])
    return GetUserPartyNode(bits[2], bits[4])

register.tag('get_user_party', do_get_user_party)

def show_party_of(user):
    g = Membership.objects.get(user=user).group
    return '<a href="%s">%s</a>' % (g.party.get_absolute_url(), Membership.objects.get(user=user).group.name)

register.simple_tag(show_party_of)
