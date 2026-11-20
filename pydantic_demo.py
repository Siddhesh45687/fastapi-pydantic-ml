from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):

    name: Annotated[str, Field(max_length=50, title='Name of the Patient', description='Give the name of the patient is less than 50 chars',examples=['Nitish','Amit'])]
    age: int = Field(gt=0,lt=100)
    email: EmailStr
    linkedin_url: AnyUrl
    weight: Annotated[float , Field(gt=0 , strict=True)]
    married: Annotated[bool, Field(default=None, description='Is the patient married or not')]
    allergies: Annotated[Optional[List[str]],Field(default=None,max_length=5)]
    contact_details: Dict[str,str]

def insert_patient_data(patient: Patient):

    print(patient.name)
    print(patient.email)
    print(patient.linkedin_url)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print('inserted')

def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print('updated')


patient_info = {'name':'Siddhesh' , 'age':21 ,'email':'abc@gmail.com','linkedin_url':'https://linkedin.com/5332', 'weight':60.00 , 'contact_details':{'phone':'2353462'}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)