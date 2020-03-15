<template>
  <div>
    <b-container fluid>

      <b-row>
        <b-col sm="1" md="6" class="my-1">
          <b-form-group
            label="Кол-во записей на странице"
            label-cols-sm="4"
            label-size="sm"
            label-for="perPageSelect"
            class="mb-0"
          >
            <b-form-select
              v-model="perPage"
              id="perPageSelect"
              size="sm"
              :options="pageOptions"
            ></b-form-select>
          </b-form-group>


        </b-col>


        <b-col sm="1" md="3" class="my-1">
          <b-form-group
            label="Всего записей"
            label-cols-sm="3"
            label-size="sm"
            label-for="perPageSelect"
            class="mb-0"
          >

            <b> {{ totalRows }} </b>
          </b-form-group>

        </b-col>
        <b-col sm="1" md="3" class="my-1">
          <b-form-group class="text-right"
          >
            <b-button variant="primary" size="sm" class="mr-2 text-center" @click="get_csv">
              Выгрузить в csv
            </b-button>
            <b-button variant="primary" size="sm" class="mr-2" v-b-modal.sicklist-modal>
              Добавить запись
            </b-button>
          </b-form-group>
        </b-col>


      </b-row>

      <b-form-group
        label="Фильтр"
        label-class="font-weight-bold pt-0"
        class="mb-0"
      >
        <b-row>
          <b-col sm="1" md="3" class="my-1">
            <b-form-group
              label-cols-lg="3"
              label="Консультант"
              label-size="sm"

              label-for="select_consultant"
            >

              <b-form-select
                id="select_consultant"
                v-model="filter.consultant"
                :options="consultants_options">

                <template v-slot:first>
                  <option :value="null">-- Укажите консультанта --</option>
                </template>
              </b-form-select>

            </b-form-group>
          </b-col>
          <b-col sm="1" md="3" class="my-1">
            <b-form-group
              label-cols-lg="3"
              label="Отделение"
              label-size="sm"

              label-for="select_department"
            >
              <b-form-select id="select_department" v-model="filter.department" :options="departments_options">
                <template v-slot:first>
                  <option :value="null">-- Укажите отделение --</option>
                </template>
              </b-form-select>

            </b-form-group>
          </b-col>

          <b-col sm="1" md="3" class="my-1">
            <b-form-group
              label-cols-lg="3"
              label="Пациент"
              label-size="sm"

              label-for="select_patient"
            >
              <b-form-input id="select_patient" v-model="filter.patient">
                <template v-slot:first>
                  <option :value="null">-- Укажите пациента --</option>
                </template>
              </b-form-input>

            </b-form-group>
          </b-col>

          <b-col sm="1" md="3" class="my-1">
            <b-form-group
              label-cols-lg="3"
              label="Дата"
              label-size="sm"

              label-for="select_date"
            >
              <b-form-input type="date" id="select_date" v-model="filter.select_date">
                <template v-slot:first>
                  <option :value="null">-- Укажите дату --</option>
                </template>
              </b-form-input>

            </b-form-group>
          </b-col>

          <b-col sm="1" md="3" class="my-1">
            <b-form-group
              label-cols-sm="1"
              label="№"
              label-size="sm"

              label-for="select_number"
            >
              <b-form-select id="select_number" v-model="filter.number" :options="number_options">
                <template v-slot:first>
                  <option :value="null">-- Укажите номер консультации --</option>
                </template>
              </b-form-select>

            </b-form-group>
          </b-col>

          <b-col sm="1" md="3" class="my-1">
            <b-form-group
              label-cols-lg="3"
              label="Коррекция"
              label-size="sm"

              label-for="select_correction"
            >

              <b-form-select id="select_correction" v-model="filter.correction" :options="correction_options">
                <template v-slot:first>
                  <option :value="null">-- Укажите коррекцию --</option>
                </template>
              </b-form-select>

            </b-form-group>
          </b-col>

          <b-col sm="1" md="3" class="my-1">
            <b-form-group
              label-cols-lg="3"
              label="Диагноз"
              label-size="sm"

              label-for="select_diagnose"
            >
              <b-form-input id="select_diagnose" v-model="filter.diagnose">
                <template v-slot:first>
                  <option :value="null">-- Укажите диагноз --</option>
                </template>
              </b-form-input>

            </b-form-group>
          </b-col>
          <b-col sm="1" md="3" class="my-1">
            <b-form-group
              label-cols-lg="3"
              label="Номер БЛ"
              label-size="sm"

              label-for="select_number_of_sl"
            >
              <b-form-input id="select_number_of_sl" type="number" v-model="filter.number_of_sl">
                <template v-slot:first>
                  <option :value="null">-- Укажите номер бл --</option>
                </template>
              </b-form-input>

            </b-form-group>
          </b-col>


        </b-row>
      </b-form-group>


      <b-pagination
        v-model="currentPage"
        :total-rows="totalRows"
        :per-page="perPage"
        align="fill"
        size="sm"
        class="my-0"
      ></b-pagination>


      <b-table
        id="sick_list_table"
        ref="sick_list_table"
        small
        fixed
        :filter="filter"
        :sort-by.sync="sortBy"
        :sort-desc.sync="sortDesc"
        :sort-direction="sortDirection"
        @filtered="onFiltered"

        style="width: 100%"


        :items="myProvider"
        :fields="fields"
        :current-page="currentPage"
        :per-page="perPage"
        @sort-changed="sortingChanged"

        head-variant="light"

      >
        <template v-slot:table-busy>
          <div class="d-flex justify-content-center mb-3">
            <b-spinner label="Loading..." class="align-middle"></b-spinner>
          </div>
        </template>


        <template v-slot:cell(actions)="row">
          <b-button variant="primary" size="sm" class="mr-2" @click="set_current_row(row)" v-b-modal.sicklist-modal>
            <font-awesome-icon icon="clone"/>
          </b-button>
          <b-button variant="primary" size="sm" class="mr-2" @click="del_current_row(row)">
            <font-awesome-icon icon="minus"/>
          </b-button>


        </template>


      </b-table>

      <b-modal ref="addSickList"
               id="sicklist-modal"
               title="Новая запись"
               hide-footer
      >
        <b-form class="w-100" @submit="onSubmit">

          <b-form-group
            label="Дата консультации:"
            label-cols-sm="8"
            label-cols-lg="4"
            label-for="sl_date">
            <b-form-input
              id="sl_date"
              type="date"
              v-model="form_data.sick_lists_sl_date"

              required
            ></b-form-input>
          </b-form-group>

          <b-form-group
            label="Консультант:"
            label-cols-sm="8"
            label-cols-lg="4"
            label-for="consultant_id">
            <b-form-select
              id="consultant_id"
              ref="consultant_select"
              :options="consultants_options"
              v-model="form_data.sick_lists_consultant_id"
              required

            ></b-form-select>
          </b-form-group>

          <b-form-group
            label="Номер больничного листа:"
            label-cols-sm="8"
            label-cols-lg="6"
            label-for="number_of_sl">
            <b-form-input
              id="number_of_sl"
              type="number"
              v-model="form_data.sick_lists_number_of_sl"
              required></b-form-input>
          </b-form-group>

          <b-form-group
            label="Номер консультации:"
            label-cols-sm="8"
            label-cols-lg="6"
            label-for="number_of_consultation">
            <b-form-input
              id="number_of_consultation"
              type="number"
              v-model="form_data.sick_lists_number_of_consultation"
              required
            ></b-form-input>
          </b-form-group>

          <b-form-group
            label="Пациент:"
            label-cols-sm="8"
            label-cols-lg="4"
            label-for="patient_sur_name">
            <b-form-input
              id="patient_sur_name"
              v-model="form_data.sick_lists_patient_sur_name"
              required
            ></b-form-input>
          </b-form-group>

          <b-form-group
            label="Возраст:"
            label-cols-sm="8"
            label-cols-lg="4"
            label-for="patient_age">
            <b-form-input
              id="patient_age"
              v-model="form_data.sick_lists_patient_age"
              type="number"
              min="0"
              max="100"
            ></b-form-input>
          </b-form-group>

          <!--          <b-form-group-->
          <!--            label="Пациент:"-->
          <!--            label-cols-sm="8"-->
          <!--            label-cols-lg="4"-->
          <!--            label-for="patient_id">-->
          <!--            <b-form-select-->
          <!--              id="patient_id"-->
          <!--              :options="patients_options"-->
          <!--              v-model="form_data.sick_lists_patient_id"-->
          <!--              required-->
          <!--              autocomplete="on"-->
          <!--            ></b-form-select>-->
          <!--          </b-form-group>-->

          <b-form-group
            label="Коррекция:"
            label-cols-sm="8"
            label-cols-lg="4"
            label-for="correction">
            <b-form-select
              id="correction"
              :options="correction_options"
              v-model="form_data.sick_lists_correction"
              required></b-form-select>
          </b-form-group>

          <b-form-group
            label="Отделение:"
            label-cols-sm="8"
            label-cols-lg="4"
            label-for="department_id"
          >
            <b-form-select
              id="department_id"
              :options="departments_options"
              v-model="form_data.sick_lists_department_id"
              required>

            </b-form-select>
          </b-form-group>

          <b-form-group
            label="Диагноз:"
            label-cols-sm="8"
            label-cols-lg="4"
            label-for="diagnose_id">
            <b-form-select
              id="diagnose_id"
              :options="diagnoses_options"
              v-model="form_data.sick_lists_diagnose_id"
              required>

            </b-form-select>
          </b-form-group>

          <b-form-group
            label="Причина:"
            label-cols-sm="8"
            label-cols-lg="4"
            label-for="reason_id">
            <b-form-select
              id="reason_id"
              :options="diagnoses_options"
              v-model="form_data.sick_lists_reason_id"
              required>

            </b-form-select>
          </b-form-group>

          <b-form-group
            label="Комментарий:"
            label-cols-sm="8"
            label-cols-lg="4"
            label-for="sl_comment">
            <b-form-textarea

              v-model="form_data.sick_lists_comment">

            </b-form-textarea>
          </b-form-group>

          <b-form-group class="text-center"
                        label-cols-sm="10">
            <b-button type="submit" variant="primary" class="text-center">Добавить</b-button>
            <!--          <b-button type="reset" variant="danger">Сброс</b-button>-->
          </b-form-group>
        </b-form>
      </b-modal>


    </b-container>
  </div>
</template>


<script>
    import axios from 'axios'

    export default {
        data() {
            return {
                totalRows: 1,
                fields: null,
                currentPage: 1,
                perPage: 5,
                pageOptions: [5, 10, 15, 100],
                sortBy: '',
                sortDesc: false,
                sortDirection: 'asc',
                filter: {
                    correction: null,
                    number: null,
                    consultant: null,
                    diagnose: null,
                    department: null,
                    patient: null,
                    select_date: null,
                    number_of_sl: null,

                },
                filterOn: [],

                correction_options: [
                    {text: 'Полная', value: 2},
                    {text: 'Частичная', value: 1},
                    {text: 'Не требуется', value: 0},
                ],
                number_options: [
                    {text: '1', value: 1},
                    {text: '2', value: 2},
                ],
                consultants_options: [],
                departments_options: [],
                patients_options: [],
                diagnoses_options: [],
                reasons_options: [],
                current_row: {},
                form_data: {
                    "sl_date": null,
                    "consultant_id": null,
                    "number_of_sl": null,
                    "number_of_consultation": null,
                    "patient_sur_name": null,
                    "patient_age": null,
                    "correction": null,
                    "department_id": null,
                    "diagnose_id": null,
                    "reason_id": null,
                    "comment": null
                },

            }
        },

        methods: {
            del_current_row(row) {
                let promise = axios.delete('/api/sick_lists', {data: {id: row.item.sick_lists_id}}
                );

                return promise.then((data) => {
                    this.$refs.sick_list_table.refresh()

                }).catch(error => {
                    return []
                })

            },
            set_current_row(row) {
                this.form_data = row.item

            },
            myProvider(ctx) {
                let promise = axios.get('/api/sick_lists',
                    {
                        params: {
                            perPage: ctx.perPage,
                            currentPage: ctx.currentPage,
                            filter: ctx.filter,
                        }
                    });

                return promise.then((data) => {
                    this.items = data.data.items;
                    this.fields = data.data.fields;
                    this.totalRows = data.data.totalRows;
                    return (data.data.items)
                }).catch(error => {
                    return []
                })
            },

            sortingChanged(ctx) {
            },

            getData() {
                axios.get('/api/consultants')
                    .then(response => {
                        this.consultants_options = response.data.items
                    })
                    .catch(error => console.log(error));

                axios.get('/api/departments')
                    .then(response => {
                        this.departments_options = response.data.items
                    })
                    .catch(error => console.log(error));

                axios.get('/api/patients')
                    .then(response => {
                        this.patients_options = response.data.items
                    })
                    .catch(error => console.log(error));
                axios.get('/api/diagnoses')
                    .then(response => {
                        this.diagnoses_options = response.data.items;
                        this.reasons_options = response.data.items
                    })
                    .catch(error => console.log(error));
            },

            onSubmit(evt) {
                evt.preventDefault();
                this.$refs.addSickList.hide();
                let promise = axios.post('/api/sick_lists', this.form_data);
                this.$refs.sick_list_table.refresh();
                return promise.then((data) => {

                }).catch(error => {
                    return []
                })
            },
            onFiltered(filteredItems) {
                // Trigger pagination to update the number of buttons/pages due to filtering
                //this.$refs.table.refresh()
                // let promise = axios.get('/api/sick_lists',
                //     {
                //         params: {
                //             perPage: this.perPage,
                //             filter: this.filter,
                //         }
                //     })
                //
                // return promise.then((data) => {
                //     this.items = data.data.items
                //     this.fields = data.data.fields
                //     this.totalRows = data.data.totalRows
                //     return (data.data.items)
                // }).catch(error => {
                //     return []
                // }),
                //
                //     this.currentPage = 1
            },
            get_csv() {

                axios.get('/api/csv',
                    {
                        params: {
                            filter: this.filter,
                        }
                    }
                )
                    .then(response => {
                        let csvContent = "data:text/csv;charset=utf-8,";
                        csvContent += response.data.csv_data;

                        const data = encodeURI(csvContent);
                        const link = document.createElement("a");
                        link.setAttribute("href", data);
                        link.setAttribute("download", "export.csv");
                        link.click();
                    })
                    .catch(error => console.log(error));


            }
        },
        computed: {
            // consultant_options: function ()
            // {
            //
            //
            // }

        },
        mounted: function () {
            this.getData()
        },

    }
</script>


<style>
  #sick_list_table {


  }
</style>
