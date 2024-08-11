from fastapi import HTTPException, Depends, status, APIRouter
from .. import models, schemas, outh2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)


# response_model=schemas.VoteResponse)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(payload: schemas.VoteBase, db: Session = Depends(get_db), logged_in_user: models.Users = Depends(outh2.get_current_user)):
    post = db.query(models.Posts).filter(
        models.Posts.id == payload.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {payload.post_id} not found")
    # if payload.vote_direction not in [-1, 1]:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                         detail="Vote direction can only be 1 or -1")
    vote_q = db.query(models.Votes).filter(models.Votes.post_id ==
                                           payload.post_id, models.Votes.user_id == logged_in_user.id)
    if payload.vote_direction == -1:
        if vote_q.first() is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"User with id: {logged_in_user.id} did not voted for post with id: {payload.post_id}")
        vote_q.delete(synchronize_session=False)
        db.commit()
        return {"message": f"Post with id: {payload.post_id} has been un-voted by user with id: {logged_in_user.id}"}
    if vote_q.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with id: {logged_in_user.id} already voted for post with id: {payload.post_id}")
    new_vote = models.Votes(post_id=payload.post_id, user_id=logged_in_user.id)
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)
    return {"message": f"Post with id: {payload.post_id} has been voted by user with id: {logged_in_user.id}"}
