<template>
  <div>
    {{ formattedTime }}
  </div>
</template>

<script>
export default {
  name: "CountdownTimer",
  data() {
    return {
      timeLeft:
        new Date("12-25").setYear(new Date().getFullYear()) -
        1000 * 60 * 60 * 24 * 12 -
        new Date(),
    };
  },
  computed: {
    formattedTime() {
      let days = this.timeLeft / 1000 / 60 / 60 / 24;
      let hours = (days % 1) * 24;
      let minutes = (hours % 1) * 60;
      let seconds = (minutes % 1) * 60;
      return `${Math.floor(days)}d ${Math.floor(hours)}h ${Math.floor(
        minutes
      )}m ${Math.floor(seconds)}s`;
    },
  },
  methods: {
    startTimer() {
      setInterval(() => {
        this.timeLeft -= 1000;
      }, 1000);
    },
  },
  mounted() {
    this.startTimer();
  },
};
</script>

<style></style>
