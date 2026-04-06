# 🐾 PawPal+

**PawPal+** is a Streamlit app that helps a busy pet owner stay consistent with daily pet care. It lets you add pets and tasks, then automatically builds a prioritized daily schedule that fits inside your available hours.

---

## 📸 Demo

<a href="/course_images/ai110/pawpal_screenshot.png" target="_blank">
  <img src="/course_images/ai110/pawpal_screenshot.png" title="PawPal App" width="" alt="PawPal App" class="center-block" />
</a>

---

## ✨ Features

### Core scheduling
- **Owner & pet profiles** — Set your name, multiple pets (name, species, breed, age), and your free hours for the day
- **Task library** — Add tasks with a title, description, duration, priority (high / medium / low), optional earliest start time, and recurrence
- **Priority-first scheduling** — The scheduler places high-priority tasks first, then medium, then low, fitting each into your availability window automatically
- **Multi-window availability** — You can be free 7–9 AM *and* 5–8 PM; the scheduler tries both windows so tasks aren't dropped unnecessarily
- **Scheduling reasoning** — Every slot explains why it was placed at that time (priority + window + placement time)

### Smarter scheduling (Phase 3)
- **Sort by time** — `Scheduler.sort_by_time()` orders any task list chronologically using earliest start time as the sort key; tasks with no start constraint fall to the end
- **Filter by pet or status** — `Scheduler.filter_tasks()` returns a focused slice of tasks filtered by pet name and/or completion status (pending / done / all)
- **Daily & weekly recurrence** — When a recurring task is marked complete, `Task.complete(today)` calculates the next due date using `timedelta`, and a fresh copy of the task is automatically added for tomorrow (or next week)
- **Conflict detection** — `Scheduler.detect_conflicts()` scans every pair of scheduled slots for time overlaps and surfaces plain-English warnings in the UI so the owner is informed without the app crashing

### UI
- Three-tab layout: **Pets & Tasks** / **Sort & Filter** / **Schedule**
- Sortable task table in the Sort & Filter tab
- Conflict warnings shown as `st.error` + `st.warning` banners
- Skipped tasks shown with an explanation and a suggestion to fix them
- JSON export of the full schedule

---

## 🗂 Project structure

```
pawpal_system.py   # All classes: Task, Pet, Owner, Scheduler, Schedule, ...
app.py             # Streamlit UI
main.py            # Terminal demo script
tests/
  test_pawpal.py   # 12 automated pytest tests
uml_final.md       # Final Mermaid.js class diagram
reflection.md      # Design decisions and AI collaboration notes
requirements.txt
```

---

## 🚀 Getting started

```bash
pip install -r requirements.txt
streamlit run app.py        # launch the UI
python main.py              # run the terminal demo
python -m pytest            # run all 12 tests
```

---

## 🧪 Test coverage

| Area | Tests |
|---|---|
| Task completion | happy path + non-recurring no-spawn |
| Pet task count | add increases count |
| Sorting | chronological order, no-start goes last |
| Recurrence | daily +1 day, weekly +7 days, one-off no clone |
| Conflict detection | overlap flagged, sequential slots clear |
| Edge cases | empty pet, filter by name, filter by status |

---

## Smarter Scheduling (detail)

Beyond basic priority-first placement, the scheduler includes four algorithmic improvements:

**Sort by time** — `Scheduler.sort_by_time(tasks)` orders any list of tasks by their `earliest_start` wall-clock time using a lambda key, with tasks that have no start constraint placed last.

**Filter by pet or status** — `Scheduler.filter_tasks(owner, pet_name, completed)` lets you pull a focused slice of tasks, e.g. only Luna's pending items or every completed task across all pets.

**Recurring task auto-spawn** — When a `daily` or `weekly` task is marked complete, `Task.complete(today)` calculates the `next_due` date using Python's `timedelta`, and `Pet.complete_task()` automatically adds a fresh copy of the task to the pet's list so it appears in tomorrow's plan.

**Conflict detection** — `Scheduler.detect_conflicts(schedule)` scans every pair of scheduled slots and reports any time overlaps as plain-English warning strings instead of crashing, so the user is informed without the app breaking.
