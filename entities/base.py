from sqlalchemy import Column, Integer, DateTime, func

class AuditMixin:
    id_usuario_crea = Column(Integer, nullable=False)
    id_usuario_edita = Column(Integer, nullable=True)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)