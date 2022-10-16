from models import ItemModel, ResourceModel
from parse_handler import ResourceHandler

def load_test_data():
    resource = ResourceModel(
        resource_name = 'nur.kz',
        resource_url = 'https://www.nur.kz/',
        top_tag = ['a', {'class': 'post-preview-text js-article-link'}],
        bottom_tag = ['div', {'class': 'formatted-body io-article-body'}],
        title_cut = ['h1', {'class': 'main-headline js-main-headline'}],
        date_cut = ['time', {'class': 'datetime datetime--publication'}],
    )
    return resource

def main():
    resource = load_test_data()
    handler = ResourceHandler()
    items_list = handler(resource)
    with open('parse_result.txt', 'w') as result_file:
        for item in items_list:
            result_file.write(f'{str(item)}\n')
        result_file.write(f'ресурс:\n{str(resource)}')
        result_file.write(f'загружено новостей:\n{len(items_list)}')
        result_file.write(f'не удалось загрузить:\n{len(ResourceHandler.not_downloaded)}')
        result_file.write("\n".join(ResourceHandler.not_downloaded))


if __name__ == '__main__':
    main()
