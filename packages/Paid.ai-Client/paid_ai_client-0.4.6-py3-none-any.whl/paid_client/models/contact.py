from typing import Optional
from dataclasses import dataclass

@dataclass
class Contact:
    id: str
    organizationId: str
    accountId: str
    salutation: str
    firstName: str
    lastName: str
    email: str
    billingStreet: str
    billingCity: str
    billingStateProvince: str
    billingCountry: str
    billingZipPostalCode: str
    phone: Optional[str] = None
    accountName: Optional[str] = None  # Read-only field set by server

    @classmethod
    def from_dict(cls, data: dict) -> 'Contact':
        """Create a Contact instance from a dictionary."""
        return cls(
            id=data['id'],
            organizationId=data['organizationId'],
            accountId=data['accountId'],
            salutation=data['salutation'],
            firstName=data['firstName'],
            lastName=data['lastName'],
            email=data['email'],
            billingStreet=data['billingStreet'],
            billingCity=data['billingCity'],
            billingStateProvince=data['billingStateProvince'],
            billingCountry=data['billingCountry'],
            billingZipPostalCode=data['billingZipPostalCode'],
            phone=data.get('phone'),
            accountName=data.get('accountName')  # Set from API response
        )

    def to_dict(self) -> dict:
        """Convert the Contact instance to a dictionary."""
        data = {
            'id': self.id,
            'organizationId': self.organizationId,
            'accountId': self.accountId,
            'salutation': self.salutation,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'billingStreet': self.billingStreet,
            'billingCity': self.billingCity,
            'billingStateProvince': self.billingStateProvince,
            'billingCountry': self.billingCountry,
            'billingZipPostalCode': self.billingZipPostalCode
        }
            
        if self.phone is not None:
            data['phone'] = self.phone
            
        return data

@dataclass
class CreateContactRequest:
    accountId: str
    salutation: str
    firstName: str
    lastName: str
    email: str
    billingStreet: str
    billingCity: str
    billingStateProvince: str
    billingCountry: str
    billingZipPostalCode: str
    phone: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert the CreateContactRequest instance to a dictionary."""
        data = {
            'accountId': self.accountId,
            'salutation': self.salutation,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'billingStreet': self.billingStreet,
            'billingCity': self.billingCity,
            'billingStateProvince': self.billingStateProvince,
            'billingCountry': self.billingCountry,
            'billingZipPostalCode': self.billingZipPostalCode
        }
            
        if self.phone is not None:
            data['phone'] = self.phone
            
        return data 