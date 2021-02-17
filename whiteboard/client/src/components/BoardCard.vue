<template>
  <div class="bg-default card shadow">
    <!--
    <div class="card-header">
      <a :href="data.href">
        <h3 class="mb-0">Board</h3>
      </a>
    </div>
    -->
    <div class="card-body">

      <div class="row mb-3">
        <div class="col">
          <h3>Board</h3>
        </div>
      </div>

      <div class="row">
        <div class="col">
          <img
            :src="data.boardSnapshot"
            class="board-preview border mb-4">
        </div>
      </div>

      <div class="row">
        <div class="col-auto">
          <p class="mb-0">Current Task:</p>
        </div>
        <div class="col">
          <p class="mb-0">{{ data.currentTask }}</p>
        </div>
        <div class="col-auto">
          <router-link
            :to="data.href"
            class="btn btn-sm btn-success">
            Open
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BoardCard',
  props: {
    data: {
      type: Object,
      default() {
        return {};
      },
    },
  },
};
</script>

<style scoped>
.board-preview {
  display: block;
  width: 100%;
  min-height: 100px;
  padding: 10px;
  background: url('../assets/bg_plus.png');
}

.board-preview > svg {
  width: 100%;
  height: 100%;
}
</style>
