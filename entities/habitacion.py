from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base
from entities.base import AuditMixin
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class Habitacion(AuditMixin, Base):
    __tablename__ = 'habitacion'

    id_habitacion = Column(Integer, primary_key=True)
    numero = Column(String)
    id_tipo = Column(Integer, ForeignKey('tipo_habitacion.id_tipo'))
    precio = Column(Float)
    disponible = Column(Boolean)

    tipo_habitacion = relationship("Tipo_Habitacion", back_populates="habitaciones")
    reservas = relationship("Reserva", back_populates="habitacion")
    
class HabitacionBase(BaseModel):
    numero: str = Field(..., min_length=1, max_length=10)
    id_tipo: int = Field(..., gt=0)
    precio: float = Field(..., ge=0)
    disponible: bool = Field(default=False)

    @validator('numero')
    def numero_no_vacio(cls, v):
        if not v.strip():
            raise ValueError('El número no puede estar vacío')
        return v.strip()

class HabitacionCreate(HabitacionBase):
    pass

class HabitacionUpdate(BaseModel):
    numero: Optional[str] = None
    id_tipo: Optional[int] = None
    precio: Optional[float] = None
    disponible: Optional[bool] = None

    @validator('numero')
    def numero_no_vacio(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El número no puede estar vacío')
        return v.strip() if v else v

class HabitacionResponse(HabitacionBase):
    id_habitacion: int
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        
class HabitacionListResponse(BaseModel):
    """Esquema para lista de habitaciones"""
    habitaciones: list[HabitacionResponse]

    class Config:
        from_attributes = True