<template>
  <div class="cards" :style="isCompleted">
    <div class="flex justify-between">
      <div class="row">
        <div class="col-md-8">
          <p class="cards-text text-center">{{ task.card_title }}</p>
        </div>
        <div class="col-md-4">
          <div class="btn-group">
            <button type="button" class="btn dropdown-toggle" data-bs-toggle="dropdown">
              <!-- <img src="../assets/arrow-right.svg" alt="plus" title="Move Card" /> -->
              Move
            </button>
            <ul class="dropdown-menu">
              <li v-for="columns in columnList" :key="columns.list_id"><a class="dropdown-item"
                  @click="dragCard(columns.list_id)">{{
                      columns.list_name
                  }}</a></li>
            </ul>
          </div>
        </div>
      </div>
      <p>{{ task.card_content }}</p>
    </div>
    <div class="flex row">
      <div class="col-md-6">{{ task.card_deadline }}</div>
      <div class="col-md-2">
        <button @click="downloadCard(task.list_id, task.card_id)"><img src="../assets/arrow-bar-up.svg"
            style="font-weight: bolder;" alt="export" title="Export Card" /></button>
      </div>
      <div class="col-md-2">
        <router-link :to="{ name: 'EditCard', params: { listId: task.list_id, cardId: task.card_id } }">
          <img src="../assets/pencil-fill.svg" alt="pencil" title="Edit Card" />
        </router-link>
        <!-- <button></button> -->
      </div>
      <div class="col-md-2">
        <button @click="deleteCard(task.card_id)"><img src="../assets/trash-fill.svg" alt="trash"
            title="Delete Card" /></button>
      </div>
    </div>
  </div>

</template>
<script>
export default {
  props: {
    task: {
      type: Object,
      default: () => ({})
    },
    column: {
      type: Array,
      default: () => []
    },
    column_id: {
      type: Number,
      default: 0
    }
  },
  computed: {
    isCompleted() {
      return {
        background: this.task.card_status == "True" ? "rgb(146 255 135)" : "white"
      };
    },
    columnList() {
      return this.column.filter(col => col.list_id != this.column_id);
    }
  },
  methods: {
    async deleteCard(card_id) {
      const url = "http://127.0.0.1:5000/cards/" + this.column_id;
      const headers = {
        'Content-Type': 'application/json',
        'x-access-token': `${localStorage.getItem('token')}`
      }
      const res = await fetch(url, {
        method: "DELETE",
        headers: headers,
        body: JSON.stringify({
          card_id: card_id
        })
      })
      const data = await res.json();
      console.log(data);
      this.$router.go()
    },
    async downloadCard(list_id, card_id) {
      const url = "http://127.0.0.1:5000/downloadCard/" + list_id + "/" + card_id;
      const headers = {
        'Content-Type': 'application/json',
        'x-access-token': `${localStorage.getItem('token')}`
      }
      await fetch(url, {
        method: "GET",
        headers: headers,
      })
    },
    async dragCard(new_list_id) {
      const card_id = this.task.card_id;
      const card_title = this.task.card_title;
      const card_content = this.task.card_content;
      const card_status = this.task.card_status;
      const card_deadline = this.task.card_deadline;
      var data12 = {};
      if (card_status == "True") {
        data12 = {
          card_title: card_title,
          card_content: card_content,
          card_deadline: card_deadline,
          card_status: card_status,
          card_completion_date: new Date().toJSON().slice(0, 10),
        }
      }
      else {
        data12 = {
          card_title: card_title,
          card_content: card_content,
          card_status: card_status,
          card_deadline: card_deadline,
        };
      }
      this.deleteCard(card_id);
      const url = "http://127.0.0.1:5000/cards/" + new_list_id;
      const headers = {
        'Content-Type': 'application/json',
        'x-access-token': `${localStorage.getItem('token')}`
      }
      const res = await fetch(url, {
        method: "POST",
        headers: headers,
        body: JSON.stringify(data12)
      })
      const data = await res.json();
      console.log(data);
      this.$router.go()
    }
  }
};
</script>
<style scoped>
.cards {
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  border-radius: 0.25rem;
  padding: 0.75rem;
  padding-left: 14px;
  padding-right: 14px;
  padding-top: 14px;
  padding-bottom: 14px;
  margin-top: 10px;
}

.cards-text {
  color: #465265;
  font-weight: 600;
  font-family: sans-serif;
  letter-spacing: 0.025em;
  font-size: 0.875rem;
}

.btn {
  padding: revert;
  margin-top: -7px;
}

button {
  background: none;
  border: none;
}
</style>
  