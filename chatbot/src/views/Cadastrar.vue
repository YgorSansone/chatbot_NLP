<template>
<div>
  <Menu />
    <div class="container">
    <h2>Cadastrar</h2>
    <form name="frmPerguntasEdicao" v-on:submit.prevent="salvar">
      <div class="form-group">
        <select
          class="form-control"
          name="code_relation"
          id="code_relation"
          v-model="selected"
        >
          <option value="0">Relação com a Resposta Anterior</option>
          <option
            v-for="selecao in selecaoperguntas"
            :key="selecao.code"
            v-bind:value="selecao.code"
          >
            {{ selecao.question }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="question">Pergunta:</label>
        <input
          type="text"
          class="form-control"
          name="question"
          id="question"
          v-model="perguntas.question"
        />
      </div>
      <div class="form-group">
        <label for="Ativo">Ativo:</label>
        <input type="checkbox" id="Ativo" class="md-switch" v-model="checked" />
      </div>
      <div class="form-group">
        <label for="answer">Resposta:</label>
        <textarea
          class="form-control"
          rows="5"
          name="answer"
          id="answer"
          v-model="perguntas.answer"
          spellcheck="false"
        >
        </textarea>
      </div>
      <router-link to="/lista"><button type="submit" class="btn btn-secondary">Cancelar</button></router-link> |
      <button type="submit" class="btn btn-primary">Cadastrar</button>
    </form>
  </div>
</div>
</template>

<script>
import axios from "axios";
import Menu from "@/components/menu.vue";
axios.defaults.headers.common = {'Authorization': `bearer ${localStorage.getItem('token_req')}`}
export default {
  components: {
    Menu
  },
  data() {
    return {
      perguntas: {},
      selecaoperguntas: [],
      id: 0,
      selected: "0",
      checked: false,
    };
  },
  created: function () {
    this.funcperguntas();
    this.funcinit();
  },
  methods: {
    funcperguntas() {
      axios.get(`http://127.0.0.1:5000/perguntas`).then(
        (response) => {
          this.selecaoperguntas = response.data;
          console.log(this.selecaoperguntas);
          // console.log(response)
        },
        (response) => {
          console.log("-------");
          console.log(response);
        }
      );
    },
    funcinit() {
        this.perguntas.question = "";
        this.perguntas.answer = "";
        this.perguntas.code_relation = "0";
        this.checked = true
    },
    salvar() {
      var dados = {};
      dados.code = this.id;
      dados.code_relation = this.selected;
      dados.question = this.perguntas.question;
      dados.answer = this.perguntas.answer;
      if (this.checked == true) {
        this.perguntas.active = 1;
      } else {
        this.perguntas.active = 0;
      }
      dados.active = this.perguntas.active;
      axios.post(`http://127.0.0.1:5000/perguntas`, dados).then(
        (response) => {
          this.$swal("Cadastrado com sucesso");
          console.log(response);
          this.$router.push({ name: "Lista" });
          // console.log(response)
        },
        (response) => {
          this.$swal("Deu erro");
          console.log("-------");
          console.log(response);
        }
      );
    },
  },
};
</script>

<style>
</style>