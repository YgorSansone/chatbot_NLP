<template>
<div>
  <Menu />
    <div>
    <div class="container">
      <h2>Lista de perguntas</h2>
      <div
        style="overflow-y: scroll; height: auto; width: : 100%;"
        align="center"
      >
        <table class="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Pergunta</th>
              <th>Resposta</th>
              <th>OPÇOES</th>
            </tr>
          </thead>
          <tbody v-for="pergunta in perguntas" :key="pergunta.code">
            <tr>
              <td nowrap="true">{{ pergunta.code }}</td>
              <td nowrap="true">{{ pergunta.question }}</td>
              <td nowrap="true">{{ pergunta.answer }}</td>
              <td nowrap="true">
                <router-link
                  :to="{ name: 'Editar', params: { id: pergunta.code } }"
                  ><button class="btn btn-primary">Editar</button></router-link
                > |
                <button
                  class="btn btn-danger"
                  @click="showmodal(pergunta.code)"
                >
                  DELETAR
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  <div v-if="show_modal">
    <transition name="modal">
      <div class="modal-mask">
        <div class="modal-wrapper">
          <div class="modal-dialog" role="document">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">Deletar pergunta ?</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                  <span aria-hidden="true" @click="hidemodal">&times;</span>
                </button>
              </div>
              <div class="modal-body">
                <p>Voce quer deletar essa pergunta ?</p>
                <br>
                <table class="table">
          <thead>
            <tr>
              <th>Pergunta</th>
              <th>Resposta</th>
            </tr>
          </thead>
          <tbody>
              <td nowrap="true">{{ perguntadel.question }}</td>
              <td nowrap="true">{{ perguntadel.answer }}</td>
          </tbody>
                </table>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="hidemodal">Cancelar</button>
                <button type="button" class="btn btn-primary" @click="deletarpergunta(perguntadel.code)">Deletar</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
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
      perguntas: [],
      delete_pergunta_code: "",
      perguntadel: [],
      show_modal: false,
    };
  },
  created: function () {
    this.funcperguntas();
  },
  methods: {
    funcperguntas() {
      axios.get(`http://127.0.0.1:5000/perguntas`).then(
        (response) => {
          console.log(response.data);
          this.perguntas = response.data;
        },
        (response) => {
          console.log("-------");
          console.log(response);
          //   window.location.href = '#end';
          // alert(response.data["mensagem"]);
          // this.$swal("" + response.data["mensagem"]);
        }
      );
    },
    showmodal(code) {
      console.log(code);
      this.delete_pergunta_code = code;
      var objIndex = this.perguntas.findIndex((pergunta => pergunta.code == this.delete_pergunta_code));
      console.log(objIndex)
      this.perguntadel.code = this.delete_pergunta_code;
      this.perguntadel.question = this.perguntas[objIndex].question;
      this.perguntadel.answer = this.perguntas[objIndex].answer;
      this.show_modal = true;
    },
    hidemodal() {
      this.show_modal = false;
    },
    deletarpergunta(code){
        var dados = {}
        dados.code = code
        this.hidemodal()
        console.log(dados)
              axios.post(`http://127.0.0.1:5000/perguntaDEL`, dados).then(
        (response) => {
          this.$swal("Deletado com sucesso");
          console.log(response);
          this.funcperguntas()
          // console.log(response)
        },
        (response) => {
          this.$swal("Deu erro");
          console.log("-------");
          console.log(response);
        }
      );
    }
  },
};
</script>

<style>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, .5);
  display: table;
  transition: opacity .3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}
</style>