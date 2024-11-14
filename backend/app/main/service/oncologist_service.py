from app.main.model.person import Person
from app.main.model.oncologist import Oncologist

def get_all_oncologists():
    output = []
    for i in Oncologist.get_all():
        i.person = Person.get_by_id(i.people_id)
        output.append(i)
    return output

def get_profile(id: int):
    x = Oncologist.get_by_people_id(id)
    x.person = Person.get_by_id(id)
    return x
