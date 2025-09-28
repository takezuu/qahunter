from sqlmodel import Field, SQLModel


class Projects(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    project_name: str = Field(index=True)


class ProjectsResponse(SQLModel):
    id: int = Field(primary_key=True, index=True)
    project_name: str = Field(index=True)


class ProjectAddedResponse(SQLModel):
    id: int = Field(primary_key=True, index=True)
    project_name: str = Field(index=True)


class ProjectUpdatedResponse(SQLModel):
    message: str
    updated_project: ProjectsResponse


class ProjectAdd(SQLModel):
    project_name: str = Field(index=True)


class ProjectPut(SQLModel):
    project_name: str = Field(index=True)
