import json
import logging
import os
import sys

from dotenv import load_dotenv

import messages
from arg_handler import parse_arguments
from database import (establish_db_connection, get_parsed_item_added,
                      get_resource_added, get_resource_deleted,
                      get_resource_list)
from models import ResourceModel
from parse_handler import ResourceHandler


def parse_items():
    """action: --parse"""
    engine, resource_table, items_table = establish_db_connection()
    resource_list = get_resource_list(engine, resource_table)
    handler = ResourceHandler()
    all_found_items = []
    for resource in resource_list:
        items_list = handler(resource)
        all_found_items += items_list

    saving_stats = {
        'updated': [],
        'created': [],
        'failed': []
    }
    for item in all_found_items:
        result = get_parsed_item_added(engine, items_table, item)
        saving_stats[result].append(item)

    result_text = messages.get_parse_stats_msg(
        resource_list,
        all_found_items,
        saving_stats,
        handler,
    )
    print(result_text)
    print(
        '\nВы также можете посмотреть результаты загрузки новостей из '
        'ресурсов в файле "parse_result.txt". В файле сохранена '
        'приведенная выше статистика, а также сами загруженные новости.'
    )
    with open('parse_result.txt', 'w') as result_file:
        result_file.write(result_text)
        result_file.write('\nЗагруженные новости:\n')
        for item in all_found_items:
            result_file.write('-----------------------\n')
            result_file.write(f'{str(item)}\n')


def add_resources(data):
    """action: --add-resources-list"""

    engine, resource_table, items_table = establish_db_connection()
    results = {
        'updated': [],
        'created': [],
        'failed to create': []
    }
    for resource in data:
        serialized_resource = ResourceModel(**resource).formated_for_db()
        result = get_resource_added(
            engine,
            resource_table,
            serialized_resource
        )
        results[result].append(resource['RESOURCE_NAME'])
    result_text = messages.get_add_resource_stats_msg(data, results)
    print(result_text)


def delete_resources(data):
    """action: --delete-resources"""

    engine, resource_table, items_table = establish_db_connection()
    results = {
        'deleted': [],
        'not_found': []
    }
    for resource_id in data:
        result = get_resource_deleted(
            engine,
            resource_table,
            int(resource_id)
        )
        results[result].append(resource_id)
    result_text = messages.get_del_resource_stats_msg(data, results)
    print(result_text)


def list_resources():
    """action: --list-resources"""
    engine, resource_table, items_table = establish_db_connection()
    resources = get_resource_list(engine, resource_table)
    for resource in resources:
        print(resource, end="\n-----------------------------\n\n")


def get_data_from_file(input_file):
    try:
        with open(input_file, 'r') as file:
            raw_data = file.read()
            data = json.loads(raw_data)
    except FileNotFoundError as e:
        print(str(e))
        sys.exit(1)
    except json.decoder.JSONDecodeError:
        print(
            "Error: couldn't retrieve list of resources from file. "
            " Please, ensure your file contains data in recommended format"
        )
        sys.exit(1)
    if not isinstance(data, list):
        print(
            "Error: couldn't retrieve list of resources from file. "
            " Please, ensure your file contains data in recommended format"
        )
        sys.exit(1)
    return data


def main():
    load_dotenv()

    logfile = os.getenv('LOGFILE')

    logging.basicConfig(
        level=logging.ERROR,
        filename=logfile,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    parser, arguments = parse_arguments()

    if arguments.delete_resources:
        data = get_data_from_file(arguments.delete_resources)
        delete_resources(data)
    elif arguments.add_resources:
        data = get_data_from_file(arguments.add_resources)
        add_resources(data)
    elif arguments.list_resources:
        list_resources()
    elif arguments.parse:
        parse_items()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
