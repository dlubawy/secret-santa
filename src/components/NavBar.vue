<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <a
        class="navbar-brand"
        href="/"
      >Secret Santa</a>
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
        <span class="navbar-toggler-icon" />
      </button>
      <div
        v-if="user"
        id="navbarSupportedContent"
        class="collapse navbar-collapse justify-content-end"
      >
        <ul class="navbar-nav ml-auto gap-2">
          <li class="nav-item">
            <div style="height: 8px" />
          </li>
          <li class="nav-item">
            <button
              class="btn btn-info"
              style="width: 100%"
              type="submit"
              @click="passwordReset"
            >
              Password Reset
            </button>
          </li>
          <li class="nav-item">
            <button
              class="btn btn-danger"
              style="width: 100%"
              type="submit"
              @click="logout"
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
  props: {
    user: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      email: "",
      password: "",
    };
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
