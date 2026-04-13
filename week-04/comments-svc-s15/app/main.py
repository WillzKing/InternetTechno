import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException, status
from typing import List
from datetime import datetime
from schemas import Comment, CommentCreate, CommentStatus

app = FastAPI(title="Comments Microservice")

comments_db: List[Comment] = []
id_counter = 1


@app.post("/comments/", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(comment: CommentCreate):
    global id_counter
    new_comment = Comment(
        id=id_counter,
        name=comment.name,
        author=comment.author,
        created_at=datetime.now(),
        status=CommentStatus.NEW
    )
    comments_db.append(new_comment)
    id_counter += 1
    return new_comment


@app.get("/comments/", response_model=List[Comment])
async def get_comments():
    return comments_db


@app.get("/comments/{comment_id}", response_model=Comment)
async def get_comment(comment_id: int):
    comment = next((c for c in comments_db if c.id == comment_id), None)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Комментарий с ID {comment_id} не найден"
        )
    return comment


@app.post("/comments/{comment_id}/pay")
async def pay_comment(comment_id: int):
    comment = next((c for c in comments_db if c.id == comment_id), None)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Комментарий с ID {comment_id} не найден"
        )
    
    if comment.status != CommentStatus.NEW:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Нельзя оплатить комментарий в статусе {comment.status.value}"
        )
    
    import random
    if random.random() < 0.3:
        comment.status = CommentStatus.CANCELLED
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка оплаты"
        )
    
    comment.status = CommentStatus.PAID
    return {"message": "Оплата прошла успешно", "status": comment.status.value}


@app.post("/comments/{comment_id}/complete")
async def complete_comment(comment_id: int):
    comment = next((c for c in comments_db if c.id == comment_id), None)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Комментарий с ID {comment_id} не найден"
        )
    
    if comment.status != CommentStatus.PAID:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Нельзя завершить комментарий в статусе {comment.status.value}"
        )
    
    comment.status = CommentStatus.DONE
    return {"message": "Комментарий завершён", "status": comment.status.value}


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "comments-svc-s15"}