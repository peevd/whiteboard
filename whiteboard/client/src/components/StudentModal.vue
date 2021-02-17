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
          <h3 class="modal-title">Student Answers</h3>
          <button
            type="button"
            class="close"
            data-dismiss="modal"
            aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="row align-items-center mb-4">
            <div class="col-auto">
              <img
                :src="pic"
                class="border rounded-circle"
                style="width: 75px; height: 75px;">
            </div>
            <div class="col">
              <h3>{{ student.first_name }} {{ student.last_name }}</h3>
            </div>
            <div class="col-auto">
              <h5 class="text-center"><strong>Completed tasks</strong></h5>
              <p class="text-center">{{ answers.length }}/{{ tasks.length }}</p>
              <ResultsChart
                :chart-data="genChart(
                [ answers.length, tasks.length - answers.length ], ['Answered', 'Unanswered'])"
                :height="150"
                :width="150" />
            </div>
          </div>

          <div class="row">
            <div class="col">
              <div class="accordion">

                <div
                  v-for="answer in answers"
                  :key="answer.id"
                  class="card">

                  <div
                    class="card-header task-header click-pointer btn-hover"
                    @click="toggleTask(answer.id)">
                    <div class="row align-items-center">
                      <div class="col">
                        <h2 class="mb-0">
                          {{ taskById(answer.task_id).name }}
                        </h2>
                      </div>
                      <div
                        v-if="answer.grade !== null"
                        class="col-auto">
                        <h2 class="mb-0">
                          {{ answer.grade }}%
                        </h2>
                      </div>
                      <div
                        v-if="answer.grade && taskFormat(answer.task_id) !== 1"
                        class="col-auto edit-btn">
                        <button
                          class="btn btn-default"
                          @click="editScore(answer.id)">
                          <font-awesome-icon
                            icon="edit"
                            size="1x" />
                        </button>
                      </div>
                    </div>
                  </div>

                  <div
                    :id="`answer-${answer.id}`"
                    :class="[ openTask === answer.id ? '' : 'collapse' ]">
                    <div class="card-body">

                      <div class="row mb-4">
                        <div
                          class="col-md-6">
                          <div
                            class="ProseMirror mb-4"
                            v-html="taskById(answer.task_id).description" />
                          <ResultsChart
                            v-if="answer.grade !== null"
                            :chart-data="genChart([ answer.grade, 100 - answer.grade ])"
                            :height="250"
                            :width="250"
                            :options="{ legend: { display: true, position: 'bottom' },
                                        responsive: false }"/>
                        </div>
                        <div class="col-md-6">
                          <template
                            v-if="taskFormat(answer.task_id) === 1">

                            <div
                              v-for="(q, i) in taskById(answer.task_id).test.questions"
                              :key="q.id"
                              class="row mb-4">

                              <div class="col">

                                <div class="row">
                                  <div
                                    class="col">
                                    {{ ++i }}. {{ q.text }}
                                  </div>
                                </div>

                                <div class="row">
                                  <div class="col pl-4">

                                    <div
                                      v-for="a in q.answers"
                                      :key="a.id"
                                      class="form-check">

                                      <input
                                        :id="`answer-${q.id}-${a.id}`"
                                        :checked="isAnswered(answer, q.id, a.id)"
                                        :value="a.id"
                                        :name="`answers-${q.id}`"
                                        disabled
                                        class="form-check-input input-radio"
                                        type="radio">
                                      <label
                                        :for="`answer-${q.id}-${a.id}`"
                                        :class="[ isAnsweredClass(answer, q.id, a.id) ]"
                                        class="form-check-label">
                                        {{ a.text }}
                                      </label>

                                    </div>

                                  </div>
                                </div>

                              </div>

                            </div>

                          </template>
                          <template
                            v-else>

                            <p>{{ answer.answers }}</p>

                          </template>
                        </div>
                      </div>

                      <div class="row justify-content-end">
                        <div
                          v-if="answer.grade === null || editTask[answer.id]"
                          class="col-auto">
                          <form
                            class="form-inline needs-validation"
                            @submit.prevent="gradeStudentAnswer(answer.task_id, answer.id)">
                            <label class="mr-2"><strong>Grade:</strong></label>
                            <input
                              v-model="grades[answer.id]"
                              type="number"
                              class="form-control mr-2"
                              style="width: 100px;"
                              min="0"
                              max="100"
                              required>
                            <input
                              type="submit"
                              class="btn btn-success">
                          </form>
                        </div>
                      </div>

                    </div>
                  </div>

                </div>

              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import $ from 'jquery';
import Pic from '@/assets/logo.png';
import ResultsChart from '@/components/ResultsChart';

export default {
  name: 'StudentModal',
  components: {
    ResultsChart,
  },
  props: {
    show: { type: Boolean, default: false },
    cId: { type: Number, default: 0 },
    student: {
      type: Object,
      default() {
        return {
          id: 0,
          first_name: '',
          last_name: '',
          picture: '',
        };
      },
    },
  },
  data() {
    return {
      grades: {},
      selectedAnswers: {},
      editTask: {},
      openTask: 0,
    };
  },
  computed: {
    pic() {
      return this.student.picture || Pic;
    },
    tasks() {
      return this.$store.state.currentTasks;
    },
    answers() {
      return this.$store.state.currentAnswers;
    },
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
    student(val) {
      if (val.id === 0) return;
      this.$store.dispatch('fetchStudentAnswers', {
        cId: this.cId,
        pId: val.id,
      });
    },
  },
  created() {
    this.$store.dispatch('fetchTasks', this.cId);
  },
  methods: {
    toggleTask(id) {
      if (this.openTask === id) {
        this.openTask = 0;
      } else {
        this.openTask = id;
      }
    },
    taskById(id) {
      return this.tasks.find(el => el.id === id) || {};
    },
    gradeStudentAnswer(tId, aId) {
      this.$store.dispatch(
        'gradeStudentAnswer',
        {
          cId: this.cId,
          tId,
          aId,
          pId: this.student.id,
          payload: {
            grade: this.grades[aId],
          },
        },
      );
      this.editTask[aId] = false;
    },
    taskFormat(id) {
      return this.taskById(id).format;
    },
    isAnswered(answer, qId, aId) {
      let flag = false;
      answer.answers.forEach((ans) => {
        if (ans.q_id === qId) {
          flag = ans.a_id.indexOf(aId) !== -1;
        }
      });

      return flag;
    },
    isAnsweredClass(answer, qId, aId) {
      let flag = false;
      let className = '';

      answer.answers.forEach((ans) => {
        if (ans.q_id === qId) {
          flag = ans.a_id.indexOf(aId) !== -1;
        }
      });

      if (flag) {
        const task = this.taskById(answer.task_id);
        const correctAnswers = task.test.correctAnswers;
        const qKey = String(qId);
        if (qKey in correctAnswers && correctAnswers[qKey].indexOf(aId) !== -1) {
          className += ' text-success';
        } else {
          className += ' text-danger';
        }
      }

      return className;
    },
    genChart(data, labels) {
      return {
        datasets: [{
          data,
          backgroundColor: ['#00cec9', '#ff7675 '],
        }],
        labels: labels || [
          'Correct',
          'Wrong',
        ],
      };
    },
    editScore(aId) {
      const tmp = {};
      tmp[aId] = !this.editTask[aId];
      this.editTask = Object.assign({}, this.editTask, tmp);

      if (!this.editTask[aId]) {
        this.grades[aId] = '';
      }
    },
  },
};
</script>

<style scoped>
.modal-dialog {
  min-width: 960px;
}

.smallsmall {
  font-size: 0.6em;
}

.task-header:not(:hover) .edit-btn {
  display: none;
}
</style>
