<template>
<div>
  <div class="row">
        <div class="col">
          <table id="slots" class="grid" style="--cols:9;">
            <tr :key="i" v-for="(x,i) in 81">
              <td>
                <div v-if="1 || 3 || 5 || 7 || 9">
                  <div  ref="cells" class="slot-cell" @click="runCellAvailable(x, i)">
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
export default {
name: "Rectangle",
  data(){
    return{
      x: 0 , y: 0, cols: 0,
      width: 100, height: 100
    }
  }
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