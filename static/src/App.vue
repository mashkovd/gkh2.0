<template>


  <div id="app">



    <div>
      <b-navbar toggleable="lg" type="dark" variant="info" >
        <b-navbar-brand href="/main" to="/main" >Главная</b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item href="/sick_lists" to="/sick_lists">Больничные листы</b-nav-item>
            <b-nav-item href="/consultants" to="/consultants">Консультанты</b-nav-item>
            <b-nav-item href="/patients" to="/patients">Пациенты</b-nav-item>
            <b-nav-item href="/diagnoses" to="/diagnoses">Болезни</b-nav-item>
            <b-nav-item href="/departments" to="/departments">Отделения</b-nav-item>

          </b-navbar-nav>

          <!-- Right aligned nav items -->
          <!--      <b-navbar-nav class="ml-auto">-->
          <!--        <b-nav-form>-->
          <!--          <b-form-input size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>-->
          <!--          <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>-->
          <!--        </b-nav-form>-->

          <!--        <b-nav-item-dropdown text="Lang" right>-->
          <!--          <b-dropdown-item href="#">EN</b-dropdown-item>-->
          <!--          <b-dropdown-item href="#">ES</b-dropdown-item>-->
          <!--          <b-dropdown-item href="#">RU</b-dropdown-item>-->
          <!--          <b-dropdown-item href="#">FA</b-dropdown-item>-->
          <!--        </b-nav-item-dropdown>-->

          <!--        <b-nav-item-dropdown right>-->
          <!--          &lt;!&ndash; Using 'button-content' slot &ndash;&gt;-->
          <!--          <template slot="button-content"><em>User</em></template>-->
          <!--          <b-dropdown-item href="#">Profile</b-dropdown-item>-->
          <!--          <b-dropdown-item href="#">Sign Out</b-dropdown-item>-->
          <!--        </b-nav-item-dropdown>-->
          <!--      </b-navbar-nav>-->
        </b-collapse>
      </b-navbar>
    </div>
  <p>
    <!-- используем компонент router-link для навигации -->
    <!-- входной параметр `to` определяет URL для перехода -->
    <!-- `<router-link>` по умолчанию отображается тегом `<a>` -->
<!--    <router-link to="/patients">Перейти к Foo</router-link>-->
<!--    <router-link to="/diagnoses">Перейти к Bar</router-link>-->
      <router-view></router-view>
  </p>


  </div>
</template>

<script>
    import axios from 'axios'

    export default {
        name: 'app',
        data() {
            return {
                languages: []
            }
        },

    }
</script>

<!--<style>-->
<!--  #app {-->
<!--    max-height: 100vh;-->
<!--    max-width: 100vw;-->
<!--  }-->

<!--</style>-->
