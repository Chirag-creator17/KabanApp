<template>
    <div class="container">
        <h1 class="text-center">Add Card</h1>
        <form @submit.prevent="addCard">
            <div class="form-group">
                <label>Card title</label>
                <input type="text" v-model="card_title" class="form-control" placeholder="Enter Card Name" autocomplete="off"
                    required />
            </div>
            <div class="form-group">
                <label>Card Content</label>
                <input type="text" v-model="card_content" class="form-control" placeholder="Enter Card Content" autocomplete="off"
                    required>
            </div>
            <div class="form-group">
                <label>Card Deadline</label>
                <br/>
                <date-picker v-model="time1" valueType="format"></date-picker>
            </div>
            <div class="form-group">
                <label>Card Status</label>
                <select v-model="card_status" class="form-select">
                    <option value="True">Completed</option>
                    <option value="False">Not completed</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary btn-lg">Submit</button>
        </form>
    </div>

</template>
  
<script>
// import store from '../Vuex';
import DatePicker from 'vue2-datepicker';
import 'vue2-datepicker/index.css';
export default {
    name: "AddCard",
    components: { DatePicker },
    data() {
        return {
            time1: null,
            card_title: "",
            card_content: "",
            card_status: "",
            list_id: this.$route.params.listId
        };
    },
    methods: {
        async addCard(e) {
            e.preventDefault();
            // console.log(this.time1)
            var data = {};
            if (this.card_status == "True") {
                data = {
                    card_title: this.card_title,
                    card_content: this.card_content,
                    card_deadline: this.time1,
                    card_status: this.card_status,
                    card_completion_date: new Date().toJSON().slice(0, 10),
                }
            }
            else {
                data = {
                    card_title: this.card_title,
                    card_content: this.card_content,
                    card_status: this.card_status,
                    card_deadline: this.time1,
                };
            }
            console.log(data);
            const url = "http://127.0.0.1:5000/cards/" + this.list_id;
            const headers = {
                'Content-Type': 'application/json',
                'x-access-token': `${localStorage.getItem('token')}`
            }
            const res=await fetch(url, {
                method: "POST",
                headers: headers,
                body: JSON.stringify(data)
            });
            const data2 = await res.json();
            console.log(data2);
            this.$router.push('/DraggerComp');
        }
    },
}
</script>
  
<style scoped>
.container {
    font-family: "Muli", sans-serif;
    /* display: flex;
     */
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 75vh;
    overflow: hidden;
    margin-top: 75px;
}

label {
    font-size: 1.2rem;
    font-weight: 500;
    margin-bottom: 5px;
}

h1 {
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 2rem;
}

.form-group {
    margin-bottom: 1.5rem;
}
</style>
  