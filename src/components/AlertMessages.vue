<template>
  <div
    id="alerts"
    class="fixed-top"
  >
    <div
      v-for="(alert, index) in alerts"
      :key="index"
      :class="getClass(alert.type)"
      role="alert"
    >
      {{ alert.text }}
      <button
        type="button"
        class="btn-close"
        data-bs-dismiss="alert"
        aria-label="Close"
        @click="$emit('remove', index)"
      />
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
