<template>
<div>
  <table id="slots" class="grid-view" style="--cols:0;">
    <tr :key="i" v-for="(x,i) in this.slots">
      <td>
        <div v-if="x.available === true">
          <div ref="cells" class="cell-available-view">
          </div>
        </div>
        <div v-else>
          <div contenteditable="true" class="cell-occupied-view">{{x.code}}</div>
        </div>
      </td>
    </tr>
  </table>
</div>
</template>

<script>
import EventBus from "@/components/EventBus";

export default {
name: "Rectangle",
  data(){
    return{
      slots:[], cols: null, rows: null,
      availableSlots: []

    }
  },

  mounted(){
    EventBus.$on('slots-fetched', data => {
      this.slots = data
      this.drawSlots()
    })
  },

  methods: {
    resetBeforeChange(){
          this.rows = null;
          this.cols = null;
          document.getElementById('slots').style.setProperty("--cols", "0");
          this.availableSlots = []
    },

    drawSlots(){
      this.resetBeforeChange();

      // draw the slots of the selected box.
      // det the dimension of slots i.e rows and cols
      let last_slot = this.slots[this.slots.length - 1]
      this.rows = last_slot.position.row
      this.cols = last_slot.position.col

      // get slots that are available
      this.availableSlots = []
      for (let x=0; x < this.slots.length; x++){
        if (this.slots[x].available === true ){
          this.availableSlots.push(this.slots[x])
        }
      }

      let pad = document.getElementById('slots').style.getPropertyValue("--cols");
      document.getElementById('slots').style.setProperty("--cols", parseInt(pad) + this.cols);

      for (let i=0; i < this.slots.length; i++){
        if (this.slots[i].available === false){
          this.$refs.cells[i].style.backgroundColor = 'darkred'
        }
      }
    }
  },
}
</script>
