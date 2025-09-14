
from typing import List, Annotated

from fastapi import APIRouter, Depends, status, Request
from sqlmodel import Session, select
from src.database import get_session
from src.models.projects import Projects, ProjectsResponse

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter()

@router.get("/projects", tags=["projects"], status_code=status.HTTP_200_OK,
            response_model=List[ProjectsResponse])
async def get_users(session: SessionDep):

    projects = Projects
    query = select(projects)

    projects = session.exec(query).all()

    return projects