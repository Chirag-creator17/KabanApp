<template>
    <div class="container container-fluid">
        <div class="col-md">
            <div class="row">
                <div v-for="column in d" :key="column.list_name" class="back-container">
                    <p class="card-text">{{ column.list_name }}</p>
                    <p>Number of completed Task : {{ column.missed_task }}/{{ column.total_task }}</p>
                    <p>Number of Deadline misses : {{ column.pending_task }}</p>
                    <template v-if="check(column.missed_task)">
                        <BarChart :data="barData(column.list_id)" />
                    </template>

                </div>
            </div>
        </div>
    </div>

</template>
  
<script>
// import draggable from "vuedraggable";
//   import TaskCard from "./TaskCard.vue";
// import store from "../Vuex";
import BarChart from "./BarChart.vue";
export default {
    name: "SummaryPage",
    components: {
        BarChart
    },
    async created() {
        var currentDateWithFormat = new Date().toJSON().slice(0, 10);
        // console.log(currentDateWithFormat);
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
        for (const col in k) {
            let c = 0, d = 0, dp = 0;
            // console.log(k[col].list_id);
            var url = "http://127.0.0.1:5000/cards/" + k[col].list_id;
            const res2 = await fetch(url, {
                method: "GET",
                headers: headers
            });
            const data2 = await res2.json();
            for (let i = 0; i < data2.length; i++) {
                // console.log(data2[i].card_deadline);
                if (data2[i].card_status == "True") {
                    c++;
                }
                else {
                    d++;
                }
                if (new Date(data2[i].card_deadline).toJSON().slice(0, 10) < currentDateWithFormat && data2[i].card_status == "False") {
                    dp++;
                }
                this.t.push(data2[i]);
                // console.log(new Date(data2[i].card_deadline));
                // console.log(new Date(data2[i].card_deadline).toJSON().slice(0, 10) < currentDateWithFormat && data2[i].card_status == "False");
            }
            k[col]["missed_task"] = c;
            k[col]["total_task"] = c + d;
            k[col]["pending_task"] = dp;
        }
        this.d = k;
        console.log("DraggerComp created");
    },
    data() {
        return {
            d: [],
            t: []
        };
    },
    methods: {
        check: function (a) {
            if (a > 0) {
                return true;
            }
            else {
                return false;
            }
        },
        barData: function (a) {
            let barDatas = {
                labels: [],
                datasets: [{ label: "Completed", data: [], backgroundColor: "#512DA8", }, { label: "Deadline", data: [], backgroundColor: "#FFA000", }]
            };
            // console.log(this.t);
            for (const col in this.t) {
                // console.log(this.t[col].list_id);
                if (this.t[col].list_id == a) {
                    if (this.t[col].card_completion_date != null) {
                        barDatas.labels.push(this.t[col].card_title);
                        let d = this.t[col].card_deadline.replaceAll("-", "");
                        let c = this.t[col].card_completion_date.replaceAll("-", "");
                        d -= 20220000;
                        c -= 20220000;
                        barDatas.datasets[0].data.push(c);
                        barDatas.datasets[1].data.push(d);
                    }
                }
            }
            return barDatas;

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
  