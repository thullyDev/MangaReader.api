from fastapi import APIRouter
from typing import Any, Dict, List, Optional

router: APIRouter = APIRouter(prefix="/manga")

@router.get("/recent")
async def start() -> Dict[str, Any]:
     return {}
