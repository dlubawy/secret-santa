<template>
  <div id="app" class="d-flex flex-column">
    <Navbar :user="user" />
    <div id="background-image" class="bg-image">
      <div v-if="user" class="d-flex flex-column gap-5 mt-5 text-center">
        <div v-if="secretName" class="container">
          <h1>Hello {{ user.displayName }}</h1>
          <h2>You are {{ secretName }}'s Secret Santa!</h2>
          <h3>Their Wishlist</h3>
          <div>
            <span>Reminder: the limit is $50 total</span>
            <ul class="list-group list-group-flush">
              <li
                v-for="gift in gifts"
                v-bind:key="gift"
                class="list-group-item"
              >
                <span v-html="makeLink(gift)"></span>
              </li>
            </ul>
          </div>
        </div>
        <div v-else class="container">
          <h1>Hello {{ user.displayName }}</h1>
          <h2>You are not a Secret Santa!</h2>
          <span>Please check back later.</span>
        </div>
        <div class="container mt-5 mb-5">
          <h3>Your Wishlist</h3>
          <div>
            <form v-on:submit.prevent="addNewGift" class="input-group">
              <label for="new-gift" class="input-group-text"
                >Add a gift ($50/gift limit)</label
              >
              <input
                v-model="newGiftText"
                id="new-gift"
                placeholder="E.g. socks or a link to Amazon wish list"
                class="form-control"
              />
              <button class="btn btn-primary">Add</button>
            </form>
            <ul class="list-group">
              <GiftItem
                v-for="(gift, index) in myGifts"
                v-bind:key="index"
                v-bind:title="gift.title"
                v-on:remove="removeGift(index)"
              />
            </ul>
          </div>
        </div>
      </div>
      <div v-else class="d-flex flex-column text-center">
        <LoginForm :user="user" />
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "./components/Navbar.vue";
import LoginForm from "./components/LoginForm.vue";
import GiftItem from "./components/GiftItem.vue";

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
      secretName: "",
      gifts: [],
      myGifts: [],
      newGiftText: "",
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
    addNewGift() {
      this.myGifts.push({
        title: this.newGiftText,
      });
      this.newGiftText = "";
      var gifts = [];
      this.myGifts.forEach((gift) => {
        gifts.push(gift.title);
      });
      getDoc(doc(userRef, auth.currentUser.uid)).then((publicUser) => {
        if (publicUser.data()) {
          setDoc(doc(userRef, auth.currentUser.uid), {
            gifts: gifts,
          });
        }
      });
    },
    removeGift(index) {
      this.myGifts.splice(index, 1);
      var gifts = [];
      this.myGifts.forEach((gift) => {
        gifts.push(gift.title);
      });
      getDoc(doc(userRef, auth.currentUser.uid)).then((publicUser) => {
        if (publicUser.data()) {
          setDoc(doc(userRef, auth.currentUser.uid), {
            gifts: gifts,
          });
        }
      });
    },
  },
  created() {
    auth.onAuthStateChanged((user) => {
      if (user) {
        this.user = user;
        getDoc(doc(userRef, user.uid)).then((publicUser) => {
          if (publicUser.data()) {
            const privateRef = collection(userRef, user.uid, "private");
            getDoc(doc(privateRef, "data")).then((privateUser) => {
              if (privateUser.data().secret && privateUser.data().secret.uid) {
                onSnapshot(
                  doc(userRef, privateUser.data().secret.uid),
                  (secretUser) => {
                    this.secretName = secretUser.data().name;
                    this.gifts = secretUser.data().gifts;
                  }
                );
              }
              if (publicUser.data().gifts && publicUser.data().gifts.length) {
                var id = 1;
                publicUser.data().gifts.forEach((gift) => {
                  this.myGifts.push({ id: id, title: gift });
                  id += 1;
                });
              }
            });
          }
        });
      } else {
        this.user = null;
        this.secretName = "";
        this.gifts = [];
        this.myGifts = [];
      }
    });
  },
  components: {
    Navbar,
    LoginForm,
    GiftItem,
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
  text-shadow: 0 0 4px black;
}
</style>
