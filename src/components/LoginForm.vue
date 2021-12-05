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
    <button class="btn btn-primary">Submit</button>
  </form>
</template>

<script>
import {
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
  },
};
</script>
