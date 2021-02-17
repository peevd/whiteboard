<template>
  <div class="card border shadow">
    <div class="card-body">

      <div class="row">
        <div class="col">
          <h3 class="mb-0">Presentations</h3>
        </div>
      </div>

      <div class="row">
        <div class="col">
          <PPTList :c-id="cId" />
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import PPTList from '@/components/PPTList';

export default {
  name: 'PPTSelectCard',
  components: {
    PPTList,
  },
  props: {
    cId: { type: Number, default: 0 },
  },
};
</script>
