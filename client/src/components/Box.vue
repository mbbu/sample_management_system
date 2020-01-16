<template>
 <table class=" table table-hover">
   <thead>
     <tr>
       <th scope="col"> Label </th>
       <th scope="col"> Tray </th>
       <th scope="col"> Rack </th>
       <th scope="col"> Chamber </th>
       <th scope="col"> Freezer </th>
       <th scope="col"> Lab Name </th>
       <th scope="col"> Lab Room </th>
       </tr>
   </thead>
   <tbody>
   <tr :key="box.id" v-for="box in response.message">
       <td> {{box.label}}</td>
       <td> {{box['tray.number']}}</td>
       <td> {{box['tray.rack.number']}}</td>
       <td> {{box['tray.rack.chamber.type']}}</td>
       <td> {{box['tray.rack.chamber.freezer.number']}}</td>
       <td> {{box['tray.rack.chamber.freezer.lab.name']}}</td>
       <td> {{box['tray.rack.chamber.freezer.lab.room']}}</td>
   </tr>
   </tbody>

 </table>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return{
      response: [],
    };
  },

  methods: {
    getBoxes() {
        axios.get('http://localhost:5000/box')
        .then((res) => {
          this.response = res.data;
          console.log(this.response)
        })
        .catch((error) => {
          console.error(error);
           });
      },
  },
  created() {
    this.getBoxes();
  },
};
</script>


