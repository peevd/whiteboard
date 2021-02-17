<template>
  <div class="card border shadow">
    <div class="card-body">

      <div class="row mb-3 align-items-center">
        <div class="col-auto pr-1">
          <custom-icon
            icon="task"
            size="3x" />
        </div>
        <div class="col">
          <h3 class="mb-0 pt-1">Results</h3>
        </div>
      </div>

      <div class="row">
        <div class="col">
          <StudentAnswerCard
            v-for="a in answers"
            :key="a.id"
            :answer="a"
            :task="getTaskById(a.task_id)"/>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import StudentAnswerCard from '@/components/StudentAnswerCard';

export default {
  name: 'StudentAnswersCard',
  components: {
    StudentAnswerCard,
  },
  props: {
    answers: {
      type: Array,
      default: () => [],
    },
    tasks: {
      type: Array,
      default: () => [],
    },
  },
  methods: {
    getTaskById(id) {
      return this.tasks.find(el => el.id === id);
    },
  },
};
</script>
