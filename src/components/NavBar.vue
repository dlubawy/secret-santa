<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">Secret Santa</a>
      <button
        v-if="user"
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div
        v-if="user"
        class="collapse navbar-collapse justify-content-end"
        id="navbarSupportedContent"
      >
        <ul class="navbar-nav ml-auto gap-2">
          <li class="nav-item">
            <div style="height: 8px"></div>
          </li>
          <li class="nav-item">
            <button
              v-on:click="passwordReset"
              class="btn btn-info"
              style="width: 100%"
              type="submit"
            >
              Password Reset
            </button>
          </li>
          <li class="nav-item">
            <button
              v-on:click="logout"
              class="btn btn-danger"
              style="width: 100%"
              type="submit"
            >
              Logout
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { auth } from "../firebaseConfig.js";
import { signOut, sendPasswordResetEmail } from "firebase/auth";

export default {
  name: "NavBar",
  data() {
    return {
      email: "",
      password: "",
    };
  },
  props: {
    user: {
      type: Object,
      default: null,
    },
  },
  methods: {
    logout() {
      signOut(auth).catch((error) => {
        console.log(error);
      });
    },
    passwordReset() {
      var resp = confirm("Send email for password reset?");
      if (resp == true) {
        sendPasswordResetEmail(auth, auth.currentUser.email);
      }
    },
  },
};
</script>
