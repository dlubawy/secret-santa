<template>
  <li class="list-group-item">
    <div class="d-flex gap-2">
      <div class="d-flex col-lg">
        {{ title }}
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
  props: {
    title: String,
  },
};
</script>
