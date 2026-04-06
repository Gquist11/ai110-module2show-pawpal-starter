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

**1. The scheduler now returns a full plan, not just a list.**
At first the scheduler just handed back a list of time slots. But I kept needing other info too — like the date, how many minutes were scheduled, and which tasks didn't fit. So I wrapped everything into one "Schedule" object that holds all of that together in one place.

**2. Owners can now have more than one free window per day.**
The original design only let you set one start time and one end time for the owner's availability. That didn't work for real life — someone might be free in the morning AND the evening. I changed it so you can add as many time windows as you need, and the scheduler will try each one.

**3. Each task slot now knows which pet it belongs to.**
Early on, a scheduled slot had no idea which pet it was for. That made it hard to show the pet's name in the app. I added a "pet" field to each slot so it always carries that info with it.

**4. Pet and Owner can do more than just hold data.**
Originally Pet and Owner were just containers — they stored info but didn't do much. As I built the app, I kept needing things like "show me only the unfinished tasks" or "mark this task as done." So I gave Pet and Owner their own helpful actions instead of putting all that work on the Scheduler.

**5. Priority now accepts plain words like "high" or "low".**
The app's input form sends priority as a regular word. The original code only understood its own internal format and would crash on plain text. I added a small helper that converts any version of the word into the right format automatically.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The conflict detector checks whether two scheduled slots overlap in time, but it only compares the final placed slots — it does not look ahead to warn you before the schedule is built. This means if the greedy scheduler quietly shifts a task to avoid a clash, no warning is shown even though two tasks wanted the same window. The tradeoff is simplicity: checking every pair of finished slots is easy to read and test, while pre-schedule conflict prediction would require running the algorithm twice or keeping extra state. For a single-owner, single-day planner this is reasonable — the user can see the output and spot if something landed in an unexpected time. A future version could add a pre-check that warns when two tasks share the same `earliest_start` before placement begins.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
