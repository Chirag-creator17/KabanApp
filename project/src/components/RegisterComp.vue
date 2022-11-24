<template>
    <div class="container">
        <h1 class="text-center">Register</h1>
        <form v-on:submit="registerUser">
            <div class="form-group">
                <label>Email address</label>
                <input type="email" v-model="email" class="form-control" placeholder="Enter email" autocomplete="off" required>
            </div>
            <div class="form-group">
                <label>Username</label>
                <input type="text" v-model="u_name" class="form-control" placeholder="Enter Username" autocomplete="off" required />
            </div>
            <div class="form-group">
                <label>Name</label>
                <input type="text" v-model="name" class="form-control" placeholder="Enter Name" autocomplete="off" required />
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" v-model="password" minlength="8" class="form-control" placeholder="Password" autocomplete="off" required>
            </div>
            <button type="submit" class="btn btn-primary btn-lg">Submit</button>
        </form>
    </div>

</template>
  
<script>
export default {
    name: "RegisterComp",
    data() {
        return {
            email: "",
            u_name: "",
            name: "",
            password: ""
        }
    },
    methods: {
        async registerUser(e) {
            e.preventDefault() // Prevent page from reloading.
            console.log(this.email, this.password, this.u_name, this.name);
            const res = await fetch('http://127.0.0.1:5000/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: this.email,
                    password: this.password,
                    u_name: this.u_name,
                    name: this.name
                })
            });
            const data = await res.json();
            console.log(data);
            localStorage.setItem('user_name', this.u_name);
            this.$router.push('/login');
        }
    }
}
</script>
  
<style scoped>
.container {
    font-family: "Muli", sans-serif;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 75vh;
    overflow: hidden;
    margin-top: 50px;
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
  