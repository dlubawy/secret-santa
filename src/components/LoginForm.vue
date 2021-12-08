<template>
  <form v-if="!user" v-on:submit.prevent="login">
    <div class="mb-3">
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
    <div class="mb-3">
      <label for="exampleInputPassword1" class="form-label">Password</label>
      <input
        v-model="password"
        type="password"
        class="form-control"
        id="exampleInputPassword1"
      />
    </div>
    <div class="d-flex gap-2">
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
</template>

<script>
import {
  sendPasswordResetEmail,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
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
    user: String,
  },
  methods: {
    login() {
      signInWithEmailAndPassword(auth, this.email, this.password).catch(
        (error) => {
          const errorCode = error.code;
          if (errorCode === "auth/user-not-found") {
            var resp = confirm("User not found. Create an account?");
            if (resp == true) {
              createUserWithEmailAndPassword(auth, this.email, this.password);
            }
          } else if (errorCode === "auth/wrong-password") {
            alert("Invalid credentials.");
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
      }
    },
  },
};
</script>
