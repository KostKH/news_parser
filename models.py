import json

class ResourceModel():
    """Класс для обмена данными с таблицей БД resourse"""

    resource_id = 'Enter resource id',
    resource_name = 'Enter resource_name'
    resource_url = 'Enter resource_url'
    top_tag = 'Enter top_tag'
    bottom_tag = 'Enter bottom_tag'
    title_cut = 'Enter title_cut'
    date_cut = 'Enter date_cut'
    count = 0
    
    def __init__(
        self,
        resource_name,
        resource_url,
        top_tag,
        bottom_tag,
        title_cut,
        date_cut,
    ):
        ResourceModel.count +=1
        self.resource_id = ResourceModel.count
        self.resource_name = resource_name
        self.resource_url = resource_url
        self.top_tag = top_tag
        self.bottom_tag = bottom_tag
        self.title_cut = title_cut
        self.date_cut = date_cut
    

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

    id = 'Enter id'
    res_id = 'Enter res_id'
    link = 'Enter link'
    title = 'Enter title'
    content = 'Enter content'
    nd_date = 'Enter nd_date'
    s_date = 'Enter s_date'
    not_date = 'Enter not_date'
    count = 0

    def __init__(
        self,
        res_id,
        link,
        title=None,
        content=None,
        nd_date=None,
        s_date=None,
        not_date=None,
    ):
        ItemModel.count += 1
        self.id = ItemModel.count
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
                str(self.content),
                str(self.nd_date),
                str(self.s_date),
                str(self.not_date)
            ]
        )
