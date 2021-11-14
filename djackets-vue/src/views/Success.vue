<template>
  <div class="page-sign-up">
    <div class="columns is-multiline">
        <div class="column is-12">
            <h1 class="title">Thank you</h1>
            <p>Your order will be processed within 48 hours</p>
        </div>
    </div>
  </div>
</template>
<script>
  import axios from "axios"
  export default {
    name: 'Success',
    mounted() {document.title = 'Success | Djackets'},
  }
</script>