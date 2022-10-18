import json

def load_test_data():
    data = [
        {
            'RESOURCE_NAME': 'nur.kz',
            'RESOURCE_URL': 'https://www.nur.kz',
            'top_tag': json.dumps(['a', {'class': 'post-preview-text js-article-link'}]),
            'bottom_tag': json.dumps(['div', {'class': 'formatted-body io-article-body'}]),
            'title_cut': json.dumps(['h1', {'class': 'main-headline js-main-headline'}]),
            'date_cut': json.dumps(['time', {'class': 'datetime datetime--publication'}]),
        },
        {
            'RESOURCE_NAME': 'scientificrussia.ru/news',
            'RESOURCE_URL': 'https://scientificrussia.ru/news/',
            'top_tag': json.dumps(['a', {'class': 'post-preview-text js-article-link'}]),
            'bottom_tag': json.dumps(['div', {'class': 'formatted-body io-article-body'}]),
            'title_cut': json.dumps(['h1', {'class': 'main-headline js-main-headline'}]),
            'date_cut': json.dumps(['time', {'class': 'datetime datetime--publication'}]),
        },
    ]
    return data