from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import List, Optional, Dict
from enum import Enum


class Priority(Enum):
    """Priority levels for tasks."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Owner:
    """Represents a pet owner."""
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str = "Owner"
    email: Optional[str] = None
    phone: Optional[str] = None
    available_minutes: int = 60
    preferences: Dict[str, str] = field(default_factory=dict)
    
    def update_info(self, **kwargs) -> None:
        """Update owner information."""
        pass
    
    def set_preference(self, key: str, value: str) -> None:
        """Set an owner preference."""
        pass
    
    def to_dict(self) -> Dict:
        """Serialize owner to dictionary."""
        pass


@dataclass
class Pet:
    """Represents a pet."""
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str = "Pet"
    species: str = "dog"  # e.g., "dog", "cat", "other"
    age_years: float = 0.0
    activity_level: str = "medium"  # e.g., "low", "medium", "high"
    feeding_times: List[time] = field(default_factory=list)
    medical_notes: Optional[str] = None
    owner_id: Optional[uuid.UUID] = None
    
    def needs_feeding_at(self, target_time: time) -> bool:
        """Check if pet needs feeding at a specific time."""
        pass
    
    def requires_medication_today(self, target_date: date) -> bool:
        """Check if pet requires medication today."""
        pass
    
    def to_dict(self) -> Dict:
        """Serialize pet to dictionary."""
        pass


@dataclass
class Task:
    """Definition of a reusable pet-care task."""
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    title: str = "Task"
    duration_minutes: int = 10
    priority: Priority = Priority.MEDIUM
    earliest_start: Optional[time] = None
    latest_end: Optional[time] = None
    recurrence_rule: Optional[str] = None  # e.g., "daily", "weekly"
    location: Optional[str] = None
    notes: Optional[str] = None
    required_pet_id: Optional[uuid.UUID] = None
    
    def is_recurring(self) -> bool:
        """Check if task is recurring."""
        pass
    
    def next_occurrence(self, after_date: date) -> Optional[date]:
        """Get next occurrence date for recurring tasks."""
        pass
    
    def conflicts_with(self, other_task: Task) -> bool:
        """Check if this task conflicts with another task."""
        pass
    
    def validate(self) -> bool:
        """Validate task constraints."""
        pass
    
    def to_dict(self) -> Dict:
        """Serialize task to dictionary."""
        pass


@dataclass
class ScheduledSlot:
    """A scheduled occurrence of a task at a specific time."""
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    task_id: uuid.UUID = None
    title: str = ""
    start_datetime: datetime = None
    end_datetime: datetime = None
    status: str = "scheduled"  # "scheduled", "completed", "skipped"
    reason: Optional[str] = None
    
    def duration_minutes(self) -> int:
        """Get duration in minutes."""
        pass
    
    def mark_completed(self, actor: str = "owner") -> None:
        """Mark slot as completed."""
        pass
    
    def reschedule(self, new_start: datetime) -> None:
        """Reschedule to a new start time."""
        pass
    
    def explain(self) -> str:
        """Get explanation for scheduling decision."""
        pass
    
    def to_dict(self) -> Dict:
        """Serialize scheduled slot to dictionary."""
        pass


@dataclass
class Schedule:
    """A daily schedule containing scheduled task slots."""
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    date: date = None
    owner_id: uuid.UUID = None
    pet_id: Optional[uuid.UUID] = None
    slots: List[ScheduledSlot] = field(default_factory=list)
    total_minutes_scheduled: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    generated_by: Optional[str] = None
    
    def add_slot(self, slot: ScheduledSlot) -> None:
        """Add a scheduled slot to the schedule."""
        pass
    
    def remove_slot(self, slot_id: uuid.UUID) -> None:
        """Remove a scheduled slot from the schedule."""
        pass
    
    def get_free_windows(self) -> List[tuple[datetime, datetime]]:
        """Get available time windows in the schedule."""
        pass
    
    def to_human_readable(self) -> str:
        """Format schedule as human-readable text."""
        pass
    
    def export_calendar(self) -> str:
        """Export schedule in calendar format (e.g., iCal)."""
        pass
    
    def to_dict(self) -> Dict:
        """Serialize schedule to dictionary."""
        pass


class Scheduler:
    """Core scheduling engine that generates daily plans."""
    
    def __init__(self, max_daily_minutes: Optional[int] = None, heuristic_settings: Optional[Dict] = None):
        """Initialize scheduler with optional constraints and settings."""
        self.max_daily_minutes = max_daily_minutes
        self.heuristic_settings = heuristic_settings or {}
    
    def generate_schedule(self, target_date: date, tasks: List[Task], owner: Owner, pet: Pet) -> Schedule:
        """Generate a daily schedule based on tasks, owner availability, and pet needs."""
        pass
    
    def score_task_for_slot(self, task: Task, start_time: datetime, context: Dict) -> float:
        """Score how well a task fits in a given time slot (0.0 to 1.0)."""
        pass
    
    def resolve_conflicts(self, schedule: Schedule) -> Schedule:
        """Resolve any scheduling conflicts in the schedule."""
        pass
    
    def explain_decision(self, slot: ScheduledSlot) -> str:
        """Provide explanation for why a task was scheduled at a particular time."""
        pass
    
    def persist_plan(self, schedule: Schedule) -> Dict:
        """Persist schedule to storage (placeholder for actual persistence)."""
        pass
