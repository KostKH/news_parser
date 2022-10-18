import json

list = [
    {
        'RESOURCE_NAME': 'nur.kz',
        'RESOURCE_URL': 'https://www.nur.kz',
        'top_tag': ['a', {'class': 'post-preview-text js-article-link'}],
        'bottom_tag': ['div', {'class': 'formatted-body io-article-body'}],
        'title_cut': ['h1', {'class': 'main-headline js-main-headline'}],
        'date_cut': ['time', {'class': 'datetime datetime--publication'}],
    }
]
with open('resources.json', 'w') as file:
    file.write(json.dumps(list))
