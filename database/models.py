from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str
    password: str
    role: str

@dataclass
class Student:
    student_id: int
    name: str
    gender: str
    age: int
    location: str
    famsize: str
    pstatus: str
    medu: int
    fedu: int
    traveltime: int
    studytime: int
    failures: int
    schoolsup: str
    famsup: str
    paid: str
    activities: str
    nursery: str
    higher: str
    internet: str
    famrel: int
    freetime: int
    health: int
    absences: int
    score: int
    performance_category: str
