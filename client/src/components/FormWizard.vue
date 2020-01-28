<template>
    <div class="tab-details">
        <ul class="steps has-content-centered">
            <li class="steps-segment" v-for="tab in tabs" :class="{ 'is-active': tab.isActive }" v-bind:key="tab.name">
                <span class="steps-marker"></span>
                <div class="steps-content">
                    <p class="is-size-4">{{tab.name}}</p>
                    <p>{{tab.info}}</p>
                </div>
            </li>
        </ul>                    
        <div class="tab-details">
            <slot :formData="formData"></slot>
        </div>
        <br/>
        <div class="field is-grouped">
            <div class="control" v-if="currentActive > 0">
                <button @click="previousTab()" class="button is-primary">Previous</button>
            </div>
            <div class="control" v-if="currentActive < totalTabs - 1">
                <button @click="nextTab()" class="button is-link">Next</button>
            </div>
            <div class="control" v-if="currentActive == totalTabs -1" >
                <button @click="submit()" class="button is-success">Submit</button>
            </div>
        </div>
                
    </div>
</template>


<script>

export default {
  name: 'form-wizard',
  
  data(){
    return{
        tabs: [],
        response: [],
        currentActive: 0,
        totalTabs: 0,
        formData: {
            theme: '',
            project: '',
            projectOwner: '',
            sampleType: '',
            species: '',
            description: '',
            lab: '',
            freezer:'',
            chamber:'',
            rack: '',
            tray: '',
            box: '',
            
            
            
            locationCollected: '',
            
            retention: '',
            barcode: '',
            analysis: '',
            temperature: '',
            amount: '',
            quantity_type: '',
            securityLevel: '',
            code: '',
            terms:'',
     }
        
    }
   },

    created(){
        this.tabs = this.$children;
        
    },

    mounted(){
        this.totalTabs = this.tabs.length;
    },

    methods:{

        previousTab(){
            this.currentActive--;
            this.tabs.forEach(tab => {
                tab.isActive = true;
            });
                this.tabs[this.currentActive].isActive = false;

        },

        nextTab(){
            //Validate input
            this.$root.$validator.validate('step'+(this.currentActive+ 1)+'.*').then(valid => {
                if (valid){
                    this.currentActive++;
                    this.tabs.forEach(tab => {
                        tab.isActive = false;
                    });
            
                    this.tabs[this.currentActive].isActive = true;
                }
            }); 

        },

        submit(){
            
            this.$root.$validator.validate('step'+this.totalTabs+'.*').then(valid => {
                if (valid){
                    alert("Everything passes ! Ready to Submit")
                }
            });
        },

    }
}
</script>


<style>
.tab-details {
    margin-top: 30px;
} 
</style>