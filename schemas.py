from pydantic import BaseModel


class IncidenciaBase(BaseModel):
    titulo: str
    descripcion: str
    prioridad: str
    estado: str


class IncidenciaCreate(IncidenciaBase):
    pass


class IncidenciaResponse(IncidenciaBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str