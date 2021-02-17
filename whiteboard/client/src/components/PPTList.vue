<template>
  <ul class="list-group list-group-flush">
    <li
      v-for="p in ppts"
      :key="p"
      class="list-group-item pl-0 pr-0" >
      <div class="row">
        <div class="col align-self-center">
          {{ p }}
        </div>
        <div
          v-if="allowSelect"
          class="col-auto">
          <button
            class="btn btn-sm btn-success"
            @click="handleSelect(p)">
            <custom-icon
              :icon="currentPPT.name === p ? 'checkboxChecked' : 'checkboxEmpty'"
              size="1x" />
          </button>
        </div>
        <div class="col-auto">
          <button
            class="btn btn-sm btn-danger"
            @click="handleDelete(p)">
            <custom-icon
              icon="trashBin"
              size="1x" />
          </button>
        </div>
      </div>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'PPTList',
  props: {
    cId: { type: Number, default: 0 },
    allowSelect: { type: Boolean, default: true },
  },
  computed: {
    ppts() {
      return this.$store.state.currentPPTs;
    },
    currentPPT() {
      return this.$store.state.currentPPT;
    },
  },
  created() {
    this.$store.dispatch('fetchPresentations', this.cId);
  },
  methods: {
    handleDelete(name) {
      const data = {
        cId: this.cId,
        name,
      };

      this.$store.dispatch('deletePPT', data);
    },
    handleSelect(ppt) {
      const data = {
        cId: this.cId,
        name: ppt,
      };

      this.$store.dispatch('selectPPT', data);
    },
  },
};
</script>
