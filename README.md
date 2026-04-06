# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

Beyond basic priority-first placement, the scheduler now includes four algorithmic improvements:

**Sort by time** — `Scheduler.sort_by_time(tasks)` orders any list of tasks by their `earliest_start` wall-clock time using a lambda key, with tasks that have no start constraint placed last.

**Filter by pet or status** — `Scheduler.filter_tasks(owner, pet_name, completed)` lets you pull a focused slice of tasks, e.g. only Luna's pending items or every completed task across all pets.

**Recurring task auto-spawn** — When a `daily` or `weekly` task is marked complete, `Task.complete(today)` calculates the `next_due` date using Python's `timedelta`, and `Pet.complete_task()` automatically adds a fresh copy of the task to the pet's list so it appears in tomorrow's plan.

**Conflict detection** — `Scheduler.detect_conflicts(schedule)` scans every pair of scheduled slots and reports any time overlaps as plain-English warning strings instead of crashing, so the user is informed without the app breaking.

---

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
