""" Gunicorn starter command """
from flask_script import Command, Option
from gunicorn.app.base import Application
from gunicorn import version_info
from gunicorn.arbiter import Arbiter
from gunicorn.config import Config

# pylint: disable=W0223
class GunicornCmd(Command):
  """Run the app within Gunicorn"""

  def __init__(self, host='127.0.0.1', port=8000, workers=6):
    self.port = port
    self.host = host
    self.workers = workers

  def get_options(self):
    """ Get cmd line options """
    return (
      Option('-t', '--host',
             dest='host',
             default=self.host),

      Option('-p', '--port',
             dest='port',
             type=int,
             default=self.port),

      Option('-w', '--workers',
             dest='workers',
             type=int,
             default=self.workers),
    )

  def handle(self, app, *args, **kwargs):

    host = kwargs['host']
    port = kwargs['port']
    workers = kwargs['workers']

    def remove_non_gunicorn_command_line_args():
      """ Remove command line args that shouldn't be passed to gunicorn """
      import sys
      args_to_remove = ['--port', '-p', '--appconfig', '--host', '-t']
      def args_filter(name_or_value):
        """ Filter given args out """
        keep = not args_to_remove.count(name_or_value)
        if keep:
          previous = sys.argv[sys.argv.index(name_or_value) - 1]
          keep = not args_to_remove.count(previous)
        return keep
      # pylint: disable=W0141
      sys.argv = list(filter(args_filter, sys.argv))

    remove_non_gunicorn_command_line_args()

    if version_info < (0, 9, 0):
      arbiter = Arbiter(Config({'bind': "%s:%d" % (host, int(port)), 'workers': workers}), app)
      arbiter.run()
    else:
      class FlaskApplication(Application):
        """ Flask app helper class """
        def init(self, parser, opts, args):
          """ Initialize application """
          return {
            'bind': '{0}:{1}'.format(host, port),
            'workers': workers
          }

        def load(self):
          """ Simply return the instance of the app """
          return app

    FlaskApplication().run()
