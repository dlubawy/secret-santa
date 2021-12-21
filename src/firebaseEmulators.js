import { connectFirestoreEmulator } from "firebase/firestore";
import { connectAuthEmulator } from "firebase/auth";

const firestore = connectFirestoreEmulator;
const auth = connectAuthEmulator;

export { firestore, auth };
