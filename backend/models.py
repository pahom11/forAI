import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class SoftDeleteModel(SQLModel):
    deleted_at: Optional[datetime.datetime] = Field(default=None, index=True)

    def soft_delete(self):
        self.deleted_at = datetime.datetime.utcnow()


class User(SoftDeleteModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    goal_score: Optional[int] = Field(default=None)
    daily_xp_goal: Optional[int] = Field(default=None)
    streak_count: int = Field(default=0)
    level: int = Field(default=1)
    total_xp: int = Field(default=0)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


class Topic(SoftDeleteModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    sprints: List["Sprint"] = Relationship(back_populates="topic")


class Sprint(SoftDeleteModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    topic_id: int = Field(foreign_key="topic.id")
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    topic: Topic = Relationship(back_populates="sprints")
    atoms: List["Atom"] = Relationship(back_populates="sprint")


class Atom(SoftDeleteModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    content: str
    sprint_id: int = Field(foreign_key="sprint.id")
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    sprint: Sprint = Relationship(back_populates="atoms")
    questions: List["Question"] = Relationship(back_populates="atom")


class Question(SoftDeleteModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    question_type: str
    atom_id: int = Field(foreign_key="atom.id")
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    atom: Atom = Relationship(back_populates="questions")
    answers: List["Answer"] = Relationship(back_populates="question")


class Answer(SoftDeleteModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    is_correct: bool
    question_id: int = Field(foreign_key="question.id")
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    question: Question = Relationship(back_populates="answers")


class Attempt(SoftDeleteModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    sprint_id: int = Field(foreign_key="sprint.id")
    completed: bool = Field(default=False)
    score: int = Field(default=0)
    lives_remaining: int = Field(default=3)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


class XPEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    xp_amount: int
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


class Achievement(SoftDeleteModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


class ReviewSchedule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    atom_id: int = Field(foreign_key="atom.id")
    next_due_date: datetime.datetime
    ease_factor: float = Field(default=2.5)
    repetitions: int = Field(default=0)
    interval: int = Field(default=0)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
