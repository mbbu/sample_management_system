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
     <tr v-for="(message, value) in boxes" :key="message">
        <td> {{message.label}} </td>
        <td> {{message.tray.number}} </td>
        <td> {{message.tray.rack.number}} </td>
         <td> {{message.tray.rack.chamber.type}} </td>
         <td> {{message.tray.rack.chamber.freezer.number}} </td>
         <td> {{message.tray.rack.chamber.freezer.lab.name}} </td>
         <td> {{message.tray.rack.chamber.freezer.lab.room}} </td>
     </tr>
   </tbody>

 </table>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return{
      boxes: [],
    };
  },
  
  methods: {
    getBoxes() {
        axios.get('http://localhost:5000/box')
        .then((res) => {
          this.boxes = res.data.boxes;
          console.log(this.boxes)
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


