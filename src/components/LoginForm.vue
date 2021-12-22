<template>
  <div id="loginForm">
    <h1 class="text-center">Please sign in</h1>
    <form v-on:submit.prevent="login">
      <div class="container">
        <label for="exampleInputEmail1" class="form-label">Email address</label>
        <input
          v-model="email"
          type="email"
          class="form-control"
          id="exampleInputEmail1"
          aria-describedby="emailHelp"
        />
        <div id="emailHelp" class="form-text">
          We'll never share your email with anyone else.
        </div>
      </div>
      <div class="container">
        <label for="exampleInputPassword1" class="form-label">Password</label>
        <input
          v-model="password"
          type="password"
          class="form-control"
          id="exampleInputPassword1"
        />
      </div>
      <div class="container">
        <button class="btn btn-primary">Submit</button>
        <button
          v-on:click="passwordReset"
          type="button"
          class="btn btn-secondary"
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
  data() {
    return {
      email: "",
      password: "",
    };
  },
  props: {
    user: Object,
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
          sendPasswordResetEmail(auth, this.email);
        }
      } else {
        resp = prompt("Enter your email address.");
        if (resp == true) {
          sendPasswordResetEmail(auth, resp);
        }
      }
    },
  },
};
</script>
