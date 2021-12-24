import argparse
import sys

from SamHeaderSequencesRenamerUtils import SamHeaderSequencesRenamerUtils
from utils import read_translations


class SamHeaderSequencesRenamer(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='In process',
            usage='''samHeaderSequencesRenamer <command> [<args>]

The commands are:
   check_availability_sequences     Compare possible translations result to a list of availability
   translate                        Performs translation of SAM header
''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    @staticmethod
    def check_availability_sequences():
        parser = argparse.ArgumentParser(
            description='Check the availability of the results of the translations')
        parser.add_argument('-t', '--translations', required=True)
        parser.add_argument('-a', '--availability', required=True)
        parser.add_argument('-o', '--output', required=False)
        args = vars(parser.parse_args(sys.argv[2:]))

        missing_sequences = SamHeaderSequencesRenamerUtils.get_non_available_sequences_from_path(
            args['translations'],
            args['availability']
        )
        if 'output' not in args or args['output'] is None:
            print(missing_sequences)
        else:
            with open(args['output'], 'w') as output_file:
                output_file.write(str(missing_sequences))

    @staticmethod
    def translate():
        parser = argparse.ArgumentParser(
            description='Performs translation of SAM header')
        parser.add_argument('-t', '--translations', required=True)
        parser.add_argument('-i', '--input', required=True)
        parser.add_argument('-o', '--output', required=True)
        args = vars(parser.parse_args(sys.argv[2:]))

        translations = read_translations(args['translations'])
        with open(args['input']) as file_input, open(args['output'], 'w') as file_output:
            SamHeaderSequencesRenamerUtils.get_header_translation(
                file_input,
                file_output,
                translations
            )
