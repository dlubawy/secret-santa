// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDFd3pl3J8sSldetAnGCb9axRZla8uWEGg",
  authDomain: "secret-santa-8c877.firebaseapp.com",
  projectId: "secret-santa-8c877",
  storageBucket: "secret-santa-8c877.appspot.com",
  messagingSenderId: "631229824814",
  appId: "1:631229824814:web:a93fa1ce22c761291484bf",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

if (process.env.NODE_ENV === "development") {
  const emulators = require("./firebaseEmulators.js");

  emulators.auth(auth, "http://localhost:9099");
  emulators.firestore(db, "127.0.0.1", 8080);
}

export { auth, db };
