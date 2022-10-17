import json

class ResourceModel():
    """Класс для обмена данными с таблицей БД resourse"""

    def __init__(
        self,
        resource_id=None,
        resource_name=None,
        resource_url=None,
        top_tag=None,
        bottom_tag=None,
        title_cut=None,
        date_cut=None,
    ):
        self.resource_id = resource_id
        self.resource_name = resource_name
        self.resource_url = resource_url
        self.top_tag = json.loads(top_tag)
        self.bottom_tag = json.loads(bottom_tag)
        self.title_cut = json.loads(title_cut)
        self.date_cut = json.loads(date_cut)
    
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
                str(self.id),
                str(self.res_id),
                str(self.link),
                str(self.title),
                str(self.nd_date),
                str(self.s_date),
                str(self.not_date)
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
