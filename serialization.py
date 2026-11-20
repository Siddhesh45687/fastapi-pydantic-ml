from pydantic import BaseModel

class Address(BaseModel):

    city: str
    state: str
    pin: str

class Patient(BaseModel):

    name:str
    gender:str
    age: int
    address:Address


address_dict = {'city':'Mumbai','state':'Maharashtra','pin':'400561'}

address1 = Address(**address_dict)

patient_dict = {'name':'Siddhesh','gender':'male','age':20,'address':address1}

patient1 = Patient(**patient_dict)

temp = patient1.model_dump_json(include=['name'])

print(temp)
print(type(temp))