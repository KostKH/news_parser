import json

class ResourceModel():
    """Класс для обмена данными с таблицей БД resourse"""

    def __init__(
        self,
        RESOURCE_ID=None,
        RESOURCE_NAME=None,
        RESOURCE_URL=None,
        top_tag=None,
        bottom_tag=None,
        title_cut=None,
        date_cut=None,
    ):
        self.resource_id = RESOURCE_ID
        self.resource_name = RESOURCE_NAME
        self.resource_url = RESOURCE_URL
        self.top_tag = json.loads(top_tag) if isinstance(
            top_tag,
            str
        ) else top_tag
        self.bottom_tag = json.loads(bottom_tag) if isinstance(
            bottom_tag,
            str
        ) else bottom_tag
        self.title_cut = json.loads(title_cut) if isinstance(
            title_cut,
            str
        ) else title_cut
        self.date_cut = json.loads(date_cut) if isinstance(
            date_cut,
            str
        ) else date_cut
    
    def formated_for_db(self):
        data = {
            'RESOURCE_NAME': str(self.resource_name),
            'RESOURCE_URL': str(self.resource_url),
            'top_tag': json.dumps(self.top_tag),
            'bottom_tag': json.dumps(self.bottom_tag),
            'title_cut': json.dumps(self.title_cut),
            'date_cut': json.dumps(self.date_cut),
        }
        return data

    def __str__(self):
        return '\n'.join(
            [
                str(self.resource_id),
                str(self.resource_name),
                str(self.resource_url),
                str(self.top_tag),
                str(self.bottom_tag),
                str(self.title_cut),
                str(self.date_cut)
            ]

        )


class ItemModel():
    """Класс для обмена данными с таблицей БД items"""

    def __init__(
        self,
        id=None,
        res_id=None,
        link=None,
        title=None,
        content=None,
        nd_date=None,
        s_date=None,
        not_date=None,
    ):
        self.id = id
        self.res_id = res_id
        self.link = link
        self.title = title
        self.content = content
        self.nd_date = nd_date
        self.s_date = s_date
        self.not_date = not_date
    
    def __str__(self):
        return '\n'.join(
            [
                f'id: {str(self.id)}',
                f'res_id: {str(self.res_id)}',
                f'link: {str(self.link)}',
                f'title: {str(self.title)}',
                f'nd_date: {str(self.nd_date)}',
                f's_date: {str(self.s_date)}',
                f'not_date: {str(self.not_date)}'
            ]
        )

    def formated_for_db(self):
        data = {
            'res_id':int(self.res_id),
            'link':str(self.link),
            'title':str(self.title),
            'content':str(self.content),
            'nd_date':int(self.nd_date),
            's_date':int(self.s_date),
            'not_date':str(self.not_date),
        }
        return data
