import argparse


def parse_arguments():

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--list-resources',
        action='store_true',
        help='list all resources from resource database'
    )
    group.add_argument(
        '--delete-resources',
        help=(
            'delete specified resources from resource database.'
            'You need to specify file with resources after this argument'
        )
    )
    group.add_argument(
        '--add-resources',
        help=(
            'adds specified resources to resource database'
            'You need to specify file with resources after this argument'
        )
    )
    group.add_argument(
        '--parse',
        action='store_true',
        help='parse resorces and save result to items database',
    )
    arguments = parser.parse_args()
    return parser, arguments
