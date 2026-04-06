import streamlit as st
from datetime import date, time
from pawpal_system import Priority, TimeWindow, Task, Pet, Owner, Scheduler, Notifications

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Pet care planning assistant")

# ---------------------------------------------------------------------------
# Session state bootstrap
# ---------------------------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = None
if "schedule" not in st.session_state:
    st.session_state.schedule = None

# ---------------------------------------------------------------------------
# Sidebar — owner + pet setup
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Owner & Pet Setup")
    owner_name = st.text_input("Owner name", value="Jordan")

    st.subheader("Availability")
    col1, col2 = st.columns(2)
    with col1:
        avail_start = st.time_input("From", value=time(7, 0))
    with col2:
        avail_end = st.time_input("To", value=time(21, 0))

    st.subheader("Pets")
    if "pets_config" not in st.session_state:
        st.session_state.pets_config = [{"name": "Mochi", "species": "dog", "breed": "Shiba", "age": 3.0}]

    for i, pc in enumerate(st.session_state.pets_config):
        with st.expander(f"Pet {i+1}: {pc['name']}", expanded=(i == 0)):
            pc["name"]    = st.text_input("Name",    value=pc["name"],    key=f"pname_{i}")
            pc["species"] = st.selectbox("Species", ["dog","cat","other"], key=f"pspec_{i}",
                                         index=["dog","cat","other"].index(pc["species"]))
            pc["breed"]   = st.text_input("Breed",   value=pc["breed"],   key=f"pbreed_{i}")
            pc["age"]     = st.number_input("Age (years)", value=pc["age"], min_value=0.0, step=0.5, key=f"page_{i}")

    if st.button("+ Add pet"):
        st.session_state.pets_config.append({"name": "New pet", "species": "dog", "breed": "", "age": 0.0})
        st.rerun()

# ---------------------------------------------------------------------------
# Main — task builder
# ---------------------------------------------------------------------------
st.subheader("Tasks")

if "tasks_config" not in st.session_state:
    st.session_state.tasks_config = [
        {"title": "Morning walk",  "desc": "Leash walk around the block", "pet_idx": 0, "duration": 30, "priority": "high",   "recurrence": "daily", "earliest": None, "latest": None},
        {"title": "Feeding",       "desc": "Half cup dry food",           "pet_idx": 0, "duration": 10, "priority": "high",   "recurrence": "daily", "earliest": None, "latest": None},
        {"title": "Vet meds",      "desc": "Heartworm pill",              "pet_idx": 0, "duration":  5, "priority": "medium", "recurrence": "daily", "earliest": None, "latest": time(9, 0)},
        {"title": "Grooming",      "desc": "Brush coat",                  "pet_idx": 0, "duration": 20, "priority": "low",    "recurrence": "",      "earliest": None, "latest": None},
    ]

pet_names = [pc["name"] for pc in st.session_state.pets_config]

for i, tc in enumerate(st.session_state.tasks_config):
    with st.expander(f"{tc['title']} [{tc['priority']}]", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            tc["title"]    = st.text_input("Title",       value=tc["title"],    key=f"ttitle_{i}")
            tc["desc"]     = st.text_input("Description", value=tc["desc"],     key=f"tdesc_{i}")
            tc["priority"] = st.selectbox("Priority", ["high","medium","low"],  key=f"tpri_{i}",
                                          index=["high","medium","low"].index(tc["priority"]))
        with c2:
            tc["duration"]   = st.number_input("Duration (min)", value=tc["duration"], min_value=1, key=f"tdur_{i}")
            tc["recurrence"] = st.text_input("Recurrence (e.g. daily)", value=tc.get("recurrence",""), key=f"trec_{i}")
            pet_idx = tc.get("pet_idx", 0)
            tc["pet_idx"]    = st.selectbox("Assign to pet", range(len(pet_names)),
                                            format_func=lambda x: pet_names[x],
                                            index=min(pet_idx, len(pet_names)-1),
                                            key=f"tpet_{i}")

if st.button("+ Add task"):
    st.session_state.tasks_config.append({
        "title": "New task", "desc": "", "pet_idx": 0,
        "duration": 10, "priority": "medium", "recurrence": "", "earliest": None, "latest": None,
    })
    st.rerun()

# ---------------------------------------------------------------------------
# Generate schedule
# ---------------------------------------------------------------------------
st.divider()
st.subheader("Build Schedule")
target_date = st.date_input("Schedule for", value=date.today())

if st.button("Generate schedule", type="primary"):
    # Build Owner
    owner = Owner(owner_name, availability_windows=[TimeWindow(avail_start, avail_end)])

    # Build Pets
    pets = []
    for pc in st.session_state.pets_config:
        pets.append(Pet(pc["name"], pc["species"], pc["breed"], pc["age"]))
        owner.add_pet(pets[-1])

    # Attach Tasks to correct pet
    for tc in st.session_state.tasks_config:
        pidx = tc.get("pet_idx", 0)
        if pidx >= len(pets):
            pidx = 0
        task = Task(
            title=tc["title"],
            description=tc["desc"],
            duration_minutes=int(tc["duration"]),
            priority=tc["priority"],
            recurrence=tc["recurrence"] or None,
            earliest_start=tc.get("earliest"),
            latest_end=tc.get("latest"),
        )
        pets[pidx].add_task(task)

    # Run scheduler
    scheduler = Scheduler()
    schedule  = scheduler.generate_daily_plan(owner, target_date)

    st.session_state.owner    = owner
    st.session_state.schedule = schedule

# ---------------------------------------------------------------------------
# Display schedule
# ---------------------------------------------------------------------------
if st.session_state.schedule:
    schedule = st.session_state.schedule
    owner    = st.session_state.owner

    st.success(f"Scheduled {len(schedule.slots)} tasks — {schedule.total_minutes_scheduled} minutes total")

    # Scheduled slots
    if schedule.slots:
        st.markdown("### Today's Plan")
        for slot in schedule.slots:
            start = slot.start.strftime("%H:%M") if slot.start else "?"
            end   = slot.end.strftime("%H:%M")   if slot.end   else "?"
            pet   = owner.get_pet(slot.pet_id)
            pet_label = f" · {pet.name}" if pet else ""
            icon  = "✅" if slot.status == "completed" else "🕐"
            st.markdown(f"{icon} **{start}–{end}** &nbsp; {slot.title}{pet_label}  \n<small>{slot.reason}</small>", unsafe_allow_html=True)

    # Skipped tasks
    if schedule.skipped_tasks:
        st.markdown("### Skipped Tasks")
        for t in schedule.skipped_tasks:
            st.warning(f"⚠️ {t.title} — couldn't fit in the availability window")

    # Owner summary
    with st.expander("Owner summary"):
        scheduler = Scheduler()
        st.text(scheduler.summary(owner))

    # JSON export
    with st.expander("Export as JSON"):
        st.code(schedule.persist(), language="json")
