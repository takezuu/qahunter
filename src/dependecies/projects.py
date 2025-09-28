from fastapi import Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.database import get_session
from src.models.projects import Projects


async def project_exists(project_id: int, session: AsyncSession = Depends(get_session)):
    query = select(Projects).where(Projects.id == project_id)
    project = session.exec(query).first()
    if project:
        return project
    raise HTTPException(status_code=404, detail="Project not found")
