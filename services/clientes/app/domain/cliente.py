from datetime import datetime

class Cliente:
    def __init__(self, id, name, surname, email, birthdate, active=True,
                 created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.birthdate = birthdate
        self.active = active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "birthdate": str(self.birthdate),
            "active": self.active,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }