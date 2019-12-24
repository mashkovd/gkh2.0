<template>
  <div>
    <b-pagination
      v-model="currentPage"
      :total-rows="totalRows"
      :per-page="perPage"
      align="fill"
      size="sm"
      class="my-0"
    ></b-pagination>

    <b-table
      id="diagnoses_table"
      small
      fixed
      striped
      hover
      small

      responsive="sm"
      :current-page="currentPage"
      :per-page="perPage"
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
                totalRows: 1,
                currentPage: 1,
                perPage: 15,
            }
        },
        computed: {},
        created() {
            this.next()


        },
        methods: {
            next() {
                axios.get('/api/diagnoses')
                    .then(response => {

                        this.items = response.data.items;
                        this.fields = response.data.fields;
                        this.totalRows = this.items.length;
                    })
                    .catch(error => console.log(error))
            },

        },

    }

</script>

<style>
</style>
