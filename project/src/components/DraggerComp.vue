<template>
  <div class="container container-fluid">
    <div class="col-md">
      <div class="row">
        <div v-for="column in d" :key="column.list_name" class="back-container">
          <div class="row">
            <div class="col-md-10">
              <p class="card-text">
                <router-link :to="{ name: 'ListSummary', params: { listId: column.list_id } }">
                  {{ column.list_name }}
                </router-link>
              </p>
            </div>
            <div class="col-md-2">
              <router-link :to="{ name: 'AddCard', params: { listId: column.list_id } }"><img src="../assets/plus-circle.svg"
                  alt="plus" title="Add Card" /></router-link>
              <!-- <button class="add-button"><img src="../assets/plus-circle.svg" alt="plus" title="Add Card" /></button> -->
            </div>

          </div>
          <div v-for="task in t" :key="task.card_id">
            <div v-if="task.list_id === column.list_id">
              <task-card :task="task" :column="d" :column_id="column.list_id" />
            </div>
            <!-- <task-card v-if="task.l_id===column.l_id" :key="task.id" :task="task" /> -->
          </div>
          <div class="container">
            <div class="row">
              <div class="col-md-8 text-center"> <button class="btn btn-lg" @click="downloadList(column.list_id)">Export List </button> </div>
              <div class="col-md-2" style="margin-top: 7px;">
                <router-link :to="{ name: 'EditList', params: { listId: column.list_id ,listName: column.list_name} }"><img src="../assets/pencil-fill.svg" alt="trash"
                    title="Edit List" /></router-link>
              </div>
              <div class="col-md-2"><button class="btn" @click="deleteList(column.list_id)"><img
                    src="../assets/trash-fill.svg" alt="trash" title="Delete List" /></button></div>
            </div>
          </div>
        </div>
        <div class="back-container">
          <div class="row">
            <div class="col-md-10">
              <p class="card-text text-center">Add List</p>
            </div>
            <div class="col-md-2">
              <router-link to="/AddList"><img src="../assets/plus-circle.svg" alt="plus" title="Add List" />
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
// import draggable from "vuedraggable";
import TaskCard from "./TaskCard.vue";
// import store from "../Vuex";
export default {
  name: "DraggerComp",
  components: {
    TaskCard,
    // draggable
  },
  async created() {
    const headers = {
      'Content-Type': 'application/json',
      'x-access-token': `${localStorage.getItem('token')}`
    }
    const res = await fetch("http://127.0.0.1:5000/lists", {
      method: "GET",
      headers: headers
    });
    const k = [];
    const data = await res.json();
    for (let i = 0; i < data.length; i++) {
      k.push(data[i]);
    }
    // console.log(k);
    this.d = k;
    const f = [];
    for (const col in k) {
      // console.log(k[col].list_id);
      var url = "http://127.0.0.1:5000/cards/" + k[col].list_id;
      const res2 = await fetch(url, {
        method: "GET",
        headers: headers
      });
      const data2 = await res2.json();
      for (let i = 0; i < data2.length; i++) {
        // console.log(data2[i]);
        this.t.push(data2[i]);
        f.push(data2[i]);
      }
    }
    // for (const col in f) {
    //   console.log(f[col]);
    // }
    console.log("DraggerComp created");
  },
  data() {
    return {
      d: [],
      t: []
    };
  },
  methods: {
    async deleteList(list_id) {
      const headers = {
        'Content-Type': 'application/json',
        'x-access-token': `${localStorage.getItem('token')}`
      }
      const url = "http://127.0.0.1:5000/lists";
      const res = await fetch(url, {
        method: "DELETE",
        headers: headers,
        body: JSON.stringify({
          list_id: list_id
        })
      });
      const data = await res.json();
      console.log(data);
      this.$router.go()
    },
    async downloadList(list_id) {
      const headers = {
        'Content-Type': 'application/json',
        'x-access-token': `${localStorage.getItem('token')}`
      }
      const url = "http://127.0.0.1:5000/downloadList/" + list_id;
      await fetch(url, {
        method: "GET",
        headers: headers
      });

    }
  }
};
</script>

<style scoped>
.container {
  margin-top: 25px;
}

.column-width {
  min-width: 320px;
  width: 320px;
}

.back-container {
  background-color: #e2e2e2;
  border-radius: 5px;
  padding-left: 0.75rem;
  /* 12px */
  padding-right: 0.75rem;
  /* 12px */
  padding-top: 0.75rem;
  /* 12px */
  padding-bottom: 0.75rem;
  /* 12px */
  margin-right: 0.75rem;
  margin-bottom: 0.75rem;
  height: auto;
  width: 300px;

}
a{
  color: black;
}
/* Unfortunately @apply cannot be setup in codesandbox, 
but you'd use "@apply border opacity-50 border-blue-500 bg-gray-200" here */
.ghost-card {
  opacity: 0.5;
  background: #F7FAFC;
  border: 1px solid #4299e1;
}

.card-text {
  font-family: sans;
  font-size: 20px;
}

.add-button {
  background: none;
  border: none;
}
</style>
