from pynecone import Command
from .client import Client
from .output import Output
from urllib.parse import urljoin

class Retrieve(Command):

    def __init__(self):
        super().__init__("retrieve")

    def run(self, args):

        format_type = 'json'
        if args.print:
            format_type = 'table'

        if args.context == 'item' and args.id is not None:
            self.output(Output.format(Client.create().get(urljoin('items/', args.id), None), format_type), args.output_path)
        elif args.context == 'data' and args.id is not None:
            self.output(Client.create().get('items/' + args.id + '/data', None), args.output_path)
        else:
            params = {'my_items': True}
            if args.id:
                params['parent_id'] = args.id

            self.output(Output.format(Client.create().get('items', params), format_type), args.output_path)

    def add_arguments(self, parser):
        parser.add_argument('--context', choices=['items', 'item', 'data'], default='items', const='items', nargs='?',
                            help='specify whether to retrieve the root item, child items or data of the root item')
        parser.add_argument('--id', help='id of the root item defaults to the user root item')
        parser.add_argument('--output_path', help="save the output to the specified path")
        parser.add_argument('--print', nargs='?', const=True, default=False, help="print human readable output.")
        # parser.add_argument('--children', nargs='?', const=True, default=False, help="retrieve all items in a given context.")

    def get_help(self):
        return 'retrieve an item or items'

    def output(self, data, path):
        if path:
            if isinstance(data, str):
                with open(path, 'w') as f:
                    print(data, file=f)
            else:
                with open(path, 'wb') as f:
                    f.write(data)
        else:
            print(data)
