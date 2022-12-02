<template>
  <div id="app" class="d-flex flex-column">
    <div id="background-image" class="bg-image flex-fill">
      <NavBar :user="user" />
      <AlertMessages v-bind:alerts="alerts" v-on:remove="removeAlert" />
      <div id="main">
        <div v-if="user" class="container text-center pt-5">
          <h1>Hello {{ user.displayName }}</h1>
          <div class="d-flex flex-column gap-5">
            <div v-if="secretName" class="row">
              <h2>You are {{ secretName }}'s Secret Santa!</h2>
              <h3 v-if="secretLocked">Their Wishlist 🔒</h3>
              <h3 v-else>Their Wishlist 🔓</h3>
              <div>
                <span>Reminder: the limit is $50 total</span>
                <ul class="list-group list-group-flush pt-3">
                  <li
                    v-for="(gift, index) in gifts"
                    v-bind:key="index"
                    class="list-group-item"
                  >
                    <span v-html="makeLink(gift)"></span>
                  </li>
                </ul>
              </div>
            </div>
            <div v-else class="row">
              <h2>You are not a Secret Santa!</h2>
              <span>Please check back later.</span>
            </div>
            <div class="row pb-3">
              <h3>Your Wishlist</h3>
              <h4>Time left to finish list:</h4>
              <h4><CountdownTimer /></h4>
              <div class="form-switch">
                <input
                  v-model="isLocked"
                  v-on:click="toggleLock"
                  class="form-check-input"
                  type="checkbox"
                  id="flexSwitchCheckDefault"
                />
                <label class="form-check-label" for="flexSwitchCheckDefault"
                  >Gift Lock</label
                >
              </div>
              <div>
                <form
                  v-if="isLocked"
                  v-on:submit.prevent="addNewGift"
                  class="input-group justify-content-center"
                >
                  <label for="new-gift" class="input-group-text"
                    >Add a gift ($50/gift limit)</label
                  >
                  <input
                    v-model="newGift"
                    id="new-gift"
                    placeholder="E.g. socks or a link to Amazon wish list"
                    class="form-control"
                    required="true"
                    disabled
                  />
                  <button class="btn btn-primary" disabled>Add</button>
                </form>
                <form
                  v-else
                  v-on:submit.prevent="addNewGift"
                  class="input-group justify-content-center"
                >
                  <label for="new-gift" class="input-group-text"
                    >Add a gift ($50/gift limit)</label
                  >
                  <input
                    v-model="newGift"
                    id="new-gift"
                    placeholder="E.g. socks or a link to Amazon wish list"
                    class="form-control"
                    required="true"
                  />
                  <button class="btn btn-primary">Add</button>
                </form>
                <ul class="list-group">
                  <GiftItem
                    v-for="(gift, index) in myGifts"
                    v-bind:key="index"
                    v-bind:title="gift"
                    v-bind:isLocked="isLocked"
                    v-on:remove="removeGift(index)"
                  />
                </ul>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="container pt-5">
          <LoginForm :user="user" v-on:addAlert="addAlert" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "./components/NavBar.vue";
import LoginForm from "./components/LoginForm.vue";
import GiftItem from "./components/GiftItem.vue";
import AlertMessages from "./components/AlertMessages.vue";
import CountdownTimer from "./components/CountdownTimer.vue";

import {
  doc,
  collection,
  getDoc,
  setDoc,
  onSnapshot,
} from "firebase/firestore";
import { db, auth } from "./firebaseConfig.js";

const userRef = collection(db, "users");

export default {
  name: "App",
  data() {
    return {
      user: null,
      isLocked: true,
      secretName: "",
      secretLocked: false,
      gifts: [],
      myGifts: [],
      newGift: "",
      alerts: [],
    };
  },
  methods: {
    makeLink(text) {
      let exp =
        /((?:https?|ftp):\/\/[a-zA-Z0-9][\w+\d+&@\-#/%?=~_|!:,.;+]*)/gim;
      return text.replace(exp, (matched) => {
        return `<a href="${matched}"><div class="text-truncate">${matched}</div></a>`;
      });
    },
    toggleLock() {
      getDoc(doc(userRef, auth.currentUser.uid))
        .then((publicUser) => {
          if (publicUser.data()) {
            setDoc(doc(userRef, auth.currentUser.uid), {
              gifts: this.myGifts,
              name: this.user.displayName,
              isLocked: this.isLocked,
            });
          }
        })
        .catch((error) => {
          if (error.code === "unavailable") {
            this.addAlert({
              text: "Failed to toggle the lock on your list because the client is offline.",
              type: "warning",
            });
          }
        });
    },
    addNewGift() {
      getDoc(doc(userRef, auth.currentUser.uid))
        .then((publicUser) => {
          if (publicUser.data()) {
            this.myGifts.push(this.newGift);
            this.newGift = "";
            setDoc(doc(userRef, auth.currentUser.uid), {
              gifts: this.myGifts,
              name: this.user.displayName,
              isLocked: this.isLocked,
            });
          }
        })
        .catch((error) => {
          if (error.code === "unavailable") {
            this.addAlert({
              text: "Failed to add gift because the client is offline.",
              type: "warning",
            });
          }
        });
    },
    removeGift(index) {
      getDoc(doc(userRef, auth.currentUser.uid))
        .then((publicUser) => {
          if (publicUser.data()) {
            this.myGifts.splice(index, 1);
            setDoc(doc(userRef, auth.currentUser.uid), {
              gifts: this.myGifts,
              name: this.user.displayName,
              isLocked: this.isLocked,
            });
          }
        })
        .catch((error) => {
          if (error.code === "unavailable") {
            this.addAlert({
              text: "Failed to remove gift because the client is offline.",
              type: "warning",
            });
          }
        });
    },
    addAlert(message) {
      this.alerts.push(message);
    },
    removeAlert(index) {
      this.alerts.splice(index, this.alerts.length);
    },
  },
  created() {
    auth.onAuthStateChanged((user) => {
      if (user) {
        this.user = user;
        getDoc(doc(userRef, user.uid))
          .then((publicUser) => {
            if (publicUser.data()) {
              const privateRef = collection(userRef, user.uid, "private");
              getDoc(doc(privateRef, "data")).then((privateUser) => {
                if (
                  privateUser.data().secret &&
                  privateUser.data().secret.uid
                ) {
                  onSnapshot(
                    doc(userRef, privateUser.data().secret.uid),
                    (secretUser) => {
                      this.secretName = secretUser.data().name;
                      this.gifts = secretUser.data().gifts;
                      this.secretLocked = secretUser.data().isLocked;
                    }
                  );
                }
              });
              if (publicUser.data().gifts && publicUser.data().gifts.length) {
                this.myGifts = publicUser.data().gifts;
                this.isLocked = publicUser.data().isLocked;
              }
            }
          })
          .catch((error) => {
            this.addAlert({ text: error.message, type: "warning" });
          });
      } else {
        this.user = null;
        this.locked = false;
        this.secretName = "";
        this.secretLocked = false;
        this.gifts = [];
        this.myGifts = [];
      }
    });
  },
  components: {
    NavBar,
    LoginForm,
    GiftItem,
    AlertMessages,
    CountdownTimer,
  },
};
</script>

<style>
#app {
  height: 100vh;
}
#background-image {
  background-image: url("./assets/pexels-george-dolgikh-giftpunditscom.webp");
  background-size: cover;
}
#main {
  text-shadow: 0 0 4px black;
}
</style>
