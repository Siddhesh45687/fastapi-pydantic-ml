from pydantic import BaseModel, EmailStr , AnyUrl, Field, field_validator,model_validator,computed_field
from typing import List , Dict , Optional , Annotated

class Patient(BaseModel):

    name:str
    email: EmailStr
    age: int
    weight: float # kg
    height: float # mtr
    married: bool = False
    allergies: List[str] = []
    contact_details: Dict[str,str]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi













def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.allergies)
    print('BMI',patient.bmi)
    print(patient.married)
    print(patient.contact_details)
    print('updated')

patient_info = {'name':'Siddhesh' , 'age':65 ,'email':'abc@hdfc.com','weight':60.00,'height':1.71,'married':True,'allergies':['pollen','dust'],'linkedin_url':'https://linkedin.com/5332',  'contact_details':{'phone':'2353462','emergency':'4566'}}

patient1 = Patient(**patient_info)

update_patient_data(patient1)