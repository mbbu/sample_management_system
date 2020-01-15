<template>
  <div>
    <p> {{ msg }}</p>
  </div>
</template>

<script>
import axios from 'axios';

  export default {
    name: 'Index',
    data() {
      return {
        msg: 'Hello Vue!',
      };
    },
    methods: {
      getMessage() {
        const path = 'http://localhost:5000/' || 'http://localhost:5000/index' || 'http://localhost:5000/welcome';
        axios.get(path)
                .then((res) => {
                  this.msg = res.data;
                  console.log(res.data);
                })
                .catch((error) => {
                  console.error(error);
                });
      },
    },
    created() {
      this.getMessage();
    },
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h3 {
    margin: 40px 0 0;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    display: inline-block;
    margin: 0 10px;
  }

  a {
    color: #42b983;
  }
</style>
