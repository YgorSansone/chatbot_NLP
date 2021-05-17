<template>
<div>
  <Menu />
    <div class="container">
    <h2>Editar</h2>
    <form name="frmPerguntasEdicao" v-on:submit.prevent="salvarEdicao">
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
      <router-link to="/lista"
        ><button type="submit" class="btn btn-secondary">
          Cancelar
        </button></router-link
      >
      |
      <button type="submit" class="btn btn-primary">Editar</button>
    </form>
  </div>
</div>
</template>

<script>
import axios from "axios";
axios.defaults.headers.common = {'Authorization': `bearer ${localStorage.getItem('token_req')}`}
import Menu from "@/components/menu.vue";
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
    this.id = this.$route.params.id;
    console.log(this.id);
    this.funceditperguntar();
    this.funcperguntas();
  },
  methods: {
    funcperguntas() {
      axios.get(`http://127.0.0.1:5000/perguntas`).then(
        (response) => {
          this.selecaoperguntas = response.data;
          var objIndex = this.selecaoperguntas.findIndex(
            (msg) => msg.code == this.id
          );
          this.selecaoperguntas.splice(objIndex, 1);
          console.log(this.selecaoperguntas);
          // console.log(response)
        },
        (response) => {
          console.log("-------");
          console.log(response);
        }
      );
    },
    funceditperguntar() {
      var dados = {};
      dados.code = this.id;
      console.log(dados);
      axios.post(`http://127.0.0.1:5000/pergunta`, dados).then(
        (response) => {
          this.perguntas.question = response.data.question;
          this.perguntas.answer = response.data.answer;
          this.perguntas.code_relation = response.data.code_relation;
          this.perguntas.active = response.data.active;
          this.selected = this.perguntas.code_relation;
          if (this.perguntas.active == 1) {
            this.checked = true;
          } else {
            this.checked = false;
          }
          console.log(this.perguntas);
          console.log(response);
        },
        (response) => {
          console.log("-------");
          console.log(response);
        }
      );
    },
    salvarEdicao() {
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
      axios.put(`http://127.0.0.1:5000/pergunta`, dados).then(
        (response) => {
          this.$swal("Atualizado com sucesso");
          console.log(response);
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