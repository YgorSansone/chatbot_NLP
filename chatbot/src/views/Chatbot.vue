<template>
<div>
  <Menu />
    <div>
    <nav class="navbar navbar-expand-sm bg-info">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link text-white" href="#">
            <span class="dot"></span>&nbsp;Chatbot está online
          </a>
        </li>
      </ul>
    </nav>
    <br />
    <div>
      <div
        style="overflow-y: scroll; height: 550px; width: 100%"
        align="center"
        id="msg"
      >
        <div
          class="talk-bubble tri-right left-top"
          style="width: 60%; background-color: #00aabb;float: left; margin-left: 50px;"
        >
          <div class="talktext">
            <p>Olá! Em que posso ajudar?</p>
          </div>
        </div>
        <div v-for="msg in mensagens" :key="msg.id">
          <div
            class="talk-bubble tri-right right-top"
            style="width: 60%; background-color: #8000ff;float: right; margin-right: 50px;"
          >
            <div class="talktext">
              <p>{{ msg.input }}</p>
            </div>
          </div>
          <div
            class="talk-bubble tri-right left-top"
            style="width: 60%; background-color: #00aabb; float: left; margin-left: 50px;"
          >
            <div class="talktext">
              <p>{{ msg.output}}</p>
            </div>
          </div>
          <div id="end">

          </div>
        </div>
      </div>
      <input
        type="text"
        id="input"
        class="form-control input_edit"
        v-on:keyup="quest"
        v-model="question"
        placeholder="Digite a sua mensagem e tecle Enter..."
      />
    </div>
    <!-- <input type="hidden" id="code_user" value="{{code_user}}" /> -->
    <!-- <input type="hidden" id="code_before" value="0" /> -->
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
      code_user: "0",
      code_before: 0,
      question: "",
      mensagens: [],
    };
  },
  methods: {
    quest(event) {
      if (event.key == "Enter") {
        if (this.question != "" && this.question != " ") {
          var data = {};
          data.code_user = this.code_user;
          data.code_before = this.code_before;
          data.question = this.question;
          var dados = {}
          dados.id = this.createCode()
          dados.input = this.question
          dados.output = "",
          this.question = ""
          this.mensagens.push(dados)
          axios.post(`http://127.0.0.1:5000/chatbot`, data).then(
            (response) => {
              console.log(response.data.lista[0]);
              var objIndex = this.mensagens.findIndex((msg => msg.id == dados.id));
              // response.data.lista[0].id = this.createCode();
              this.mensagens[objIndex].output=response.data.lista[0].output;
              this.code_before = parseInt(response.data.lista[0].code_current);
              console.log(this.mensagens);
              window.location.href = '#end';
            },
            (response) => {
              console.log("-------");
              console.log(response);
              window.location.href = '#end';
              // alert(response.data["mensagem"]);
              // this.$swal("" + response.data["mensagem"]);
            }
          );
          window.location.href = '#end';
        }
      }
    },
    createCode(){
    window.location.href = '#end';
    return Math.floor(new Date().valueOf() * Math.random())
    }
  },
};
</script>

<style>
.dot {
  height: 13px;
  width: 13px;
  background-color: lightgreen;
  border-radius: 50%;
  display: inline-block;
}
/* css de balão de diálogo */
.talk-bubble {
  margin: 10px;
  display: inline-block;
  position: relative;
  width: 100%;
  height: auto;
  color: white;
}

.tri-right.border.left-top:before {
  content: " ";
  position: absolute;
  width: 0;
  height: 0;
  left: -40px;
  right: auto;
  top: -8px;
  bottom: auto;
  border: 32px solid;
  border-color: #666 transparent transparent transparent;
}
.tri-right.left-top:after {
  content: " ";
  position: absolute;
  width: 0;
  height: 0;
  left: -20px;
  right: auto;
  top: 0px;
  bottom: auto;
  border: 22px solid;
  border-color: #00aabb transparent transparent transparent;
}

.tri-right.border.right-top:before {
  content: " ";
  position: absolute;
  width: 0;
  height: 0;
  left: auto;
  right: -40px;
  top: -8px;
  bottom: auto;
  border: 32px solid;
  border-color: #666 transparent transparent transparent;
}
.tri-right.right-top:after {
  content: " ";
  position: absolute;
  width: 0;
  height: 0;
  left: auto;
  right: -20px;
  top: 0px;
  bottom: auto;
  border: 20px solid;
  border-color: #8000ff transparent transparent transparent;
}

.talktext {
  padding: 1em;
  text-align: left;
  line-height: 1.5em;
}
.talktext p {
  -webkit-margin-before: 0em;
  -webkit-margin-after: 0em;
}
.input_edit{
    width: 90% !important;
    bottom: 3%;
    position: absolute;
    left: 5%;
}
</style>