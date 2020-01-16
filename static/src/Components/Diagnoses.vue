<template>
  <div>

    <b-form>

      <b-button class="m-md-2" size="sm" variant="primary"
                v-b-modal.diagnose-modal>
        Добавить диагноз
      </b-button>
    </b-form>

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
      ref="diagnoses_table"
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

    <b-modal ref="addDiagnose"
             id="diagnose-modal"
             title="Новая запись"
             hide-footer
    >
      <b-form class="w-100" @submit="onSubmit">

        <b-form-group
          label="Название диагноза:"
          label-cols-sm="8"
          label-cols-lg="4"
          label-for="diagnose_name">
          <b-form-input
            id="diagnose_name"
            v-model="form_data.diagnose_name"

          ></b-form-input>
        </b-form-group>


        <b-form-group class="text-center"
                      label-cols-sm="10">
          <b-button type="submit" variant="primary" class="text-center">Добавить</b-button>
          <!--          <b-button type="reset" variant="danger">Сброс</b-button>-->
        </b-form-group>
      </b-form>
    </b-modal>


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
                form_data: {
                    "diagnose_name": null,
                },
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
            onSubmit(evt) {
                evt.preventDefault();
                this.$refs.addDiagnose.hide();
                let promise = axios.post('/api/diagnoses', this.form_data);

                return promise.then((data) => {
                  this.next();
                }).catch(error => {
                    return []
                })
            },

        },

    }

</script>

<style>
</style>
