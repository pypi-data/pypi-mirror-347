from typing import Optional
from dataclasses import dataclass

@dataclass
class Contact:
    id: str
    organizationId: str
    salutation: str
    firstName: str
    lastName: str
    email: str
    billingStreet: str
    billingCity: str
    billingStateProvince: str
    billingCountry: str
    billingZipPostalCode: str
    accountId: Optional[str] = None
    phone: Optional[str] = None
    accountName: Optional[str] = None  # Read-only field set by server
    externalId: Optional[str] = None
    accountExternalId: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Contact':
        """Create a Contact instance from a dictionary."""
        return cls(
            id=data['id'],
            organizationId=data['organizationId'],
            salutation=data['salutation'],
            firstName=data['firstName'],
            lastName=data['lastName'],
            email=data['email'],
            billingStreet=data['billingStreet'],
            billingCity=data['billingCity'],
            billingStateProvince=data['billingStateProvince'],
            billingCountry=data['billingCountry'],
            billingZipPostalCode=data['billingZipPostalCode'],
            accountId=data.get('accountId'),
            phone=data.get('phone'),
            accountName=data.get('accountName'),
            externalId=data.get('externalId'),
            accountExternalId=data.get('accountExternalId')
        )

    def to_dict(self) -> dict:
        """Convert the Contact instance to a dictionary."""
        data = {
            'id': self.id,
            'organizationId': self.organizationId,
            'salutation': self.salutation,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'billingStreet': self.billingStreet,
            'billingCity': self.billingCity,
            'billingStateProvince': self.billingStateProvince,
            'billingCountry': self.billingCountry,
            'billingZipPostalCode': self.billingZipPostalCode,
        }
            
        if self.phone is not None:
            data['phone'] = self.phone
        if self.accountExternalId is not None:
            data['accountExternalId'] = self.accountExternalId
        if self.accountId is not None:
            data['accountId'] = self.accountId
        if self.externalId is not None:
            data['externalId'] = self.externalId    
            
        return data

@dataclass
class CreateContactRequest:
    salutation: str
    firstName: str
    lastName: str
    email: str
    billingStreet: str
    billingCity: str
    billingStateProvince: str
    billingCountry: str
    billingZipPostalCode: str
    accountId: Optional[str] = None
    accountExternalId: Optional[str] = None
    phone: Optional[str] = None
    externalId: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert the CreateContactRequest instance to a dictionary."""
        data = {
            'salutation': self.salutation,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'billingStreet': self.billingStreet,
            'billingCity': self.billingCity,
            'billingStateProvince': self.billingStateProvince,
            'billingCountry': self.billingCountry,
            'billingZipPostalCode': self.billingZipPostalCode,
        }
            
        if self.accountId is not None:
            data['accountId'] = self.accountId
        if self.accountExternalId is not None:
            data['accountExternalId'] = self.accountExternalId
        if self.phone is not None:
            data['phone'] = self.phone
        if self.externalId is not None:
            data['externalId'] = self.externalId
            
        return data 