export class Task {
    taskName: string;
    duration: number; // in minutes
    urgency: string; // e.g., 'high', 'medium', 'low'
    isRecurring: boolean;

    constructor(taskName: string, duration: number, urgency: string, isRecurring: boolean) {
        this.taskName = taskName;
        this.duration = duration;
        this.urgency = urgency;
        this.isRecurring = isRecurring;
    }

    getTaskDetails(): string {
        return `Task: ${this.taskName}, Duration: ${this.duration} minutes, Urgency: ${this.urgency}, Recurring: ${this.isRecurring ? 'Yes' : 'No'}`;
    }

    markAsComplete(): void {
        console.log(`Task "${this.taskName}" has been marked as complete.`);
    }
}