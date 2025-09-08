from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from database.connection import Base
from entities.base import AuditMixin
from pydantic import BaseModel, Field, validator
from typing import Optional, List

class Tipo_Habitacion(AuditMixin, Base):
    __tablename__ = 'tipo_habitacion'

    id_tipo = Column(Integer, primary_key=True)
    nombre_tipo = Column(String)
    descripcion = Column(Text)

    habitaciones = relationship("Habitacion", back_populates="tipo_habitacion")
    
class Tipo_HabitacionBase(BaseModel):
    id_tipo: int = Field(..., gt=0)
    nombre_tipo: str = Field(..., min_length=1, max_length=100)
    descripcion: str = Field(..., min_length=1)

    @validator('id_tipo')
    def id_tipo_positivo(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El ID de tipo debe ser un número positivo')
        return v

    @validator('nombre_tipo')
    def nombre_tipo_no_vacio(cls, v):
        if not v.strip():
            raise ValueError('El nombre del tipo no puede estar vacío')
        return v.strip()

    @validator('descripcion')
    def descripcion_no_vacia(cls, v):
        if not v.strip():
            raise ValueError('La descripción no puede estar vacía')
        return v.strip()

class Tipo_HabitacionCreate(Tipo_HabitacionBase):
    pass

class Tipo_HabitacionUpdate(Tipo_HabitacionBase):
    id_tipo: Optional[int] = None
    nombre_tipo: Optional[str] = None
    descripcion: Optional[str] = None

    @validator('id_tipo')
    def id_tipo_positivo(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El ID de tipo debe ser un número positivo')
        return v

     @validator('nombre_tipo')
    def nombre_tipo_no_vacio(cls, v):
        if not v.strip():
            raise ValueError('El nombre del tipo no puede estar vacío')
        return v.strip()

    @validator('descripcion')
    def descripcion_no_vacia(cls, v):
        if not v.strip():
            raise ValueError('La descripción no puede estar vacía')
        return v.strip()

class Tipo_HabitacionResponse(Tipo_HabitacionBase):
    id_tipo: int
    nombre_tipo: str
    descripcion: str

    class Config:
        orm_mode = True

class Tipo_HabitacionListResponse(BaseModel):
    """Esquema para lista de tipos de habitación"""
    tipos_habitacion: List[Tipo_HabitacionResponse]
    
    class Config:
        from_attributes = True