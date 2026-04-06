export class Notifications {
    sendNotification(message: string): void {
        console.log(`Notification sent: ${message}`);
    }

    scheduleNotification(task: Task): void {
        const message = `Reminder: ${task.taskName} is scheduled.`;
        this.sendNotification(message);
    }
}