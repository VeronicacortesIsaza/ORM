from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class Reserva_Servicios(Base):
    __tablename__ = 'reserva_servicios'

    id_reserva = Column(Integer, ForeignKey('reserva.id_reserva'), primary_key=True)
    id_servicio = Column(Integer, ForeignKey('servicios_adicionales.id_servicio'), primary_key=True)

    reserva = relationship("Reserva", back_populates="servicios")
    servicio = relationship("Servicios_Adicionales", back_populates="reservas")
