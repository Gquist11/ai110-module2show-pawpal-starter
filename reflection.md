# PawPal+ Project Reflection

## 1. System Design
a. The profile: It will store who the owner is and info about their pet. This data will feed everything else. 

b. Task: A list of pet-care to do's like walking, feeding and so on with details like how long each takes, how urgent it is, and whether it repeats. It will be like a reuseable task library. 

c. Smart Scheduler: Takes the tasks and the profile data and builds a daily plan automatically. It will also expalins why it scheduled things when it did. 

d. Notifications and task completion
**a. Initial design**

- Briefly describe your initial UML design.

* The app has a small set of pieces that work together: 
the owner and pet data feed into a scheduler that turns task into a daily plan. The scheduler also makes short explanations for why it put a task at a certain time, and a notifications part can remind the owner.

- What classes did you include, and what responsibilities did you assign to each?
* Owner/Profile: Has the owners name, contact and daily availability. Tells the scheduler when the owner is free. 
* Pet: It has the pet's information, and tells the scheduler the pet-specific needs. 
* Task: Describes a job as in title, how long it takes, priority, and simple timing limits. Knows if it's valid and when it should repeat. 
* Scheduled Slot: One scheduled occurrence of a task with start/end time, status, and a short reason why it was placed there. A day's list of the scheduler and totals which show's the free time and produce readable output. 
* Smart Scheduler: Takes task + profile + pet and produces a schedule using rules, resolves basic conflicts and provides short explanations. 
* Notifications: Creates reminders from the scheduled slots and list or send them.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, a few things changed once I started writing the actual code.

1. The scheduler now returns a full plan, not just a list.
At first the scheduler just handed back a list of time slots. But I kept needing other info too — like the date, how many minutes were scheduled, and which tasks didn't fit. So I wrapped everything into one "Schedule" object that holds all of that together in one place.

2. Owners can now have more than one free window per day.
The original design only let you set one start time and one end time for the owner's availability. That didn't work for real life — someone might be free in the morning AND the evening. I changed it so you can add as many time windows as you need, and the scheduler will try each one.

3. Each task slot now knows which pet it belongs to.
Early on, a scheduled slot had no idea which pet it was for. That made it hard to show the pet's name in the app. I added a "pet" field to each slot so it always carries that info with it.

4. Pet and Owner can do more than just hold data.
Originally Pet and Owner were just containers — they stored info but didn't do much. As I built the app, I kept needing things like "show me only the unfinished tasks" or "mark this task as done." So I gave Pet and Owner their own helpful actions instead of putting all that work on the Scheduler.

5. Priority now accepts plain words like "high" or "low".
The app's input form sends priority as a regular word. The original code only understood its own internal format and would crash on plain text. I added a small helper that converts any version of the word into the right format automatically.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers four constraints: task priority (high/medium/low), the owner's available time windows, a task's earliest allowed start time, and a task's latest allowed end time. Priority was treated as the most important because a missed high-priority task (like medication) has real consequences for the pet. Time windows came second because the whole plan is useless if it falls outside the owner's free hours. Earliest start and latest end were added third to handle real-world cases like "the vet clinic opens at 9 AM" or "the pill must be given before 9 AM." Personal preferences like pet mood or weather were left out to keep the system simple and testable.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler picks tasks in priority order and places them one at a time from the start of the available window. This is fast and simple, but it means a long high-priority task can block a short medium-priority task that needed that same early slot. The app chooses this approach because it is easy to understand and works well for a single owner with a small number of tasks each day. A more complex approach — like trying every possible ordering — would be slower and harder to explain to the user.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

AI was used at every stage of this project. In the design phase it helped brainstorm which classes were needed and what responsibilities each one should have. During implementation it wrote first drafts of methods like `sort_by_time`, `detect_conflicts`, and `spawn_next_occurrence`, which I then reviewed and adjusted. It also caught bugs — for example, it pointed out that the scheduler was returning a bare list instead of a `Schedule` object, which made the code harder to work with. For refactoring it suggested splitting the UI into tabs and using `st.table` and `st.dataframe` to make the data look cleaner.

The most helpful prompts were specific ones that described the exact behavior I wanted: "write a method that sorts tasks by earliest_start and puts None values last" worked much better than "sort my tasks." Asking it to explain generated code line by line before accepting it also helped me understand what was happening instead of just copying it.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When asked for a conflict detection strategy, the AI first suggested raising an exception when two tasks overlapped. I rejected that because crashing the app is a bad experience for a pet owner who just wants a warning. Instead I asked it to return a list of warning strings so the UI could display them without stopping. I verified the change by writing a test that manually builds two overlapping slots and checks that the method returns a non-empty list rather than throwing an error. That test is now part of the automated suite (`test_conflict_detection_flags_overlapping_slots`).

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

The test suite covers 12 behaviors across five areas. Task completion and pet task count were tested first because they are the foundation everything else builds on. Sorting correctness was tested by adding tasks out of order and checking the returned order. Recurrence was tested by completing a daily and a weekly task and verifying that a new copy appeared with the correct next-due date, and that a one-off task did not clone itself. Conflict detection was tested with two overlapping slots (should warn) and two back-to-back slots (should not warn). Edge cases covered an empty pet, filtering by pet name, and filtering by completion status. These tests matter because they catch bugs silently — if `spawn_next_occurrence` stopped working, a pet could miss medication the next day and the owner would have no idea.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am confident the core scheduling logic is correct for the cases the tests cover. The greedy priority-first algorithm consistently places tasks in the right order and respects time windows. I am less confident about edge cases I haven't tested yet. Given more time I would test: a task whose duration is longer than the entire availability window (should be skipped cleanly), two tasks that together fill the window exactly with no room for a third, what happens when `avail_start` equals `avail_end` (zero-length window), and recurring tasks that span across a timezone change.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The part I am most satisfied with is the recurring task system. Marking a daily task complete and watching a fresh copy automatically appear with tomorrow's date feels like real app behavior — not just a demo. The fact that it is covered by two tests and wired into the UI makes it feel solid rather than fragile.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would redesign the availability window system to support gaps within a window — for example, "free from 7–9 AM except 8–8:30 AM (school drop-off)." Right now the scheduler treats each window as fully open. I would also add a way for the UI to mark a slot complete directly on the schedule screen and see the next occurrence appear in real time without regenerating the whole plan.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The most important thing I learned is that AI is a fast first-draft tool, not a final decision maker. It can generate a working method in seconds, but it does not know your design goals — it will happily suggest raising an exception where you wanted a warning, or returning a list where you needed an object. Staying in the role of lead architect means reading every suggestion critically, asking "does this fit the system I am building?", and running a test before trusting the answer. The AI saved a lot of typing; the judgment about what to keep was always mine.
