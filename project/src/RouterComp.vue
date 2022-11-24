<script>
import Vue from 'vue';
import Router from 'vue-router';
import DraggerComp from './components/DraggerComp.vue'
import LoginComp from './components/LoginComp.vue'
import RegisterComp from './components/RegisterComp.vue'
import AddCard from './components/AddCard.vue'
import EditCard from './components/EditCard.vue'
import AddList from './components/AddList.vue'
import EditList from './components/EditList.vue'
import SummaryPage from './components/SummaryPage.vue'
import ListSummary from './components/ListSummary.vue'
Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    { path: '/DraggerComp', component: DraggerComp },
    { path: '/SummaryPage', component: SummaryPage },
    { path: '/Login', component: LoginComp },
    { path: '/Register', component: RegisterComp },
    { path: '/AddList', component: AddList },
    { path: '/AddCard/:listId', name: "AddCard", component: AddCard, props: true },
    {path : '/ListSummary/:listId', name: "ListSummary", component: ListSummary, props: true},
    { path: '/', redirect: '/Login' },
    { path: '/EditList/:listId', name: "EditList", component: EditList },
    { path: '/EditCard/:listId', name: "EditCard", component: EditCard, props: true }
  ]
});
</script>