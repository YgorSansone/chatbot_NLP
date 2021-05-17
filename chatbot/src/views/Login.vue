<template>
  <div>
    <Menu />
    <div>
      <div class="div-interno">
        <h1>Login</h1>
        <hr />
        <div class="form-floating mb-3">
          <input type="email" class="form-control" id="email" v-model="email" />
          <label for="email">Email:</label>
        </div>
        <div class="col-md 6">
          <div class="form-floating mb-3">
            <input
              type="password"
              name="senha"
              id="senha"
              placeholder=""
              class="senha form-control"
              v-model="senha"
            />
            <label for="senha">Senha:</label>
          </div>
        </div>
        <div class="text-center">
          <img
            alt="Logo"
            class="rounded"
            src="../assets/robot.gif"
            style="width: 20%"
          />
        </div>
        <hr />
        <!-- <button type="button" class="btn btn-success">Cadastrar parente</button> -->

        <router-link :to="{ name: 'registrar' }"
          ><button class="btn btn-secondary">Registrar</button></router-link
        >
        |
        <button class="btn btn-success" @click="validate">Entrar</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Menu from "@/components/menu.vue";
export default {
  components: {
    Menu,
  },
  data() {
    return {
      email: "",
      senha: "",
      valido: false,
      error: undefined,
    };
  },
  methods: {
    validateEmail(email) {
      var re = /\S+@\S+\.\S+/;
      return re.test(email);
    },
    validate() {
      var email = this.email;
      var senha = this.senha;
      if (email == "" || senha == "") {
        this.error = "Dados invalidos !";
        this.$swal("Dados invalidos !");
      } else {
        if (this.validateEmail(email)) {
          this.login();
        } else {
          console.log("email erro");
        }
      }
    },
    login() {
      axios
        .post("http://127.0.0.1:5000/login", {
          email: this.email,
          senha: this.senha,
        })
        .then((res) => {
          this.error = undefined;
          console.log(res);
          console.log(res.data.result[0]._id.$oid);
          localStorage.setItem("token_req", res.data.token);
          localStorage.setItem("token", res.data.result[0]._id.$oid);
          localStorage.setItem("email", res.data.result[0].email);
          localStorage.setItem("code", res.data.result[0].code);
          this.$router.push({ name: "Lista" });
        })
        .catch((err) => {
          console.log(err.response);
          this.error = err.response.data.err;
          this.$swal(err.response.data.err);
        });
    },
  },
  beforeMount() {
    var data = localStorage.getItem("token");
    var email = localStorage.getItem("email");
    var token = localStorage.getItem("token_req");
    if (data == undefined || email == undefined || token == undefined) {
      // this.is_user = false;
    } else {
      this.$router.push({ name: "Lista" });
    }
  },
};
</script>

<style>
</style>
<style scoped>
.div-interno {
  max-width: 80%;
  margin: auto;
  /* margin-top: 10px; */
  padding: 30px;
}
</style>