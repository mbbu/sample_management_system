<template>
<div>
  <table id="slots" class="grid-view" style="--cols:0;">
    <tr :key="i" v-for="(x,i) in this.slots">
      <td>
        <div v-if="x.available === true">
          <div ref="cells" class="cell-available-view"></div>
        </div>
        <div v-else>
          <div ref="cells" contenteditable="true" class="cell-occupied-view" @focusout="getNewSlotData(i)">
            {{x['sample.code']}}
          </div>
        </div>
      </td>
    </tr>
  </table>
</div>
</template>

<script>
import EventBus from "@/components/EventBus";
import axios from "axios";
import {slot_resource} from "@/utils/api_paths";
import {handleError, pageStartLoader, secureStoreGetAuthString, showFlashMessage} from "@/utils/util_functions";

export default {
name: "Rectangle",
  data(){
    return{
      slots:[], cols: null, rows: null,
      availableSlots: [], updatedSlots: [],
      time: 2000, // loader-time
    }
  },

  mounted(){
    EventBus.$on('slots-fetched', data => {
      this.slots = data
      this.drawSlots()
    })

    EventBus.$on('update-slots', this.updateSlotData)
  },

  methods: {
    resetBeforeChange(){
          this.rows = null;
          this.cols = null;
          this.availableSlots = []; this.updatedSlots = [];
          document.getElementById('slots').style.setProperty("--cols", "0");
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
    },

    getNewSlotData(index){
      // use the trim method to remove leading and trailing white spaces
      if (this.slots[index].code.trim() !== this.$refs.cells[index].textContent.trim()){
        this.updatedSlots.push({'old': this.slots[index]['sample.code'].trim(), 'new':this.$refs.cells[index].textContent.trim()})
      }
    },

    updateSlotData(){
      let loader = pageStartLoader(this);
      this.$log.info('updated slots are: ', this.updatedSlots, ' of type ', typeof this.updatedSlots[0])

      axios.put(slot_resource, {
              slots: {'updated' :this.updatedSlots}
          }, {
              headers:
                  {
                    Authorization: secureStoreGetAuthString()
                  }
          }).then((response) => {
                setTimeout(()=> {
                  loader.hide();
                  showFlashMessage(this, 'success', response.data['message'], '');
                },this.time)
          }).catch((error) => { handleError(this, error, loader) });
    },
  },
}
</script>
