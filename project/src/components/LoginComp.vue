<template>
    <div class="container">
        <h1 class="text-center">Login</h1>
        <form @submit.prevent="loginUser">
            <div class="form-group">
                <label>Email</label>
                <input type="text" v-model="email" class="form-control" placeholder="Enter Email" autocomplete="off"
                    required />
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" v-model="password" class="form-control" placeholder="Password" autocomplete="off"
                    required>
            </div>
            <button type="submit" class="btn btn-primary btn-lg">Submit</button>

            <p class="text" style="margin-top:8px">
                Don't have an account? <a href="./register">Register</a>
            </p>
        </form>
    </div>

</template>
  
<script>
// import store from '../Vuex';
export default {
    name: "LoginComp",
    data() {
        return {
            email: "",
            password: ""
        }
    },
    methods: {
        async loginUser(e) {
            e.preventDefault();
            console.log(this.email, this.password);
            const res = await fetch('http://127.0.0.1:5000/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: this.email,
                    password: this.password
                })
            });
            const data = await res.json();
            console.log(data);
            // add token to local storage of web browser
            localStorage.setItem('token', data.token);
            this.$router.push('/DraggerComp');
            // store.commit('setToken', data.token);
            // store.dispatch('setToken', data.token);
            // const res2 = await fetch('http://127.0.0.1:5000/lists', {
            //     method: 'GET',
            //     headers: {
            //         'Content-Type': 'application/json',
            //         'x-access-token': `${data.token}`
            //     }
            // }).then(res => res.json()).then(data => console.log(data));
            // const data2 = await res2.json();
            // console.log(data2[0]);
             // Prevent page from reloading.
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
  