# encoding: utf-8
from uuid import uuid4
from datetime import datetime
from test.json_utils import list_to_json

class BaseModel(object):
    """Base class"""
    # 1:enabled     0:disabled
    status_ = ''
    created_time = ''
    creater =''
    modified_time = ''
    modifier = ''

    def __init__(self,status_ ,created_time,creater,modified_time,modifier):
        self.status_ =status_
        self.created_time = created_time
        self.creater = creater
        self.modified_time = modified_time
        self.modifier = modifier

class Comment(BaseModel):
    """Represents Proected comments."""

    id = ''
    name = ''
    text = ''
    date = ''

    def __init__(self,name,text,date,status_ ,created_time,creater,modified_time,modifier):
        super(Comment,self).__init__(status_ ,created_time,creater,modified_time,modifier)
        self.id =uuid4()
        self.name = name
        self.text = text
        self.date = date


comm1=Comment(name='zhangsan',
             text='1233frkfrfmrf',
             date=datetime.now(),
             status_='1',
             created_time=datetime.now(),
             creater ='null',
             modified_time=datetime.now(),
             modifier ='null')

comm2=Comment(name='test',
             text='6666666',
             date=datetime.now(),
             status_='0',
             created_time=datetime.now(),
             creater ='est',
             modified_time=datetime.now(),
             modifier ='tt')
objs=[]
objs.append(comm1)
objs.append(comm2)
#print(dir(comm1))
print(list_to_json(objs))

