<template>
  <div id="loginForm">
    <h1 class="text-center">
      Please sign in
    </h1>
    <form @submit.prevent="login">
      <div class="container">
        <label
          for="inputEmail1"
          class="form-label"
        >Email address</label>
        <input
          id="inputEmail1"
          v-model="email"
          type="email"
          class="form-control"
          aria-describedby="emailHelp"
          required="true"
        >
        <div
          id="emailHelp"
          class="form-text"
        >
          We'll never share your email with anyone else.
        </div>
      </div>
      <div class="container">
        <label
          for="inputPassword1"
          class="form-label"
        >Password</label>
        <input
          id="inputPassword1"
          v-model="password"
          type="password"
          class="form-control"
          required="true"
        >
      </div>
      <div class="container">
        <button class="btn btn-primary">
          Submit
        </button>
        <button
          type="button"
          class="btn btn-secondary"
          @click="passwordReset"
        >
          Password Reset
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import {
  sendPasswordResetEmail,
  signInWithEmailAndPassword,
} from "firebase/auth";

import { auth } from "../firebaseConfig.js";

export default {
  name: "LoginForm",
  props: {
    user: Object,
  },
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    login() {
      signInWithEmailAndPassword(auth, this.email, this.password).catch(
        (error) => {
          const errorCode = error.code;
          if (
            errorCode === "auth/wrong-password" ||
            errorCode === "auth/user-not-found"
          ) {
            this.$emit("addAlert", {
              text: "Invalid credentials.",
              type: "danger",
            });
          }
        }
      );
    },
    passwordReset() {
      if (this.email) {
        var resp = confirm(`Send email to ${this.email} for password reset?`);
        if (resp == true) {
          sendPasswordResetEmail(auth, this.email).then(() => {
            this.$emit("addAlert", { text: "Email sent.", type: "success" });
          });
        }
      } else {
        resp = prompt("Enter your email address.");
        if (resp !== null) {
          sendPasswordResetEmail(auth, resp).then(() => {
            this.$emit("addAlert", { text: "Email sent.", type: "success" });
          });
        }
      }
    },
  },
};
</script>
