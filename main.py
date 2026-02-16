from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

import models, schemas, auth, database


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="API de Gestión de Incidencias",
    description="Examen FastAPI + MySQL + JWT",
    version="1.0.0"
)


@app.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    if form_data.username == "admin" and form_data.password == "1234":
        access_token = auth.create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/incidencias", response_model=List[schemas.IncidenciaResponse])
def read_incidencias(db: Session = Depends(database.get_db)):
    incidencias = db.query(models.Incidencia).all()
    return incidencias


@app.post("/incidencias", response_model=schemas.IncidenciaResponse)
def create_incidencia(
    incidencia: schemas.IncidenciaCreate, 
    db: Session = Depends(database.get_db),
    current_user: str = Depends(auth.get_current_user) 
):

    db_incidencia = models.Incidencia(**incidencia.dict())
    db.add(db_incidencia)
    db.commit()
    db.refresh(db_incidencia)
    return db_incidencia


@app.get("/users/me")
def read_users_me(current_user: str = Depends(auth.get_current_user)):
    return {"usuario_autenticado": current_user, "mensaje": "Tienes acceso al área protegida"}