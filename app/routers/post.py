from typing import List, Optional
from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, Response, status, APIRouter
from ..database import get_db
from .. import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts;""")
    # posts = cursor.fetchall()
    print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def create_posts(post: schemas.CreatePost, db : Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(title=post.title, content=post.content, published=post.published, owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", status_code=status.HTTP_302_FOUND,response_model=schemas.Post)
def get_posts(id: int, db : Session = Depends(get_db)):

    # cursor.execute(""" SELECT * FROM posts WHERE id = (%s) """, (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"message with id {id} was not found")
    return post

@router.delete("/{id}")
def delete_posts(id: int, db : Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = (%s) RETURNING * """, (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this request")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_posts(id: int, updated_post: schemas.CreatePost, db : Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
    #                (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this request")

    updated_post_dict = updated_post.model_dump()
    post_query.update(updated_post_dict,synchronize_session=False)
    db.commit()
    return post_query.first()
