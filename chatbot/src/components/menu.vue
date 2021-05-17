<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light navbar-light bg-light">
      <div class="container-fluid">
        <!-- <a class="navbar-brand" href="#"></a> -->
        <!-- <img src="../assets/LOGO-FOME.png" style="width: 65px" /> -->
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNavAltMarkup"
          aria-controls="navbarNavAltMarkup"
          aria-expanded="false"
          aria-label="Toggle navigation"
          @click="showdiv()"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
          <div class="navbar-nav">
            <router-link to="/chat"><a class="nav-link active" aria-current="page" @click="reload">ChatBot</a></router-link>
            <div v-if="is_user">
              <router-link to="/lista"><a class="nav-link" aria-current="page" @click="reload">Lista</a></router-link>
            </div>
            <div v-if="is_user">
                <router-link to="/cadastrar"><a class="nav-link" aria-current="page" @click="reload">Cadastrar</a></router-link>
            </div>
          </div>
        </div>
        <div v-if="is_user">
          <div class="navbar-nav ml-auto">
            <a href="/" class="nav-item nav-link" @click="sair()">Sair</a>
          </div>
          <!-- <a class="nav-link right" id="right" href="/login" @click="sair()">Sair</a> -->
        </div>
        <div v-else>
          <div class="navbar-nav ml-auto">
            <a href="/" class="nav-item nav-link" @click="sair()">Login</a>
          </div>
        </div>
      </div>
    </nav>
        <div v-if="show" class="menu_cel">
          <div class="container-fluid">
          <div class="navbar-collapse">
          <div class="navbar-nav">
            <router-link to="/chat"><a class="nav-link active texto" aria-current="page">ChatBot</a></router-link>
            <div v-if="is_user">
              <router-link to="/lista"><a class="nav-link" @click="reload">Lista</a></router-link>
              <router-link to="/cadastrar"><a class="nav-link" @click="reload">Cadastrar</a></router-link>
              <!-- <a class="ms-auto" href="/admin/lista">Lista</a> -->
            </div>
          </div>
        </div>
        </div>
        </div>
  </div>
</template>
<script>
export default {
  name: "Menu",
  data() {
    return {
      is_user: false,
      show: false,
      status: localStorage.getItem("token_req")
    };
  },
  methods: {
    sair() {
      localStorage.clear();
    },
    showdiv(){
      this.show = !this.show
    },
    reload(){
      this.status = localStorage.getItem("token_req");
      if (this.status == undefined) {
        this.is_user = false;
      }
      else {
      this.is_user = true;
    }
    }
  },
  beforeMount() {
    var data = localStorage.getItem("token");
    var email = localStorage.getItem("email");
    this.status = localStorage.getItem("token_req");
    if (data == undefined || email == undefined) {
      this.is_user = false;
    } else {
      this.is_user = true;
    }
  },
  watch: {
    status(status) {
      if (status == undefined) {
        this.is_user = false;
      }
      else {
      this.is_user = true;
    }
    }
  }
};
</script>
<style scoped>
.menu_cel{
  background-color: #f8f9fa;
  
}
.menu_cel .texto{
color: rgba(0,0,0,.55);
}
</style>