from pydantic import BaseModel, EmailStr , AnyUrl, Field, field_validator,model_validator
from typing import List , Dict , Optional , Annotated

class Patient(BaseModel):

    name:str
    email: EmailStr
    age: int
    weight: float
    married: bool = False
    allergies: List[str] = []
    contact_details: Dict[str,str]

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 must have an emergency contact')
        return model

def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.allergies)
    print(patient.married)
    print(patient.contact_details)
    print('updated')

patient_info = {'name':'Siddhesh' , 'age':65 ,'email':'abc@hdfc.com','weight':60.00,'married':True,'allergies':['pollen','dust'],'linkedin_url':'https://linkedin.com/5332', 'weight':60.00 , 'contact_details':{'phone':'2353462','emergency':'4566'}}

patient1 = Patient(**patient_info)

update_patient_data(patient1)