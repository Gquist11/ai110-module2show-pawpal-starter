class Profile {
    ownerName: string;
    petName: string;
    petType: string;
    petAge: number;

    constructor(ownerName: string, petName: string, petType: string, petAge: number) {
        this.ownerName = ownerName;
        this.petName = petName;
        this.petType = petType;
        this.petAge = petAge;
    }

    getProfileInfo(): string {
        return `Owner: ${this.ownerName}, Pet: ${this.petName}, Type: ${this.petType}, Age: ${this.petAge}`;
    }
}

export default Profile;