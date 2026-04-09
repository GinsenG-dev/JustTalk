from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.database import get_db
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate, PostOut, PostUpdate
from app.services.auth import get_current_user

router = APIRouter(prefix="/posts", tags=["posts"])


def _get_post_or_404(db: Session, post_id: int) -> Post:
    post = db.scalar(
        select(Post)
        .options(selectinload(Post.user))
        .where(Post.id == post_id)
    )
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.get("", response_model=list[PostOut])
def list_posts(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    posts = db.scalars(
        select(Post)
        .options(selectinload(Post.user))
        .order_by(Post.created_at.desc())
    ).all()
    return posts


@router.get("/{post_id}", response_model=PostOut)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return _get_post_or_404(db, post_id)


@router.post("", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(
    data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = Post(
        user_id=current_user.id,
        title=data.title,
        body=data.body,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    post = db.scalar(
        select(Post)
        .options(selectinload(Post.user))
        .where(Post.id == post.id)
    )
    assert post is not None
    return post


@router.patch("/{post_id}", response_model=PostOut)
def update_post(
    post_id: int,
    data: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = _get_post_or_404(db, post_id)
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    payload = data.model_dump(exclude_unset=True)
    for key, value in payload.items():
        setattr(post, key, value)
    db.add(post)
    db.commit()
    db.refresh(post)
    post = db.scalar(
        select(Post)
        .options(selectinload(Post.user))
        .where(Post.id == post.id)
    )
    assert post is not None
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = _get_post_or_404(db, post_id)
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    db.delete(post)
    db.commit()
    return None
