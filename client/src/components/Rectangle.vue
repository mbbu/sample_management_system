<template>
<div>
  <div class="row">
        <div class="col">
          <table id="slots" class="grid" style="--cols:9;">
            <tr :key="i" v-for="(x,i) in 81">
              <td>
                <div v-if="1 || 3 || 5 || 7 || 9">
                  <div  ref="cells" class="slot-cell">
                  </div>
                </div>
                <div v-else>
                  <div class="cell-occupied"></div>
                </div>
              </td>
            </tr>
          </table>
        </div>
  </div>
</div>
</template>

<script>
import EventBus from "@/components/EventBus";

export default {
name: "Rectangle",
  data(){
    return{
      slots:null, cols: 0,

    }
  },

  mounted(){
    EventBus.$on('slots-fetched', data => {
      this.slots = data
    })
  },
}
</script>

<style scoped>
.slot-cell {
  width: 50px;
  height: 50px;
  background: green;
  display: table-cell;
}
</style>