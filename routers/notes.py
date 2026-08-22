from datetime import datetime
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



@notes_router.get("/getNotes", response_model=list[NotesResponse])
async def get_notes(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(db_model.NotesDB).filter(
        db_model.NotesDB.owner_id == current_user.id,
        db_model.NotesDB.is_deleted == False
    ).all()



@notes_router.post("/createNotes",response_model=NotesResponse)
async def create_notes(newNotes:CreateNotes,current_user = Depends(get_current_user) ,db:Session = Depends(get_db)):
    db_notes = db_model.NotesDB(owner_id=current_user.id ,title=newNotes.title ,content = newNotes.content)
    db.add(db_notes)
    db.commit()
    db.refresh(db_notes)
    return db_notes



@notes_router.put("/updateNotes/{notes_id}", response_model=NotesResponse)
async def update_notes(notes_id: int, updateNotes: UpdateNotes, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    notes = db.query(db_model.NotesDB).filter(db_model.NotesDB.id == notes_id).first()
    if not notes:
        raise HTTPException(status_code=404, detail="Note does not exist")
    if notes.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this note")
    if notes.is_deleted:
        raise HTTPException(status_code=404, detail="Note has been deleted")

    # conflict detection — client must send the version it started editing from
    if notes.version != updateNotes.base_version:
        raise HTTPException(
            status_code=409,
            detail=f"Conflict: note was modified on another device (server version: {notes.version})"
        )

    if updateNotes.title is not None:
        notes.title = updateNotes.title
    if updateNotes.content is not None:
        notes.content = updateNotes.content

    notes.version += 1  # increment version on every successful save
    db.commit()
    db.refresh(notes)
    return notes




@notes_router.delete("/deleteNotes/{notes_id}")
async def delete_notes(notes_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    notes = db.query(db_model.NotesDB).filter(db_model.NotesDB.id == notes_id).first()
    if not notes or notes.is_deleted:
        raise HTTPException(status_code=404, detail="Note does not exist")
    if notes.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    # soft delete — mark as deleted, keep in DB for 30-day recovery
    notes.is_deleted = True
    notes.deleted_at = datetime.utcnow()
    db.commit()
    return {"message": "Note deleted successfully"}


@notes_router.get("/trash", response_model=list[NotesResponse])
async def get_trash(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Returns notes deleted in the last 30 days — recoverable."""
    return db.query(db_model.NotesDB).filter(
        db_model.NotesDB.owner_id == current_user.id,
        db_model.NotesDB.is_deleted == True
    ).all()


@notes_router.post("/restoreNotes/{notes_id}", response_model=NotesResponse)
async def restore_notes(notes_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    """Recover a soft-deleted note."""
    notes = db.query(db_model.NotesDB).filter(db_model.NotesDB.id == notes_id).first()
    if not notes or not notes.is_deleted:
        raise HTTPException(status_code=404, detail="Note not found in trash")
    if notes.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    notes.is_deleted = False
    notes.deleted_at = None
    db.commit()
    db.refresh(notes)
    return notes


    
    


    










