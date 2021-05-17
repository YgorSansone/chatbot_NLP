<template>
<div>
  <Menu />
    <div>
    <div class="div-interno">
      <h1>Registrar</h1>
      <hr />
      <form name="frmregistro" v-on:submit.prevent="validate">
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
        <button class="btn btn-success" type="submit">Cadastar</button>
      </form>
    </div>
  </div>
</div>
</template>

<script>
import axios from "axios";
import Menu from "@/components/menu.vue";
export default {
  components: {
    Menu
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
          this.cadastro();
        } else {
          console.log("email erro");
        }
      }
    },
    cadastro() {
      axios
        .post("http://127.0.0.1:5000/registro", {
          email: this.email,
          senha: this.senha,
        })
        .then((res) => {
          this.error = undefined;
          console.log(res)
        //   localStorage.setItem("token", res.data.token);
        this.$swal("Cadastrado com sucesso");
          this.$router.push({ name: "login" });
        })
        .catch((err) => {
          console.log(err.response);
          this.error = err.response.data.mensagem;
          this.$swal(err.response.data.mensagem);
        });
    },
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