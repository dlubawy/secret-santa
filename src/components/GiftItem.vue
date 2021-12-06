<template>
  <li class="list-group-item">
    <div class="d-flex gap-2">
      <div class="d-flex col-lg">
        <a v-if="isLink(title)" v-bind:href="title">{{ title }}</a>
        <span v-else>{{ title }}</span>
      </div>
      <div class="d-grid gap-2 d-md-flex justify-content-md-end">
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
