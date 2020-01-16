<template>
  <div>

    <b-form>

      <b-button class="m-md-2" size="sm" variant="primary"
                v-b-modal.department-modal>
        Добавить отделение
      </b-button>
    </b-form>

    <b-table
      id="departments_table"
      ref="departments_table"
      striped
      hover
      small

      responsive="sm"

      :items="items"
      :fields="fields"
    >

    </b-table>

    <b-modal ref="addDepartment"
             id="department-modal"
             title="Новая запись"
             hide-footer
    >
      <b-form class="w-100" @submit="onSubmit">

        <b-form-group
          label="Название отделения:"
          label-cols-sm="8"
          label-cols-lg="4"
          label-for="department_name">
          <b-form-input
            id="department_name"
            v-model="form_data.department_name"

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
                form_data: {
                    "department_name": null,
                },
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

                        this.items = response.data.items;
                        this.fields = response.data.fields
                    })
                    .catch(error => console.log(error))
            },
            onSubmit(evt) {
                evt.preventDefault();
                this.$refs.addDepartment.hide();
                let promise = axios.post('/api/departments', this.form_data);

                return promise.then((data) => {
                  this.next();
                }).catch(error => {
                    return []
                })
            },

        },

    }

</script>
