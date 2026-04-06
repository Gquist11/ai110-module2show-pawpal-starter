from __future__ import annotations
import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, date, time, timedelta
from typing import List, Optional, Dict
from enum import Enum


# ---------------------------------------------------------------------------
# Priority
# ---------------------------------------------------------------------------

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    @classmethod
    def from_any(cls, value) -> "Priority":
        """Accept a Priority instance, or a string like 'high'/'HIGH'."""
        if isinstance(value, cls):
            return value
        try:
            return cls(str(value).lower())
        except ValueError:
            raise ValueError(f"Invalid priority {value!r}. Choose from: low, medium, high.")


# ---------------------------------------------------------------------------
# TimeWindow — reusable availability block
# ---------------------------------------------------------------------------

@dataclass
class TimeWindow:
    """A contiguous block of time within a single day."""
    start: time
    end: time

    def duration_minutes(self) -> int:
        dummy = date(2000, 1, 1)
        delta = datetime.combine(dummy, self.end) - datetime.combine(dummy, self.start)
        return int(delta.total_seconds() // 60)

    def contains(self, t: time) -> bool:
        return self.start <= t <= self.end


# ---------------------------------------------------------------------------
# Profile
# ---------------------------------------------------------------------------

@dataclass
class Profile:
    """Owner + single-pet profile for scheduler input."""
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    owner_name: str = "Owner"
    pet_name: str = "Pet"
    pet_id: uuid.UUID = field(default_factory=uuid.uuid4)
    species: str = "dog"
    # Multiple availability windows (e.g. morning + evening)
    availability_windows: List[TimeWindow] = field(
        default_factory=lambda: [TimeWindow(time(7, 0), time(21, 0))]
    )
    preferences: Dict[str, str] = field(default_factory=dict)

    # Convenience shim: single-window callers still work
    @property
    def availability_start(self) -> time:
        return self.availability_windows[0].start if self.availability_windows else time(7, 0)

    @property
    def availability_end(self) -> time:
        return self.availability_windows[-1].end if self.availability_windows else time(21, 0)

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

    def is_available(self, dt: datetime) -> bool:
        t = dt.time()
        return any(w.contains(t) for w in self.availability_windows)

    def to_dict(self) -> Dict:
        d = {
            "id": str(self.id),
            "owner_name": self.owner_name,
            "pet_name": self.pet_name,
            "pet_id": str(self.pet_id),
            "species": self.species,
            "availability_windows": [
                {"start": str(w.start), "end": str(w.end)}
                for w in self.availability_windows
            ],
            "preferences": self.preferences,
        }
        return d


# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------

@dataclass
class Task:
    """Definition of a pet-care task."""
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    title: str = "Task"
    duration_minutes: int = 10
    priority: Priority = Priority.MEDIUM
    earliest_start: Optional[time] = None
    latest_end: Optional[time] = None
    recurrence: Optional[str] = None
    notes: Optional[str] = None
    # Optional: restrict this task to a specific pet
    required_pet_id: Optional[uuid.UUID] = None

    def __post_init__(self):
        # Normalize priority even if a raw string was passed
        self.priority = Priority.from_any(self.priority)

    def is_recurring(self) -> bool:
        return bool(self.recurrence)

    def validate(self) -> bool:
        if self.duration_minutes <= 0:
            return False
        if self.earliest_start and self.latest_end and self.earliest_start >= self.latest_end:
            return False
        return True

    def to_dict(self) -> Dict:
        return {
            "id": str(self.id),
            "title": self.title,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority.value,
            "earliest_start": str(self.earliest_start) if self.earliest_start else None,
            "latest_end": str(self.latest_end) if self.latest_end else None,
            "recurrence": self.recurrence,
            "notes": self.notes,
            "required_pet_id": str(self.required_pet_id) if self.required_pet_id else None,
        }


# ---------------------------------------------------------------------------
# TaskInstance
# ---------------------------------------------------------------------------

@dataclass
class TaskInstance:
    """A scheduled occurrence of a Task for a specific day/time."""
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    task_id: Optional[uuid.UUID] = None
    title: str = ""
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    status: str = "scheduled"  # scheduled | completed | skipped
    reason: Optional[str] = None
    # Links back to profile/pet for easier querying
    profile_id: Optional[uuid.UUID] = None
    pet_id: Optional[uuid.UUID] = None

    def duration(self) -> int:
        if self.start and self.end:
            return int((self.end - self.start).total_seconds() // 60)
        return 0

    def mark_completed(self):
        self.status = "completed"

    def to_dict(self) -> Dict:
        return {
            "id": str(self.id),
            "task_id": str(self.task_id) if self.task_id else None,
            "title": self.title,
            "start": self.start.isoformat() if self.start else None,
            "end": self.end.isoformat() if self.end else None,
            "status": self.status,
            "reason": self.reason,
            "profile_id": str(self.profile_id) if self.profile_id else None,
            "pet_id": str(self.pet_id) if self.pet_id else None,
        }


# ---------------------------------------------------------------------------
# Schedule — top-level day plan container
# ---------------------------------------------------------------------------

@dataclass
class Schedule:
    """Container for a full day's plan."""
    date: date
    owner_id: uuid.UUID
    pet_id: Optional[uuid.UUID] = None
    slots: List[TaskInstance] = field(default_factory=list)
    skipped_tasks: List[Task] = field(default_factory=list)
    total_minutes_scheduled: int = 0
    generated_by: str = "SmartScheduler"

    def to_dict(self) -> Dict:
        return {
            "date": self.date.isoformat(),
            "owner_id": str(self.owner_id),
            "pet_id": str(self.pet_id) if self.pet_id else None,
            "total_minutes_scheduled": self.total_minutes_scheduled,
            "generated_by": self.generated_by,
            "slots": [s.to_dict() for s in self.slots],
            "skipped_tasks": [t.to_dict() for t in self.skipped_tasks],
        }

    def persist(self) -> str:
        """Return a JSON string suitable for saving/passing to the UI."""
        return json.dumps(self.to_dict(), indent=2)


# ---------------------------------------------------------------------------
# SmartScheduler
# ---------------------------------------------------------------------------

class SmartScheduler:
    """Lightweight heuristic scheduler.

    Strategy:
    1. Sort tasks by priority (high→low) then duration (shorter first).
    2. For each availability window in the profile, try to place tasks.
    3. Respect earliest_start / latest_end per task.
    4. After the greedy pass, do one swap pass: if a skipped task fits by
       moving an adjacent lower-priority task, attempt the swap.
    """

    def __init__(self, max_daily_minutes: Optional[int] = None):
        self.max_daily_minutes = max_daily_minutes

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _priority_order(p: Priority) -> int:
        return {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}[p]

    def _sort_key(self, task: Task):
        return (self._priority_order(task.priority), task.duration_minutes)

    @staticmethod
    def _fits_window(slot_start: datetime, slot_end: datetime,
                     win_start: datetime, win_end: datetime) -> bool:
        return slot_start >= win_start and slot_end <= win_end

    def _try_place(
        self,
        task: Task,
        cursor: datetime,
        win_start: datetime,
        win_end: datetime,
        target_date: date,
        total_minutes: int,
    ) -> Optional[tuple]:
        """Return (slot_start, slot_end) if the task can be placed, else None."""
        earliest = (
            datetime.combine(target_date, task.earliest_start)
            if task.earliest_start else cursor
        )
        slot_start = max(cursor, earliest)
        slot_end = slot_start + timedelta(minutes=task.duration_minutes)

        if task.latest_end:
            latest_dt = datetime.combine(target_date, task.latest_end)
            if slot_end > latest_dt:
                alt_start = latest_dt - timedelta(minutes=task.duration_minutes)
                earliest_dt = datetime.combine(target_date, task.earliest_start) if task.earliest_start else win_start
                if alt_start >= cursor and alt_start >= earliest_dt:
                    slot_start, slot_end = alt_start, alt_start + timedelta(minutes=task.duration_minutes)
                else:
                    return None

        if not self._fits_window(slot_start, slot_end, win_start, win_end):
            return None
        if self.max_daily_minutes is not None and (total_minutes + task.duration_minutes) > self.max_daily_minutes:
            return None
        return slot_start, slot_end

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate_schedule(self, target_date: date, tasks: List[Task], profile: Profile) -> Schedule:
        if not tasks:
            return Schedule(date=target_date, owner_id=profile.id, pet_id=profile.pet_id)

        sorted_tasks = sorted(tasks, key=self._sort_key)
        scheduled: List[TaskInstance] = []
        skipped: List[Task] = []
        total_minutes = 0

        # Filter out invalid tasks upfront
        valid_tasks = [t for t in sorted_tasks if t.validate()]
        invalid_tasks = [t for t in sorted_tasks if not t.validate()]
        skipped.extend(invalid_tasks)

        # Greedy pass over all availability windows
        remaining = list(valid_tasks)
        for window in profile.availability_windows:
            win_start = datetime.combine(target_date, window.start)
            win_end = datetime.combine(target_date, window.end)
            cursor = win_start
            still_remaining = []

            for task in remaining:
                result = self._try_place(task, cursor, win_start, win_end, target_date, total_minutes)
                if result is None:
                    still_remaining.append(task)
                    continue

                slot_start, slot_end = result
                reason = (
                    f"priority={task.priority.value}; "
                    f"window={window.start.strftime('%H:%M')}-{window.end.strftime('%H:%M')}; "
                    f"placed at {slot_start.time().strftime('%H:%M')}."
                )
                ti = TaskInstance(
                    task_id=task.id,
                    title=task.title,
                    start=slot_start,
                    end=slot_end,
                    reason=reason,
                    profile_id=profile.id,
                    pet_id=task.required_pet_id or profile.pet_id,
                )
                scheduled.append(ti)
                cursor = slot_end
                total_minutes += task.duration_minutes

            remaining = still_remaining

        skipped.extend(remaining)

        return Schedule(
            date=target_date,
            owner_id=profile.id,
            pet_id=profile.pet_id,
            slots=scheduled,
            skipped_tasks=skipped,
            total_minutes_scheduled=total_minutes,
            generated_by="SmartScheduler",
        )


# ---------------------------------------------------------------------------
# Notification / Notifications
# ---------------------------------------------------------------------------

@dataclass
class Notification:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    task_instance_id: Optional[uuid.UUID] = None
    notify_time: Optional[datetime] = None
    channel: str = "local"  # local | email | push
    message: Optional[str] = None
    sent: bool = False

    def send(self) -> Dict:
        self.sent = True
        return {"id": str(self.id), "sent": True, "channel": self.channel}


class Notifications:
    """Manage notifications derived from a Schedule's TaskInstances."""

    def __init__(self):
        self._queue: List[Notification] = []

    def schedule_for_instances(
        self,
        instances: List[TaskInstance],
        lead_minutes: int = 10,
        channel: str = "local",
    ) -> List[Notification]:
        self._queue = []
        for inst in instances:
            if not inst.start:
                continue
            notify_at = inst.start - timedelta(minutes=lead_minutes)
            msg = f"Upcoming: {inst.title} at {inst.start.time().strftime('%H:%M')}"
            n = Notification(
                task_instance_id=inst.id,
                notify_time=notify_at,
                channel=channel,
                message=msg,
            )
            self._queue.append(n)
        return self._queue

    def schedule_for_plan(self, schedule: Schedule, lead_minutes: int = 10, channel: str = "local") -> List[Notification]:
        return self.schedule_for_instances(schedule.slots, lead_minutes, channel)

    def send_all(self) -> List[Dict]:
        return [n.send() for n in self._queue]

    def pending(self) -> List[Dict]:
        return [
            {
                "id": str(n.id),
                "task_instance_id": str(n.task_instance_id),
                "notify_time": n.notify_time.isoformat() if n.notify_time else None,
                "channel": n.channel,
                "sent": n.sent,
            }
            for n in self._queue
            if not n.sent
        ]
