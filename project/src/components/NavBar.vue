<template>
  <nav class="navbar navbar-expand-lg bg-light" style="width: 100%;">
    <div class="container-fluid">
      <router-link to="/DraggerComp" class="navbar-brand">{{u_name}}</router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link to="/DraggerComp" class="nav-link active" aria-current="page">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/Login" class="nav-link active" aria-current="page">Login</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/SummaryPage" class="nav-link active" aria-current="page">Summary</router-link>
          </li>
        </ul>
        <form class="d-flex" role="search">
          <button class="btn btn-outline-danger" type="submit" @click="logout">Logout</button>
        </form>
      </div>
    </div>
  </nav>
</template>
<script>
import { mapGetters } from 'vuex';
export default {
  data() {
    return {
      showMenu: false,
      u_name: localStorage.getItem('user_name'),
      token: null
    }
  },
  methods: {
    toggleNavbar: function () {
      this.showMenu = !this.showMenu;
    },
    logout() {
      // localStorage.removeItem('user_name');
      localStorage.removeItem('token');
      this.$router.push('/login');
    },
    getUserName() {
      if(localStorage.getItem('user_name') != null) {
        this.u_name = localStorage.getItem('user_name');
      }
      else {
        this.u_name = "Kanban";
      }
    },
    isLoggedIn() {
      if(localStorage.getItem('token') != null) {
        return true;
      }
      else {
        return false;
      }
    }
  },
  computed: {
    ...mapGetters(['isLoggedIn'])
  }
}
</script>