from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from twisted.internet import task
from twisted.internet import reactor
from django.conf import settings

from api_client import utils




class Command(BaseCommand):
    args = '-i <check_interval>'
    help = 'Runs daemon to search for neighbors'

    option_list = BaseCommand.option_list + (
        make_option('--interval', '-i', dest='interval',
            help='Define the interval in seconds to check for neighbors.'),
    )

    def handle(self, *args, **options):
        interval = options.get('interval',  )
        if not interval:
            interval = settings.DEFAULT_CHECK_INTERVAL

        try:
            interval = int(interval)
        except ValueError:
            raise ValueError("Interval must be an integer.")


        print "Running every %s seconds." % interval
        
        #def runIntervalSecond(*args, **kw):
        #    interval = kw.get('interval')
        #    print "%s seconds have passed" % (interval)
        
        c = utils.ClientParser()
        
        kw = {'interval':interval}
        l = task.LoopingCall(c.process, *args, **kw)
        l.start(interval)
        
        
        reactor.run()
        
 