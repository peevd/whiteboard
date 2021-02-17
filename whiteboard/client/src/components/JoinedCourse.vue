<template>
  <div
    id="joined-course"
    class="row">

    <div
      v-if="notMember"
      class="col-lg-12 col-xl-6 offset-xl-3 justify-content-center">
      <div class="jumbotron text-center p-4">
        <h3 class="mb-0">You are not a member of this course</h3>
      </div>
    </div>

    <template v-else>
      <div class="col-sm-12 col-md-6">

        <div class="row mb-4">
          <div class="col-sm-12">
            <CourseCardDetailed :course="course" />
          </div>
        </div>

        <div class="row mb-2">

          <div class="col-sm-12">
            <BoardCard
              :data="boardCardData" />
          </div>

        </div>

      </div>

      <div class="col-sm-12 col-md-6">
        <div class="row mb-4">
          <div class="col-12">
            <div class="bg-default card shadow">
              <div class="card-body">

                <div class="row mb-3 align-items-center">
                  <div class="col-auto pr-1">
                    <custom-icon
                      icon="task"
                      size="3x" />
                  </div>
                  <div class="col">
                    <h3 class="mb-0 pt-1">Tasks</h3>
                  </div>
                </div>

                <div
                  v-for="task in tasks"
                  :key="task.id"
                  class="card mb-2">
                  <div class="card-body py-3">
                    <div class="row align-items-center">
                      <div class="col">
                        <div class="row">
                          <div class="col">
                            <h5 class="mb-0">{{ task.name }}</h5>
                          </div>
                        </div>
                      </div>
                      <div class="col-auto">
                        <h3 class="mb-0 px-3">{{ task.task_number }}</h3>
                      </div>
                    </div>
                  </div>
                </div>

              </div>
            </div>
          </div>
        </div>

        <div class="row mb-4">
          <div class="col-12">
            <AppointmentsCard
              :events="events"
              :disable-edit="true" />
          </div>
        </div>

        <div class="row">
          <div class="col-12">
            <StudentAnswersCard
              :answers="answers"
              :tasks="tasks" />
          </div>
        </div>
      </div>
    </template>

  </div>
</template>

<script>
import AppointmentsCard from '@/components/AppointmentsCard';
import BoardCard from '@/components/BoardCard';
import CourseCardDetailed from '@/components/CourseCardDetailed';
import StudentAnswersCard from '@/components/StudentAnswersCard';

export default {
  name: 'JoinedCourse',
  components: {
    AppointmentsCard,
    BoardCard,
    CourseCardDetailed,
    StudentAnswersCard,
  },
  data() {
    return {
      notMember: false,
    };
  },
  computed: {
    cId() {
      return Number(this.$route.params.cId);
    },
    gId() {
      return this.$store.state.currentGroup.id;
    },
    course() {
      return this.$store.state.currentCourse;
    },
    tasks() {
      return this.$store.state.currentTasks;
    },
    answers() {
      return this.$store.state.currentAnswers;
    },
    board() {
      return this.$store.state.currentBoard;
    },
    boardSnapshot() {
      return this.$store.state.currentBoardSnapshot;
    },
    events() {
      return this.$store.state.events;
    },
    currentTask() {
      const taskId = this.board.task_id;
      const task = this.$store.state.currentTasks.find(el => el.id === taskId);
      return task ? task.name : 'unknown';
    },
    boardCardData() {
      return {
        board: this.board,
        boardSnapshot: this.boardSnapshot,
        currentTask: this.currentTask,
        cId: this.cId,
        gId: 1,
        href: `/joined-courses/${this.cId}/board`,
      };
    },
  },
  created() {
    const key = this.$route.query.key;
    const gId = this.$route.query.gId;

    const self = this;
    this.$store.dispatch('fetchJoinedCourse', this.cId)
      .then(() => {
        self.$store.dispatch('fetchGroupEvents', { cId: self.cId, gId: self.gId });
        self.$store.dispatch('fetchMyStudentAnswers', { cId: self.cId });
      })
      .catch(() => {
        if (key && gId) {
          const data = {
            cId: this.cId,
            gId,
            key,
          };

          this.$store.dispatch('joinCourse', data)
            .then(() => this.$store.dispatch('fetchJoinedCourse', this.cId))
            .catch(() => this.$router.push('/')); // todo: show some error that key is invalid
        } else {
          this.$router.push('/');
        }
      });
  },
};
</script>

<style scoped>
#joined-course {
  padding: 60px;
}
</style>
