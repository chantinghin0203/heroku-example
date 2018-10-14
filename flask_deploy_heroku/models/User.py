from jsonobject import *
from numpy import unicode


class Job(JsonObject):
    salary = IntegerProperty()


class User(JsonObject):
    username = StringProperty()
    name = StringProperty()
    active = BooleanProperty(default=False)
    date_joined = DateTimeProperty()
    tags = ListProperty(unicode)
    job = ObjectProperty(Job)


u = User({
    'name': u'John Doe',
    'username': u'jdoe',
    'active': False,
    'date_joined': '2013-08-05T02:46:58Z',
    'tags': [u'generic', u'anonymous'],
    'job': {"salary": 25450}
})

print(u.to_json())
print(u.job.salary)

