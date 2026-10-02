from pydantic import BaseModel


class StudentBase(BaseModel):
  name: str
  email: str
  course: str
  semester: int


class StudentCreate(StudentBase):
  pass


class StudentUpdate(BaseModel):
  name: str | None = None
  email: str | None = None
  course: str | None = None
  semester: int | None = None


class StudentResponse(StudentBase):
  id: int

  class Config:
    from_attributes = True