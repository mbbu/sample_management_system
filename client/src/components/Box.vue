<template>
 <table>
   <thead>
     <tr>
       <th scope="col"> Tray </th>
       <th scope="col"> Label </th>
       <tr> 
        </tr>
   </thead>

   <tbody>
     <tr v-for="(box, index) in boxes" :key="index">
        <td> box.tray</td>       
        <td> box.label</td>       

     </tr>
   </tbody>

 </table>
</template>

<script>
import axios from 'axios';

export default {
  data(){
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


