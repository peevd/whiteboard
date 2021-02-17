<template>
  <div
    id="modal"
    class="modal fade"
    tabindex="-1"
    role="dialog">
    <div
      class="modal-dialog"
      role="document">
      <div class="modal-content bg-default">

        <div class="modal-body text-center">
          <h5>Joining audio conference with teacher</h5>

          <button
            class="btn btn-success"
            @click="approve">Join</button>
        </div>

      </div>
    </div>
  </div>

</template>

<script>
import $ from 'jquery';

export default {
  name: 'JoinAudioModal',
  props: {
    show: { type: Boolean, default: false },
  },
  watch: {
    show(newVal) {
      if (newVal) {
        $(this.$el).modal('show');

        const component = this;
        $(this.$el).one('hidden.bs.modal', () => {
          component.$store.commit('toggleTaskCreate');
        });
      }
    },
  },
  methods: {
    approve() {
      $(this.$el).modal('hide');
      this.$emit('audioon');
    },
  },
};
</script>
