from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
import db_model
from models import CreateNotes, UpdateNotes, NotesResponse
from routers.user import get_current_user
from database import SessionLocal

notes_router = APIRouter()

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()



@notes_router.get("/getNotes",response_model=list[NotesResponse])
async def get_notes(db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    return db.query(db_model.NotesDB).filter(db_model.NotesDB.owner_id == current_user.id).all()



@notes_router.post("/createNotes",response_model=NotesResponse)
async def create_notes(newNotes:CreateNotes,current_user = Depends(get_current_user) ,db:Session = Depends(get_db)):
    db_notes = db_model.NotesDB(owner_id=current_user.id ,title=newNotes.title ,content = newNotes.content)
    db.add(db_notes)
    db.commit()
    db.refresh(db_notes)
    return db_notes



@notes_router.put("/updateNotes/{notes_id}",response_model=NotesResponse)
async def update_notes(notes_id:int,updateNotes:UpdateNotes,current_user = Depends(get_current_user) ,db:Session=Depends(get_db)):
    notes = db.query(db_model.NotesDB).filter(db_model.NotesDB.id == notes_id).first()
    if not notes :
        raise HTTPException(status_code=404,detail="Note does not exisit")
    if notes.owner_id != current_user.id :
        raise HTTPException(status_code=401 ,detail="User is not Autorised to access this Note")

    if updateNotes.title is not None:
        notes.title = updateNotes.title
    if updateNotes.content is not None :
        notes.content = updateNotes.content
    
    db.commit()
    db.refresh(notes)
    return notes




@notes_router.delete("/deleteNotes/{notes_id}")
async def delete_notes(notes_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    notes = db.query(db_model.NotesDB).filter(db_model.NotesDB.id == notes_id).first()
    if not notes:
        raise HTTPException(status_code=404, detail="Note does not exist")
    if notes.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(notes)
    db.commit()
    return {"message": "Note deleted successfully"}


    
    


    










