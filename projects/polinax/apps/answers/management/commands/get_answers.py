import re
import feedparser
from django.core.management.base import NoArgsCommand
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.conf import settings
from groups.models import Membership
from profiles.models import Profile
from answers.models import Answer
from questions.models import Question
search_re = re.compile(Site.objects.get(id=settings.SITE_ID).domain + reverse("view_question", args=[0])[:-2] + '(\d+)')

class Command(NoArgsCommand):
    help = 'Read all the feeds and get some fresh answers.'
    
    def parse_feeds(self, feeds):      
        result = []
        for k, feed in feeds:
            f = feedparser.parse(feed)
            for i in f.entries:
                # if i.date
                c = i.content[0].value
                m = search_re.search(c)
                if m:
                    a = {"adder_id":k,
                        "text":c,
                        "url":i.link,
                        "q_id": int(m.groups()[0]),
                        "summary": i.title,
                             }
                    result.append(a)
        return result

    def handle_noargs(self, **options):
        cs = Membership.objects.filter(role__title='candidate').values_list('user', flat=True)
        ps = Profile.objects.filter(user__id__in=cs, website__isnull=False).values_list('user_id','website')
        print ps
        answers = self.parse_feeds(ps)
        print answers
        for a in answers:
            Answer.objects.create(**a) 
        
