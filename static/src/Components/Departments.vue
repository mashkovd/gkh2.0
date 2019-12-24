<template>
  <div>

    <b-table
      id="consultants_table"
      striped
      hover
      small

      responsive="sm"

      :items="items"
      :fields="fields"
    >

    </b-table>


  </div>
</template>

<script>

    import axios from 'axios'


    export default {
        data() {
            return {
                fields: [],
                items: [],
            }
        },
        computed: {
            rows() {
                return this.items.length
            }
        },
        created() {
            this.next()


        },
        methods: {
            next() {
                axios.get('/api/departments')
                    .then(response => {

                        this.items = response.data.items
                        this.fields = response.data.fields
                    })
                    .catch(error => console.log(error))
            },

        },

    }

</script>
