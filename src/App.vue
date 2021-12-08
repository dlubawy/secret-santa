<template>
  <div id="app" class="d-flex flex-column">
    <Navbar :user="user" />
    <div id="background-image" class="bg-image">
      <br />
      <div class="container">
        <div v-if="user" class="text-center">
          <h1>Hello {{ user }}</h1>
          <h2>You are {{ secretName }}'s Secret Santa!</h2>
          <h3>Their Wishlist</h3>
          <ul class="list-group list-group-flush">
            <li v-for="gift in gifts" v-bind:key="gift" class="list-group-item">
              <a v-if="isLink(gift)" v-bind:href="gift"
                ><div class="text-truncate">{{ gift }}</div></a
              >
              <span v-else>{{ gift }}</span>
            </li>
          </ul>
          <br />
          <h3>Your Wishlist</h3>
          <div>
            <form v-on:submit.prevent="addNewGift" class="input-group">
              <label for="new-gift" class="input-group-text"
                >Add a gift ($25 limit)</label
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
                v-bind:key="gift.id"
                v-bind:title="gift.title"
                v-on:remove="removeGift(index)"
              />
            </ul>
          </div>
          <br />
        </div>
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
      user: "",
      secretName: "",
      gifts: [],
      myGifts: [],
    };
  },
  methods: {
    isLink(text) {
      let exp =
        /((?:https?|ftp):\/\/[a-zA-Z0-9][\w+\d+&@\-#/%?=~_|!:,.;+]*)/gim;
      return text.match(exp) != null;
    },
    addNewGift() {
      this.myGifts.push({
        id: this.nextGiftId++,
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
            name: publicUser.data().name,
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
            name: publicUser.data().name,
          });
        }
      });
    },
  },
  created() {
    auth.onAuthStateChanged((user) => {
      if (user) {
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
              } else {
                this.secretName = "no one";
                this.gifts = [];
              }
              this.user = publicUser.data().name;
              if (publicUser.data().gifts && publicUser.data().gifts.length) {
                var id = 1;
                publicUser.data().gifts.forEach((gift) => {
                  this.myGifts.push({ id: id, title: gift });
                  id += 1;
                });
              }
            });
          } else {
            this.user = "No Name";
            this.secretName = "no one";
          }
        });
      } else {
        this.user = "";
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
  height: 100vh;
  background-size: cover;
}
</style>
