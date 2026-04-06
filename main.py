from datetime import date, time
from pawpal_system import Priority, TimeWindow, Task, Pet, Owner, Scheduler

# ---------------------------------------------------------------------------
# 1. Create Owner with availability windows
# ---------------------------------------------------------------------------
owner = Owner(
    name="Jordan",
    availability_windows=[
        TimeWindow(time(7, 0), time(9, 30)),   # morning block
        TimeWindow(time(17, 0), time(20, 0)),  # evening block
    ],
)

# ---------------------------------------------------------------------------
# 2. Create two Pets
# ---------------------------------------------------------------------------
mochi = Pet(name="Mochi", species="dog", breed="Shiba Inu", age_years=3.0)
luna  = Pet(name="Luna",  species="cat", breed="Tabby",     age_years=5.0)

owner.add_pet(mochi)
owner.add_pet(luna)

# ---------------------------------------------------------------------------
# 3. Add Tasks with different times / priorities
# ---------------------------------------------------------------------------

# --- Mochi's tasks ---
mochi.add_task(Task(
    title="Morning walk",
    description="Leash walk around the neighborhood",
    duration_minutes=30,
    priority="high",
    recurrence="daily",
    earliest_start=time(7, 0),
))

mochi.add_task(Task(
    title="Breakfast feeding",
    description="Half cup of dry kibble",
    duration_minutes=10,
    priority="high",
    recurrence="daily",
))

mochi.add_task(Task(
    title="Heartworm pill",
    description="Hide pill in peanut butter",
    duration_minutes=5,
    priority="medium",
    recurrence="daily",
    latest_end=time(9, 0),
))

# --- Luna's tasks ---
luna.add_task(Task(
    title="Evening feeding",
    description="One pouch of wet food",
    duration_minutes=10,
    priority="high",
    recurrence="daily",
    earliest_start=time(17, 0),
))

luna.add_task(Task(
    title="Litter box cleaning",
    description="Scoop and add fresh litter",
    duration_minutes=10,
    priority="medium",
    recurrence="daily",
))

luna.add_task(Task(
    title="Playtime",
    description="Wand toy session",
    duration_minutes=15,
    priority="low",
    earliest_start=time(17, 30),
))

# ---------------------------------------------------------------------------
# 4. Run the Scheduler and print Today's Schedule
# ---------------------------------------------------------------------------
scheduler = Scheduler()
schedule  = scheduler.generate_daily_plan(owner, date.today())

print("=" * 50)
print(f"  TODAY'S SCHEDULE — {schedule.date}")
print(f"  Owner: {owner.name}  |  Pets: {', '.join(p.name for p in owner.get_pets())}")
print("=" * 50)

if schedule.slots:
    for slot in schedule.slots:
        start = slot.start.strftime("%I:%M %p")
        end   = slot.end.strftime("%I:%M %p")
        pet   = owner.get_pet(slot.pet_id)
        pet_label = pet.name if pet else "?"
        print(f"  {start} – {end}  |  {slot.title:<22}  ({pet_label})")
        print(f"    → {slot.reason}")
else:
    print("  No tasks could be scheduled.")

if schedule.skipped_tasks:
    print()
    print("  SKIPPED:")
    for t in schedule.skipped_tasks:
        print(f"  ✗ {t.title}")

print("=" * 50)
print(f"  Total: {len(schedule.slots)} tasks, {schedule.total_minutes_scheduled} minutes")
print("=" * 50)

print()
print(scheduler.summary(owner))
