<template>
  <li class="list-group-item">
    <div class="row justify-content-center">
      <div class="col-sm-10 align-self-center">
        <span v-html="makeLink(title)"></span>
      </div>
      <div class="col-sm-2 align-self-center">
        <button
          v-if="!isLocked"
          v-on:click="$emit('remove')"
          class="btn-sm btn-warning"
        >
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
    makeLink(text) {
      let exp =
        /((?:https?|ftp):\/\/[a-zA-Z0-9][\w+\d+&@\-#/%?=~_|!:,.;+]*)/gim;
      return text.replace(exp, (matched) => {
        return `<a href="${matched}"><div class="text-truncate">${matched}</div></a>`;
      });
    },
  },
  props: {
    title: String,
    isLocked: Boolean,
  },
};
</script>
