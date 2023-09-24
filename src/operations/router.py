import time

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi_cache.decorator import cache 
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from operations.models import operation
from operations.shemas import OperationCreate

router = APIRouter(
    prefix="/operations",
    tags=["Operations"]
)

@router.get("/long-operations")
@cache(expire=30)
def get_long_op():
    time.sleep(5)
    return "Много данных"

@router.get("")
async def get_specific_operations(
        operation_type: str,
        session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.all(),
            "details": None
        }
    except Exception:
        # Передать ошибку разработчикам
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })

@router.post("/")
async def add__specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    new_operation.date = new_operation.date.replace(tzinfo=None)
    stmt = insert(operation).values(**new_operation.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}