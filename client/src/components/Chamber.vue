<template>
  <div>
   <p> {{ msg }} </p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Chamber',
  data() {
    return {
      msg: 'kjngvfc',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/chamber';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
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
