<template>
  <div id="alerts" class="fixed-top">
    <div
      v-for="(alert, index) in alerts"
      v-bind:class="getClass(alert.type)"
      role="alert"
      v-bind:key="index"
    >
      {{ alert.text }}
      <button
        type="button"
        class="btn-close"
        data-bs-dismiss="alert"
        aria-label="Close"
        v-on:click="$emit('remove', index)"
      ></button>
    </div>
  </div>
</template>

<script>
export default {
  name: "AlertMessages",
  props: {
    alerts: Array,
  },
  methods: {
    getClass(type) {
      if (type == null) {
        type = "success";
      }
      return `alert alert-${type} alert-dismissible fade show`;
    },
  },
};
</script>

<style></style>
