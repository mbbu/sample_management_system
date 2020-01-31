<template>
  <div class="container">
    <h2> Login </h2>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group
        id="input-group-1"
        label="Email address:"
        label-for="input-1"
      >
        <b-form-input
          id="input-1"
          v-model="form.email"
          type="email"
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-2" label="Your Password:" label-for="input-2">
        <b-form-input
          id="input-2"
          type="password"
          v-model="form.password"
        ></b-form-input>
      </b-form-group>

      <div class="wrapper">

        <b-form-group id="input-group-4">
        <b-form-checkbox-group v-model="form.checked" id="checkboxes-4">
          <b-form-checkbox value="me">Remember Me</b-form-checkbox>
        </b-form-checkbox-group>
      </b-form-group>

          <b-button type="submit" variant="primary">Submit</b-button>

          <p> Don't have an account yet?</p>

          <b-button type="register" variant="danger">Register</b-button> 
      </div>
    
 
      
    </b-form>
   
  </div>
</template>

<script>
  export default {
    data() {
      return {
        form: {
          email: '',
          checked: []
        },
        show: true
      }
    },
    methods: {
      onSubmit(evt) {
        evt.preventDefault()
        alert(JSON.stringify(this.form))
      },
      onReset(evt) {
        evt.preventDefault()
        // Reset our form values
        this.form.email = ''
        this.form.checked = []
        // Trick to reset/clear native browser form validation state
        this.show = false
        this.$nextTick(() => {
          this.show = true
        })
      }
    }
  }
</script>

<style>
.wrapper {
  text-align: center;
  display: inline-block;

}


</style>