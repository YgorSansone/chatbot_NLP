import Vue from 'vue'
import VueRouter from 'vue-router'
// import Home from '../views/Home.vue'
import Chatbot from '../views/Chatbot.vue'
import Lista from '../views/Lista.vue'
import Editar from '../views/Editar.vue'
import Cadastrar from '../views/Cadastrar.vue'
import Login from '../views/Login.vue'
import Registrar from '../views/Registrar.vue'
import axios from 'axios';
function AdminAuth(to,from,next){
  if(localStorage.getItem('token') != undefined){
    var dados = {
      id: localStorage.getItem('token'),
      email: localStorage.getItem('email'),
      code: localStorage.getItem('code'),
    }
    axios.defaults.headers.common = {'Authorization': `bearer ${localStorage.getItem('token_req')}`}
    axios.post("http://127.0.0.1:5000/validate",dados).then(res=>{
      console.log(res)
      next();
    }).catch(err =>{
      // localStorage.clear();
      console.log(err.response)
      next("/");
    })
  }else{
    next("/");
    // localStorage.clear();
  }
}
Vue.use(VueRouter)

const routes = [
  {
    path: '/lista',
    name: 'Lista',
    component: Lista,
    beforeEnter: AdminAuth
  },
  {
    path: '/chat',
    name: 'Chat',
    component: Chatbot
  },
  {
    path: '/cadastrar',
    name: 'Cadastrar',
    component: Cadastrar,
    beforeEnter: AdminAuth
  },
  {
    path: '/editar/:id',
    name: 'Editar',
    component: Editar,
    beforeEnter: AdminAuth
  },
  {
    path: '/',
    name: 'login',
    component: Login
  },
  {
    path: '/registrar',
    name: 'registrar',
    component: Registrar
  },
  
  // {
  //   path: '/about',
  //   name: 'About',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  // }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
