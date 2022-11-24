<template>
    <div class="container">
        <h1 class="text-center">Edit List</h1>
        <form @submit.prevent="editList">
            <div class="form-group">
                <label>List title</label>
                <input type="text" v-model="list_name" class="form-control" placeholder="Enter Card Name" autocomplete="off"
                    required />
            </div>
            <button type="submit" class="btn btn-primary btn-lg">Submit</button>
        </form>
    </div>
</template>
  
<script>
export default {
    name: "AddList",
    data() {
        return {
            list_id: this.$route.params.listId,
            ln: this.$route.params.listName,
            list_name: this.$route.params.listName
        };
    },
    methods: {
        async editList(e) {
            e.preventDefault();
            const data = {
                list_id: this.list_id,
                list_name: this.list_name,
            };
            console.log(data);
            const url = "http://127.0.0.1:5000/lists";
            const headers = {
                'Content-Type': 'application/json',
                'x-access-token': `${localStorage.getItem('token')}`
            }
            const res=await fetch(url, {
                method: "PUT",
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
    height: 70vh;
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
  