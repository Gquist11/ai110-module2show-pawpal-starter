import streamlit as st
from datetime import date, time
from pawpal_system import Priority, TimeWindow, Task, Pet, Owner, Scheduler

# ============================================================
# Step 1 — Import
# All classes come from pawpal_system.py (line above).
# ============================================================

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")
st.title("🐾 PawPal+")
st.caption("Pet care planning assistant")

# ============================================================
# Step 2 — Session State "vault"
#
# Streamlit reruns the whole script on every click.
# We check whether an Owner already exists in the vault
# before creating one — so the Owner (and its pets/tasks)
# survives every rerun without being wiped.
# ============================================================
if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name="Jordan",
        availability_windows=[TimeWindow(time(7, 0), time(21, 0))],
    )
if "schedule" not in st.session_state:
    st.session_state.schedule = None

# Shortcut so we don't type st.session_state.owner everywhere
owner: Owner = st.session_state.owner

# ============================================================
# Sidebar — owner settings + Add Pet form
# ============================================================
with st.sidebar:
    st.header("⚙️ Owner Settings")

    new_name = st.text_input("Owner name", value=owner.name)
    if new_name.strip() and new_name.strip() != owner.name:
        owner.name = new_name.strip()

    st.subheader("Availability")
    c1, c2 = st.columns(2)
    with c1:
        avail_start = st.time_input("From", value=owner.availability_windows[0].start)
    with c2:
        avail_end = st.time_input("To", value=owner.availability_windows[0].end)

    # Update the window live if the user changes the times
    if (avail_start != owner.availability_windows[0].start
            or avail_end != owner.availability_windows[0].end):
        owner.availability_windows = [TimeWindow(avail_start, avail_end)]

    st.divider()

    # --------------------------------------------------------
    # Step 3 — Add Pet form wired to owner.add_pet()
    #
    # When the user submits this form:
    #   1. We create a new Pet object from the form values.
    #   2. We call owner.add_pet(new_pet) — the Owner class
    #      method that registers the pet inside the Owner.
    #   3. Because owner lives in session_state, the pet
    #      is saved for every future rerun.
    # --------------------------------------------------------
    st.subheader("➕ Add a Pet")
    with st.form("add_pet_form", clear_on_submit=True):
        pet_name    = st.text_input("Pet name",    placeholder="e.g. Mochi")
        pet_species = st.selectbox("Species",      ["dog", "cat", "other"])
        pet_breed   = st.text_input("Breed",       placeholder="e.g. Shiba Inu")
        pet_age     = st.number_input("Age (yrs)", min_value=0.0, step=0.5, value=1.0)
        if st.form_submit_button("Add Pet") and pet_name.strip():
            new_pet = Pet(
                name=pet_name.strip(),
                species=pet_species,
                breed=pet_breed,
                age_years=pet_age,
            )
            owner.add_pet(new_pet)   # <-- class method called here
            st.success(f"Added {new_pet.name}!")
            st.rerun()

# ============================================================
# Main — pet cards + Add Task forms
# ============================================================
pets = owner.get_pets()

if not pets:
    st.info("No pets yet. Use the sidebar to add your first pet.")
    st.stop()

st.subheader("🐾 Pets & Tasks")

for pet in pets:
    label = f"{pet.name}  ({pet.species}" \
            + (f", {pet.breed}" if pet.breed else "") \
            + f", {pet.age_years:.0f} yrs)  — {len(pet.get_tasks())} task(s)"

    with st.expander(label, expanded=True):

        # Show tasks already on this pet
        if pet.get_tasks():
            for task in pet.get_tasks():
                icon = "✅" if task.completed else "○"
                rec  = f" · _{task.recurrence}_" if task.recurrence else ""
                st.markdown(
                    f"{icon} **{task.title}** · {task.priority.value} · "
                    f"{task.duration_minutes} min{rec}"
                )
        else:
            st.caption("No tasks yet — add one below.")

        # ----------------------------------------------------
        # Step 3 — Add Task form wired to pet.add_task()
        #
        # When the user submits this form:
        #   1. We create a Task from the form values.
        #   2. We call pet.add_task(new_task) — the Pet class
        #      method that attaches the task and sets its
        #      required_pet_id automatically.
        #   3. Because the pet lives inside the owner which
        #      lives in session_state, the task is saved.
        # ----------------------------------------------------
        with st.form(f"add_task_{pet.id}", clear_on_submit=True):
            st.markdown(f"**Add a task for {pet.name}**")
            fc1, fc2 = st.columns(2)
            with fc1:
                t_title    = st.text_input("Title",       placeholder="e.g. Morning walk",   key=f"tt_{pet.id}")
                t_desc     = st.text_input("Description", placeholder="e.g. Leash walk",     key=f"td_{pet.id}")
                t_priority = st.selectbox("Priority", ["high", "medium", "low"],             key=f"tpri_{pet.id}")
            with fc2:
                t_duration   = st.number_input("Duration (min)", min_value=1, value=15,      key=f"tdur_{pet.id}")
                t_recurrence = st.text_input("Recurrence",  placeholder="e.g. daily",        key=f"trec_{pet.id}")

            if st.form_submit_button(f"Add task to {pet.name}") and t_title.strip():
                new_task = Task(
                    title=t_title.strip(),
                    description=t_desc,
                    duration_minutes=int(t_duration),
                    priority=t_priority,
                    recurrence=t_recurrence.strip() or None,
                )
                pet.add_task(new_task)   # <-- class method called here
                st.success(f"Added '{new_task.title}' to {pet.name}!")
                st.rerun()

# ============================================================
# Build & display the schedule
# ============================================================
st.divider()
st.subheader("📅 Build Schedule")

pending = owner.all_pending_tasks()
if not pending:
    st.warning("No pending tasks yet. Add tasks to your pets above.")
else:
    dc1, dc2 = st.columns([3, 1])
    with dc1:
        target_date = st.date_input("Schedule for", value=date.today())
    with dc2:
        st.metric("Pending tasks", len(pending))

    if st.button("Generate schedule", type="primary"):
        # owner already holds all pets and their tasks — pass it straight in
        schedule = Scheduler().generate_daily_plan(owner, target_date)
        st.session_state.schedule = schedule  # save to vault

# ---- Results ----
if st.session_state.schedule:
    sched = st.session_state.schedule

    st.success(
        f"Scheduled {len(sched.slots)} tasks — "
        f"{sched.total_minutes_scheduled} minutes total"
    )

    if sched.slots:
        st.markdown("### Today's Plan")
        for slot in sched.slots:
            start     = slot.start.strftime("%I:%M %p") if slot.start else "?"
            end       = slot.end.strftime("%I:%M %p")   if slot.end   else "?"
            pet       = owner.get_pet(slot.pet_id)
            pet_label = f" · {pet.name}" if pet else ""
            icon      = "✅" if slot.status == "completed" else "🕐"
            st.markdown(
                f"{icon} **{start} – {end}** &nbsp; {slot.title}{pet_label}  \n"
                f"<small style='color:gray'>{slot.reason}</small>",
                unsafe_allow_html=True,
            )

    if sched.skipped_tasks:
        st.markdown("### ⚠️ Could not fit")
        for t in sched.skipped_tasks:
            st.warning(f"{t.title} — outside your availability window")

    with st.expander("Owner summary"):
        st.text(Scheduler().summary(owner))

    with st.expander("Export as JSON"):
        st.code(sched.persist(), language="json")
