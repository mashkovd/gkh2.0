<template>

     <div class="main_text">
       Больничные листы
     </div>

</template>

<script>
    import axios from 'axios'

    export default {
        name: 'Main',
        data() {
            return {
                items: []
            }
        },

    }
</script>

<style scoped>
  p {
    margin: 100px;
  }
  .main_text {
    padding: 50px;
    text-align: center;
  }

</style>
