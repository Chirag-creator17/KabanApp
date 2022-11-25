<template>
    <div class="container">
        <form @submit.prevent="addCard">
            <div class="form-group">
                <label>To which list you want to move the cards ?</label>
                <multiselect class="form-select" v-model="list_selected" :options="lists"></multiselect>
            </div>
            <button type="submit" class="btn btn-primary btn-lg">Submit</button>
        </form>
    </div>
</template>
<script>
import Multiselect from 'vue-multiselect';
export default {
    name: "DeleteListChoice",
    components: { Multiselect },
    data() {
        return {
            lists: [],
            list_id: this.$route.params.listId,
            list_selected: "",
        };
    },
    async created() {
        const url = "http://127.0.0.1:5000/lists";
        const headers = {
            'Content-Type': 'application/json',
            'x-access-token': `${localStorage.getItem('token')}`
        }
        const res = await fetch(url, {
            method: "GET",
            headers: headers,
        });
        const data = await res.json();
        let d = [];
        for (let i = 0; i < data.length; i++) {
            if(data[i].list_id != this.list_id){
                d.push(data[i]);
            }
        }
        this.lists = d;
    },
    methods: {
        async deleteCard(card_id) {
            const url = "http://127.0.0.1:5000/cards/" + this.list_id;
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
        },
        async dragCard(task, new_list_id) {
            const card_id = task.card_id;
            const card_title = task.card_title;
            const card_content = task.card_content;
            const card_status = task.card_status;
            const card_deadline = task.card_deadline;
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
        },
        async addCard(e) {
            e.preventDefault();
            console.log(this.list_selected.list_id);
            const listid = this.list_selected.list_id;
            const url = "http://127.0.0.1:5000/cards/" + this.list_id;
            const headers = {
                'Content-Type': 'application/json',
                'x-access-token': `${localStorage.getItem('token')}`
            }
            const res = await fetch(url, {
                method: "GET",
                headers: headers,
            });
            const data = await res.json();
            for (let i in data) {
                this.dragCard(data[i], listid);
            }
            const url2 = "http://127.0.0.1:5000/lists";
            const res1 = await fetch(url2, {
                method: "DELETE",
                headers: headers,
                body: JSON.stringify({
                    list_id: this.list_id
                })
            });
            const data1 = await res1.json();
            console.log(data1);
            this.$router.push('/DraggerComp');
        }
    }
};
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
    