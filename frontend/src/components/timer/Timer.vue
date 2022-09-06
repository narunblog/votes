<template>
  <div>
    <flip-countdown :deadline="deadline"></flip-countdown>
  </div>
</template>

<script>
  import FlipCountdown from 'vue2-flip-countdown'


  export default {
  components: {
    FlipCountdown,
  },
  props: {
    deadline: {
      type: String,
      required:true,
    }
  }
  }
</script>