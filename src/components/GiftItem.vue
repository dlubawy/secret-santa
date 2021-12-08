<template>
  <li class="list-group-item">
    <div class="row justify-content-center">
      <div class="col-sm-10">
        <a v-if="isLink(title)" v-bind:href="title"
          ><div class="text-truncate">{{ title }}</div></a
        >
        <span v-else>{{ title }}</span>
      </div>
      <div class="col-sm-2">
        <button v-on:click="$emit('remove')" class="btn btn-warning">
          Remove
        </button>
      </div>
    </div>
  </li>
</template>

<script>
export default {
  name: "GiftItem",
  methods: {
    isLink(text) {
      let exp =
        /((?:https?|ftp):\/\/[a-zA-Z0-9][\w+\d+&@\-#/%?=~_|!:,.;+]*)/gim;
      return text.match(exp) != null;
    },
  },
  props: {
    title: String,
  },
};
</script>
