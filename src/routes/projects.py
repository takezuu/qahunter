from typing import List, Annotated

from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlmodel import Session, select

from src.database import get_session
from src.dependecies.projects import project_exists
from src.models.projects import Projects, ProjectsResponse, ProjectAddedResponse, ProjectAdd, ProjectUpdatedResponse, \
    ProjectPut

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter()


@router.get("/projects", tags=["projects"], status_code=status.HTTP_200_OK,
            response_model=List[ProjectsResponse])
async def get_projects(session: SessionDep):
    projects = Projects
    query = select(projects)

    projects = session.exec(query).all()

    return projects


@router.get("/projects/{project_id}", tags=["projects"], status_code=status.HTTP_200_OK,
            response_model=ProjectsResponse)
async def get_project(project=Depends(project_exists)):
    return project


@router.post("/projects", tags=["projects"], status_code=status.HTTP_201_CREATED,
             response_model=ProjectAddedResponse)
async def create_project(project: ProjectAdd, session: SessionDep, request: Request):
    db_project = Projects(**project.model_dump())

    if db_project.project_name:
        query = select(Projects).where(Projects.project_name == db_project.project_name)
        project_name_exists = session.exec(query).first() is not None
        if project_name_exists:
            raise HTTPException(status_code=409, detail="Project name is already use")

    try:
        session.add(db_project)
        session.commit()
        session.refresh(db_project)
    except Exception as err:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'Failed create a project: {err}')
    return db_project


@router.patch("/projects/{project_id}", tags=["projects"], status_code=status.HTTP_200_OK,
            response_model=ProjectUpdatedResponse)
async def patch_project(session: SessionDep, update_data: ProjectPut, project: Projects = Depends(project_exists)):
    try:

        if update_data.project_name:
            query = select(Projects).where(Projects.project_name == update_data.project_name)
            is_project = session.exec(query).first() is not None
            if is_project:
                raise HTTPException(status_code=409, detail="Project name is already use")

        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(project, key, value)

        session.add(project)
        session.commit()
        session.refresh(project)

        return {"message": "Project updated successfully", "updated_project": project}
    except Exception as err:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))


@router.delete("/projects/{project_id}", tags=["projects"], status_code=status.HTTP_200_OK)
async def delete_project(session: SessionDep, project=Depends(project_exists)):
    try:
        if project:
            session.delete(project)
            session.commit()
            return {"message": "Project deleted successfully"}
        return {"message": "Project can't be deleted"}
    except Exception as err:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))
