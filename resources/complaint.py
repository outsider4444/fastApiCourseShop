from typing import List

from fastapi import APIRouter, Depends
from starlette.requests import Request

from managers.auth import oauth2_scheme, is_complainer, is_admin
from managers.complaint import ComplaintManager
from schemas.request.complaint import ComplaintIn
from schemas.response.complaint import ComplaintOut

router = APIRouter(tags=["Complaints"])


# endpoints для предметов
@router.get("/complaints/",
            dependencies=[Depends(oauth2_scheme)], response_model=List[ComplaintOut],
            status_code=200)
async def get_complaints(request: Request):
    user = request.state.user
    return await ComplaintManager.get_complaints(user)


@router.post("/complaints/",
             dependencies=[Depends(oauth2_scheme), Depends(is_complainer)], response_model=ComplaintOut,
             status_code=201)
async def create_complaint(request: Request, complaint: ComplaintIn):
    user = request.state.user
    return await ComplaintManager.create_complaint(complaint.dict(), user)


@router.delete("/complaints/{complaint_id}/",
               dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
               status_code=202)
async def delete_complaint(complaint_id: int):
    await ComplaintManager.delete(complaint_id)


