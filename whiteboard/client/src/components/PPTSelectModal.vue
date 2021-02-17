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

        <div class="modal-header bg-default">
          <h3 class="modal-title">Choose presentation</h3>
          <button
            type="button"
            class="close"
            data-dismiss="modal"
            aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>

        <div class="modal-body">
          <PPTList
            :c-id="cId" />
        </div>

        <div class="modal-footer bg-default">
          <button
            type="button"
            class="btn btn-secondary"
            data-dismiss="modal">Close</button>
        </div>

      </div>

    </div>

  </div>
</template>

<script>
import $ from 'jquery';
import PPTList from '@/components/PPTList';

export default {
  name: 'PPTSelectModal',
  components: {
    PPTList,
  },
  props: {
    show: { type: Boolean, default: false },
    cId: { type: Number, default: 0 },
  },
  watch: {
    show(newVal) {
      if (newVal) {
        $(this.$el).modal('show');
      } else {
        $(this.$el).modal('hide');
      }

      const component = this;
      if (newVal === true) {
        $(this.$el).one('hide.bs.modal', () => {
          component.$emit('hide');
        });
      }
    },
  },
};
</script>
