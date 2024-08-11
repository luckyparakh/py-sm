from fastapi import HTTPException, Depends, status, APIRouter
from .. import models, schemas, outh2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostVoteOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, search: Optional[str] = ""):
    # records = db.query(models.Posts).filter(
    #     models.Posts.title.contains(search)).limit(limit).all()
    # SELECT postsa.*, count(votes.post_id) as votes FROM public.postsa left join votes on postsa.id=votes.post_id group by postsa.id;

    records = db.query(models.Posts, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Posts.id == models.Votes.post_id, isouter=True).filter(models.Posts.title.contains(search)).group_by(models.Posts.id).limit(limit).all()
    return records  # FastAPI will automatically convert this to JSON


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db), logged_in_user: models.Users = Depends(outh2.get_current_user)):
    # new_post = models.Posts(title=payload.title, content=payload.content,published=payload.publish)
    new_post = models.Posts(**payload.model_dump())
    new_post.user_id = logged_in_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{post_id}", response_model=schemas.PostVoteOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    # post = db.query(models.Posts).filter(models.Posts.id == post_id).first()
    post = db.query(models.Posts, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Posts.id == models.Votes.post_id, isouter=True).filter(models.Posts.id == post_id).group_by(models.Posts.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {post_id} not found")
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), logged_in_user: models.Users = Depends(outh2.get_current_user)):

    # cursor.execute(
    #     "DELETE FROM posts WHERE id = %s returning *", (str(post_id),))
    # del_post = cursor.fetchone()
    del_q = db.query(models.Posts).filter(models.Posts.id == post_id)
    del_post = del_q.first()
    if not del_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {post_id} not found")
    if del_post.user_id != logged_in_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not allowed to delete this post")
    del_q.delete(synchronize_session=False)
    db.commit()
    return


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), logged_in_user: models.Users = Depends(outh2.get_current_user)):
    # cursor.execute("Update posts SET title = %s, content = %s, published = %s WHERE id = %s returning *",
    #                (post.title, post.content, post.publish, id))
    # post_to_update = cursor.fetchone()
    up_q = db.query(models.Posts).filter(models.Posts.id == id)
    post = up_q.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")

    if post.user_id != logged_in_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not allowed to update this post")
    up_q.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return up_q.first()
