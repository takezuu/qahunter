from sqlmodel import Field, SQLModel


class Projects(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    project_name: str = Field(index=True)

class ProjectsResponse(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    project_name: str = Field(index=True)
