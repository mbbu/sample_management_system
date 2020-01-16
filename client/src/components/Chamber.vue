<template>
  <table class=" table table-hover">
   <thead>
     <tr>
         <th scope="col"> Type </th>
       <th scope="col"> Freezer Number </th>
       <th scope="col"> Freezer Room </th>
       <th scope="col"> Code </th>
       </tr>
   </thead>
   <tbody>
     <tr v-for="chamber in response.chamber" :key="chamber.id">
<!--        <p> {{ value }} </p>-->
        <td> {{chamber.type}} </td>
        <td> {{chamber.freezer.room}} </td>
        <td> {{chamber.freezer.number}} </td>
         <td> {{chamber.code}} </td>
     </tr>
   </tbody>

 </table>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Chamber',
  data() {
    return {
      response: [],
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/chamber';
      axios.get(path)
        .then((res) => {
          this.response = res.data;
          console.log(res.data);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
}
</script>
