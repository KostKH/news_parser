def get_parse_stats_msg(
    resource_list,
    all_found_items,
    saving_stats,
    resource_handler
):
    failed_res_number = len(resource_handler.failed_resources)
    handled_res_number = len(resource_list) - failed_res_number
    parse_info = [
        f'\nНайдено ресурсов в базе на парсинг: {len(resource_list)}',
        f'Обработано ресурсов: {str(handled_res_number)}',
        f'Не удалось обработать: {str(failed_res_number)}',
        '\nЧто именно не было обработано:',
        '\n'.join(resource_handler.failed_resources),
        '\nВ части обработанных ресурсов:',
        f'Загружено новостей: {len(all_found_items)}',
        f'Не удалось загрузить: {len(resource_handler.not_downloaded)}',
        '\nЧто именно не было загружено:',
        '\n'.join(resource_handler.not_downloaded),
        '\nИз загруженных новостей:',
        f'Сохранена в БД как новая новость: {len(saving_stats["created"])}',
        f'Новость найдена в базе, обновлена: {len(saving_stats["updated"])}',
        f'Не удалось сохранить в БД: {len(saving_stats["failed"])}',
    ]
    return '\n'.join(parse_info)


def get_add_resource_stats_msg(data, results):
    addition_info = [
        f'\nНайдено ресурсов во входящих параметрах: {len(data)}',
        f'Добавлено новых ресурсов: {len(results["created"])}',
        f'Обновлено существовавших ресурсов: {len(results["updated"])}',
        f'Не удалась загрузка ресурсов: {len(results["failed to create"])}',
        f'\nСписок обновленных ресурсов:\n {results["updated"]}',
        f'\nЧто не удалось загрузить:\n {results["failed to create"]}'
    ]
    return '\n'.join(addition_info)


def get_del_resource_stats_msg(data, results):
    addition_info = [
        f'\nНайдено ресурсов для удаления во входящих параметрах: {len(data)}',
        f'Удалено ресурсов: {len(results["deleted"])}',
        f'Не найдено реусрсов в БД: {len(results["not_found"])}',
        f'\nЧто именно не было найдено:\n {str(results["not_found"])}'
    ]
    return '\n'.join(addition_info)
