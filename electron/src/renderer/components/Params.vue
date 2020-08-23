<template>
  <v-card class="pa-2 ma-4">
    <div class="node-list material-scrollbar py-2">
      <params-thumbnail v-for="node in nodes" :key="node.id" class="thumbnail" :stroke_selected="stroke_selected" :fill_selected="fill_selected"
                        :polyline_selected="polyline_selected" :clone_selected="clone_selected" v-bind="node"></params-thumbnail>
    </div>
  </v-card>
</template>

<script>
const inkStitch = require("../../lib/api")
import ParamsThumbnail from './ParamsThumbnail.vue'

export default {
  name: "Params",
  components: {
    ParamsThumbnail
  },
  data: function () {
    return {
      nodes: [],
      stroke_selected: false,
      fill_selected: false,
      polyline_selected: false,
      clone_selected: false,
    }
  },
  computed: {
    thumbnail_url() {
      return `${inkStitch.url}/params/thumbnail/path4440-3-1-0`
    },
    logo() {
      return require("../assets/logo.png")
    }
  },
  created: function () {
    inkStitch.get('/params/objects').then(response => {
      this.nodes = response.data
    })
  }
}
</script>

<style scoped>
.thumbnail {
  display: inline-block;
}

.node-list {
  overflow-x: scroll;
  white-space: nowrap;
}

.node-list div.v-card {
  vertical-align: top;
  display: inline-block;
}

.material-scrollbar::-webkit-scrollbar {
  height: 10px;
  width: 10px;
  background-color: transparent;
}

.material-scrollbar::-webkit-scrollbar-thumb {
  border-radius: 8px;
  -webkit-box-shadow: inset 0 0 5px rgba(0, 0, 0, .3);
  background-color: rgb(140, 168, 224);
}

</style>
