# stdlib imports
from optparse import OptionParser
import sys

# local imports
from command import Command
from up import UpCommand
from errors import FillPathError
from down import DownCommand

class FillCommand(Command):
    def init_parser(self):
        usage = "schema fill [options] [path_to_fill_sql]" \
                "\n\n" \
                "Arguments" \
                "\n  path_to_fill_sql               the path to your fill sql, " \
                "which alternatively can live in your config like '\"fill_path\" : \"relative/path/to-fill.sql\"'" \
                "your config value will be used by default, and a fill path specified as an argument will override any config value"

        parser = OptionParser(usage=usage)
        parser.add_option('-f', '--force',
                          action='store_true', dest='force', default=False,
                          help='Continue running alters even if an error has occurred')
        parser.add_option('-v', '--verbose',
                          action='store_true', dest='verbose', default=False,
                          help='Output verbose error-messages when used with -f option if errors are encountered')
        parser.add_option('-u', '--run-up',
                          action='store_true', dest='run_up', default=False,
                          help='run the up command before running fill')
        self.parser = parser

    def run(self):
        (options, args) = self.parser.parse_args()
        fill_path = args[0] if len(args) > 0 else None or self.config.get('fill_path')

        if fill_path is None:
          raise FillPathError('you must specify a fill path either on the commanline as "schema fill [options] [path_to_fill_sql]" or in your config as "fill_path" : "relative/path/to-fill.sql"')

        sys.stdout.write(fill_path)
        if options.run_up:
            sys.stdout.write("\nRunning up\n")
            sys.argv = [sys.argv[0]]
            if options.force:
                sys.argv.append('--force')
            if options.verbose:
                sys.argv.append('--verbose')
            UpCommand(self.context).run()

        sys.stdout.write("\nApplying fill sql\n")
        self.db._run_file(filename=fill_path,
                  exit_on_error=not options.force,
                  verbose=options.verbose)

        sys.stdout.write('Applied fill sql.')
