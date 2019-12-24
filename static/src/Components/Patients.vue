<template>
  <div>
    <b-form>

      <b-button class="m-md-2" size="sm" variant="primary"
                v-b-modal.patient-modal>
        Добавить пациента
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
      id="patients_table"
      ref="table"
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
    <b-modal ref="addPatient"
             id="patient-modal"
             title="Новая запись"
             hide-footer
    >
      <b-form class="w-100" @submit="onSubmit">
        <b-form-group
          label="Фамилия:"
          label-cols-sm="8"
          label-cols-lg="4"
          label-for="patient_sur_name">
          <b-form-input
            id="patient_sur_name"
            v-model="form_data.patient_sur_name"

            required
          ></b-form-input>
        </b-form-group>

        <b-form-group
          label="Имя:"
          label-cols-sm="8"
          label-cols-lg="4"
          label-for="patient_first_name">
          <b-form-input
            id="patient_first_name"
            v-model="form_data.patient_first_name"

          ></b-form-input>
        </b-form-group>

        <b-form-group
          label="Возраст:"
          label-cols-sm="8"
          label-cols-lg="4"
          label-for="patient_age">
          <b-form-input
            id="patient_age"
            v-model="form_data.patient_age"
            type="number"
            min="0"
            max="100"
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
                    "patient_sur_name": null,
                    "patient_first_name": null,
                    "patient_age": null,
                },
            }
        },
        computed: {},
        created() {
            this.next()
        },
        methods: {
            next() {
                axios.get('/api/patients')
                    .then(response => {

                        this.items = response.data.items;
                        this.fields = response.data.fields;
                        this.totalRows = this.items.length;
                    })
                    .catch(error => console.log(error))
            },
            onSubmit(evt) {
                evt.preventDefault();
                this.$refs.addPatient.hide();
                let promise = axios.post('/api/patients', this.form_data)
                this.$refs.table.refresh()
                return promise.then((data) => {

                }).catch(error => {
                    return []
                })
            },

        },

    }

</script>

<style>

</style>
