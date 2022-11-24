<template>
    <div class="container">
        <h1 class="text-center">Edit Card</h1>
        <form @submit.prevent="editCard">
            <div class="form-group">
                <label>Card title</label>
                <input type="text" v-model="ct" class="form-control" placeholder="Enter Card Title" autocomplete="off"
                    required />
            </div>
            <div class="form-group">
                <label>Card Content</label>
                <input type="text" v-model="cc" class="form-control" placeholder="Enter Card Content" autocomplete="off"
                    required>
            </div>
            <div class="form-group">
                <label>Card Deadline</label>
                <br/>
                <date-picker v-model="time" valueType="format"></date-picker>
            </div>
            <div class="form-group">
                <label>Card Status</label>
                <select v-model="cs" class="form-select" placeholder="Enter Card Status">
                    <option value="True">Completed</option>
                    <option value="False">Not completed</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary btn-lg">Submit</button>
        </form>
    </div>

</template>
  
<script>
// import { waitForDebugger } from 'inspector';
import DatePicker from 'vue2-datepicker';
import 'vue2-datepicker/index.css';
// import store from '../Vuex';
export default {
    name: "EditCard",
    components: { DatePicker },
    data() {
        return {
            ct: "",
            cc: "",
            cs: "",
            time: null,
            p: this.$route.params.cardId,
            l: this.$route.params.listId
        }
    },
    async created() {
        // console.log(this.p, this.l);
        const headers = {
                'Content-Type': 'application/json',
                'x-access-token': `${localStorage.getItem('token')}`
            }
        const url = "http://127.0.0.1:5000/cards/" + this.l;
        const res = await fetch(url, {
            method: "GET",
            headers: headers,
        });
        let t = "", c = "", s = "",ti="";
        const data = await res.json();
        for (let i = 0; i < data.length; i++) {
            if (data[i].card_id === this.p) {
                t = data[i].card_title;
                c = data[i].card_content;
                s = data[i].card_status;
                ti=data[i].card_deadline;
            }
        }
        this.ct = t;
        this.cc = c;
        this.cs = s;
        this.time=ti;
        // console.log(this.cc, this.ct, this.cs, this.ti);
    },
    methods: {
        async editCard(e) {
            e.preventDefault();
            console.log(this.cc, this.ct, this.cs, this.time);
            var data = {};
            if(this.cs=="True"){
                data = {
                    card_id:this.p,
                    card_title: this.ct,
                    card_content: this.cc,
                    card_deadline: this.time,
                    card_status: this.cs,
                    card_completion_date: new Date().toJSON().slice(0, 10),
                }
            }
            else{
                data = {
                    card_id:this.p,
                    card_title: this.ct,
                    card_content: this.cc,
                    card_deadline: this.time,
                    card_status: this.cs,
                }
            }
            const headers = {
                'Content-Type': 'application/json',
                'x-access-token': `${localStorage.getItem('token')}`
            }
            const url = "http://127.0.0.1:5000/cards/" + this.l;
            const res=await fetch(url, {
                method: "PUT",
                headers: headers,
                body: JSON.stringify(data)
            });
            const data2 = await res.json();
            console.log(data2);
            this.$router.push('/DraggerComp');
        }
    }
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
  