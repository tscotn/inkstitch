<template>
  <v-card class="pa-1 pt-2 mx-1" :disabled="!selected" :color="selected ? 'white' : 'grey lighten-3'">
    <v-tooltip top>
      <template v-slot:activator="{ on, attrs }">
        <v-card-title class="py-0 px-1 my-1 text-subtitle-2 text-truncate d-block allow-tooltip"
                      style="max-width: 100px"
                      v-text="name"
                      v-on="on"
                      v-bind="attrs"
                      :disabled="false"></v-card-title>
      </template>
      <span>{{ name }}</span>
    </v-tooltip>
    <v-img ref="thumbnail" class="checkerboard align-end" contain :src="thumbnail_url" width="100px" height="100px">
    </v-img>
    <v-card-actions class="pa-0">
      <v-img class="icon ml-1 my-1" v-if="stroke" :src="require('../assets/icons/stroke.png')" max-width="20px"></v-img>
      <v-img class="icon ml-1 my-1" v-if="fill" :src="require('../assets/icons/fill.png')" max-width="20px"></v-img>
      <v-img class="icon ml-1 my-1" v-if="clone" :src="require('../assets/icons/clone.png')" max-width="20px"></v-img>
      <v-img class="icon ml-1 my-1" v-if="polyline" :src="require('../assets/icons/polyline.png')" max-width="20px"></v-img>
    </v-card-actions>
  </v-card>
</template>

<script>
const inkStitch = require("../../lib/api")

export default {
  name: "ParamsThumbnail",
  props: {
    node_id: String,
    name: String,
    stroke_selected: false,
    fill_selected: false,
    clone_selected: false,
    polyline_selected: false,
  },
  data: function () {
    return {
      stroke: null,
      fill: null,
      polyline: null,
      clone: null,
      visible: false
    }
  },
  computed: {
    thumbnail_url() {
      if (this.visible) {
        return `${inkStitch.url}/params/thumbnail/${this.node_id}`
      } else {
        return ""
      }
    },
    sendlog() {
      console.log(`visible: ${this.node_id}`)
    },
    selected() {
      return (this.stroke_selected && this.stroke) ||
          (this.fill_selected && this.fill) ||
          (this.polyline_selected && this.polyline) ||
          (this.clone_selected && this.clone)
    }
  },
  created: function () {
    inkStitch.get(`params/object-types/${this.node_id}`).then(response => {
      this.stroke = response.data.stroke
      this.fill = response.data.fill
      this.polyline = response.data.polyline
      this.clone = response.data.clone
    })
  },
  mounted() {
    // This stuff makes it so that the thumbnail isn't generated until they've
    // scrolled it into view.  That way, if they select a bunch of stuff, we
    // don't kill their CPU by generating all the thumbnails at once.
    this.observer = new IntersectionObserver(entries => {
      const image = entries[0];
      if (image.isIntersecting) {
        this.visible = true;
        this.observer.disconnect();
      }
    }, {root: this.$parent.$el});

    this.observer.observe(this.$refs.thumbnail.$el);
  },
}
</script>

<style scoped>
.icon {
  display: inline-block;
}

.checkerboard:hover {
  /* this magic is from https://stackoverflow.com/a/51054396 */
  background-image: linear-gradient(to right, rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0.75)),
  linear-gradient(to right, black 50%, white 50%),
  linear-gradient(to bottom, black 50%, white 50%);
  background-blend-mode: normal, difference, normal;
  background-size: 8px 8px;
  background-repeat: repeat;
}

.allow-tooltip {
  pointer-events: auto;
  user-select: auto;
}
</style>
