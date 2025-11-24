<template>
  <li class="list-group-item">
    <div class="row justify-content-center">
      <div class="col-sm-10 align-self-center">
        <span v-html="makeLink(title)" />
      </div>
      <div class="col-sm-2 align-self-center">
        <button
          v-if="!isLocked"
          class="btn-sm btn-warning"
          @click="$emit('remove')"
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
  props: {
    title: String,
    isLocked: Boolean,
  },
  methods: {
    makeLink(text) {
      let exp =
        /((?:https?|ftp):\/\/[a-zA-Z0-9][\w+\d+&@\-#/%?=~_|!:,.;+]*)/gim;
      return text.replace(exp, (matched) => {
        return `<a href="${matched}"><div class="text-truncate">${matched}</div></a>`;
      });
    },
  },
};
</script>
