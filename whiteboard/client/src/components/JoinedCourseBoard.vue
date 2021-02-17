<template>
  <div
    id="student-board"
    class="row align-self-stretch">
    <audio
      id="teacher-audio"
      autoplay />
    <JoinAudioModal
      :show="askToCall"
      @audioon="callTeacher"/>
    <div
      id="task-info"
      class="col-sm-3">

      <div class="row mb-4">
        <div
          ref="tasksCol"
          class="col-sm-12">
          <div
            v-show="!task || Object.keys(task).length === 0"
            class="card bg-default">

            <div class="card-body">
              <h5 class="mb-0">No task set</h5>
            </div>

          </div>

          <div
            v-if="task && Object.keys(task).length !== 0"
            class="row">
            <div class="col">
              <div class="card bg-default shadow">
                <div class="card-header p-0">
                  <button
                    id="tasks-toggle"
                    class="btn w-100"
                    title="Toggle task"
                    @click="toggleTask">
                    <custom-icon
                      icon="task"
                      size="2x" />
                    Current Task
                  </button>
                </div>
                <div class="card-body p-0">
                  <div
                    v-show="displayTask"
                    id="current-task"
                    ref="currentTask"
                    class="card bg-default">
                    <div class="card-body">

                      <div class="row">
                        <div class="col">
                          <h3 class="mb-0">{{ task.name }}</h3>
                        </div>
                      </div>

                      <div class="row">
                        <div class="col">
                          <div
                            class="ProseMirror"
                            v-html="task.description" />
                        </div>
                      </div>

                      <!-- open answer form -->
                      <div class="row">
                        <div class="col">
                          <form
                            v-if="task.format === 2"
                            class="form"
                            @submit.prevent="submitOpenAnswer">
                            <div
                              class="input-group">

                              <label
                                for="open-answer"
                                class="col-md-12 col-form-label">
                                Answer:
                              </label>

                              <div class="col-md-12">
                                <textarea
                                  id="open-answer"
                                  v-model="openAnswer"
                                  :disabled="taskAnswered"
                                  type="text"
                                  rows="2"
                                  @keydown.ctrl.enter="submitOpenAnswer" />
                              </div>

                            </div>
                            <div class="input-group">
                              <div class="col-sm-12">
                                <input
                                  :disabled="taskAnswered"
                                  :value="!taskAnswered ? 'Submit' : 'Submitted'"
                                  type="submit"
                                  class="btn btn-success">
                              </div>
                              <div
                                v-if="openError"
                                class="col-sm-12">
                                <small class="text-danger">
                                  Answer is empty.
                                </small>
                              </div>
                            </div>
                          </form>
                        </div>
                      </div>
                      <!-- end of open answer form -->

                      <!-- test form -->
                      <div class="row">
                        <div class="col">
                          <form
                            v-if="task.format === 1"
                            class="form"
                            @submit.prevent >

                            <div
                              v-for="(q, i) in task.test.questions"
                              :key="q.id"
                              class="row mb-4">

                              <div class="col">

                                <div class="row">
                                  <div class="col">
                                    {{ ++i }}. {{ q.text }}
                                  </div>
                                </div>
                                <div
                                  v-if="errors[q.id]"
                                  class="row">
                                  <div class="col">
                                    <small class="text-danger">
                                      Maximum number of answers for question is
                                      {{ task.test.correctAnswers[q.id] }}
                                    </small>
                                  </div>
                                </div>

                                <div class="row">
                                  <div class="col pl-4">

                                    <div
                                      v-for="a in q.answers"
                                      :key="a.id"
                                      class="custom-control custom-checkbox">

                                      <input
                                        :id="`answer-${task.id}-${q.id}-${a.id}`"
                                        :key="`answer-${task.id}-${q.id}-${a.id}`"
                                        :value="a.id"
                                        :name="`answers-${q.id}`"
                                        :disabled="taskAnswered"
                                        class="custom-control-input"
                                        type="checkbox"
                                        @input="(e) => handleTestAnswer(e, q.id, a.id)">
                                      <label
                                        :for="`answer-${task.id}-${q.id}-${a.id}`"
                                        class="custom-control-label">
                                        {{ a.text }}
                                      </label>

                                    </div>

                                  </div>
                                </div>

                              </div>

                            </div>

                            <div class="row">
                              <div class="col-sm-12">
                                <input
                                  :disabled="taskAnswered"
                                  :value="!taskAnswered ? 'Submit' : 'Submitted'"
                                  type="submit"
                                  class="btn btn-success"
                                  @click.prevent="submitTestAnswers">
                              </div>
                              <div
                                v-if="testError"
                                class="col-sm-12">
                                <small class="text-danger">
                                  All questions need to have an answer.
                                </small>
                              </div>
                            </div>

                          </form>
                        </div>
                      </div>
                      <!-- end of test form -->

                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col">
          <PPTPresentation
            :hide-controls="true"
            :c-id="cId" />
        </div>
      </div>

    </div>
    <div class="col-sm-9">
      <BoardCanvas
        :g-id="gId"
        :c-id="cId"
        :editable="boardEditable"
        :socket="socket" />
    </div>
    <div
      id="chat-corner"
      class="row align-items-end">

      <button
        v-if="peer && (peer.disconnected || !call || !call.open)"
        id="rejoin"
        class="btn"
        title="Rejoin audio conference"
        @click="rejoin">
        <custom-icon
          icon="phone"
          size="2x" />
      </button>

      <BoardChat
        :g-id="gId"
        :c-id="cId"
        :socket="socket" />

    </div>
  </div>
</template>

<script>
import io from 'socket.io-client';
import Peer from 'peerjs';
import config from '@/config.json';

import BoardCanvas from '@/components/BoardCanvas';
import BoardChat from '@/components/BoardChat';
import JoinAudioModal from '@/components/JoinAudioModal';
import PPTPresentation from '@/components/PPTPresentation';

export default {
  name: 'JoinedCourseBoard',
  components: {
    BoardCanvas,
    BoardChat,
    JoinAudioModal,
    PPTPresentation,
  },
  data() {
    return {
      socket: io(`${config.hostname}/data`, {
        path: '/whiteboard.io',
      }),
      peer: null,
      call: null,
      openAnswer: null,
      testAnswers: {},
      errors: {},
      testError: false,
      openError: false,
      displayTask: true,
      askToCall: false,
      boardEditable: false,
    };
  },
  computed: {
    cId() {
      return Number(this.$route.params.cId);
    },
    course() {
      return this.$store.state.currentCourse;
    },
    group() {
      return this.$store.state.currentGroup;
    },
    task() {
      return this.$store.state.currentTask;
    },
    questions() {
      return this.$store.state.currentQuestions;
    },
    me() {
      return `${this.$store.state.user.first_name} ${this.$store.state.user.last_name}`;
    },
    gId() {
      return this.$store.state.currentGroup.id;
    },
    taskAnswered() {
      return this.$store.state.currentTaskAnswered;
    },
    uId() {
      return this.$store.state.user.id;
    },
    currentAnswers() {
      return this.$store.state.currentAnswers;
    },
  },
  watch: {
    task() {
      this.$nextTick(() => this.onResize());
    },
  },
  created() {
    window.addEventListener('resize', this.onResize);

    this.$store.dispatch('fetchStudentBoard', this.cId)
      .then(() => {
        this.$store.dispatch('setBreadcrumbs', [
          {
            name: `${this.course.name}`,
            href: `/joined-courses/${this.course.id}`,
          },
        ]);

        const self = this;
        this.$store.dispatch('fetchMyStudentAnswers', { cId: this.cId })
          .then(() => {
            if (this.taskAnswered) {
              const answer = this.currentAnswers.find(el => el.task_id === this.task.id);
              self.setAnswer(answer.answers);
            }
          });


        const sockData = { room: this.cId, data: { name: this.me } };
        this.socket.emit('joined', sockData);

        const peerId = `${this.uId}-${this.cId}-${this.gId}`;

        if (config.peerPort) {
          this.peer = new Peer(peerId, {
            key: config.peerKey,
            host: config.peerHost,
            port: config.peerPort,
            secure: config.peerSecure,
          });
        } else {
          this.peer = new Peer(peerId, {
            key: config.peerKey,
            host: config.peerHost,
            secure: config.peerSecure,
          });
        }

        this.peer.on('error', (err) => {
          self.$toastr.error(err, 'Peer error');
        });

        this.peer.on('open', () => {
          self.askToCall = true;
          // self.callTeacher();
        });
      });

    if (this.socket !== null) {
      this.socket.on('task_transfer', (data) => {
        this.openAnswer = null;
        this.testAnswers = {};
        this.errors = {};
        this.testError = false;
        this.openError = false;
        const self = this;
        this.$store.dispatch('fetchTask', data)
          .then(() => {
            if (this.taskAnswered) {
              const answer = this.currentAnswers.find(el => el.task_id === data.tId);
              self.setAnswer(answer.answers);
            }
          });
      });

      this.socket.on('b_edit', (data) => {
        this.boardEditable = data;
      });
    }
  },
  mounted() {
    this.$nextTick(() => this.onResize());
  },
  beforeDestroy() {
    this.socket.disconnect();
    this.peer.destroy();
  },
  methods: {
    setAnswer(ans) {
      if (this.task.format === 1) {
        const answers = {};
        ans.forEach((el) => { answers[String(el.q_id)] = el.a_id; });

        this.testAnswers = answers;
        this.checkAnswerBoxes();
      } else {
        this.openAnswer = ans;
      }
    },
    submitOpenAnswer() {
      if (this.openAnswer !== null && this.openAnswer !== '') {
        this.openError = false;

        this.$store.dispatch('submitAnswer', {
          cId: this.cId,
          tId: this.task.id,
          payload: {
            answers: this.openAnswer,
          },
        });
      } else {
        this.openError = true;
      }
    },
    submitTestAnswers() {
      if (Object.keys(this.testAnswers).length === this.task.test.questions.length) {
        this.testError = false;

        const answers = [];
        Object.keys(this.testAnswers)
          .forEach(el => answers.push({ q_id: Number(el), a_id: this.testAnswers[el] }));

        this.$store.dispatch('submitAnswer', {
          cId: this.cId,
          tId: this.task.id,
          payload: {
            answers,
          },
        });
      } else {
        this.testError = true;
      }
    },
    callTeacher() {
      const teacherPeerId = `${this.cId}-${this.gId}`;
      const aStream = new AudioContext();
      const call = this.peer.call(teacherPeerId,
        aStream.createMediaStreamDestination().stream);

      this.call = call;

      call.on('stream', (s) => {
        this.$toastr.info('Audio stream recieved');
        const audioEl = this.$el.querySelector('#teacher-audio');
        audioEl.srcObject = s;
      });
      call.on('close', () => {
        this.callTeacher();
      });
      call.on('error', err => this.$toastr.error(err, 'Call error'));
    },
    onResize() {
      const height = document.documentElement.clientHeight;
      const tasksColEl = this.$refs.tasksCol;
      const currentTaskEl = this.$refs.currentTask;
      if (currentTaskEl) {
        const rect = tasksColEl.getBoundingClientRect();
        currentTaskEl.style.maxHeight = `${height - rect.top - 110}px`;
      }
    },
    toggleTask() {
      this.displayTask = !this.displayTask;
    },
    handleTestAnswer(e, qId, aId) {
      const isChecked = e.srcElement.checked;

      if (isChecked) {
        if (!this.testAnswers[qId] ||
            this.testAnswers[qId].length < this.task.test.correctAnswers[qId]) {
          this.testAnswers = Object.assign({}, this.testAnswers, {
            [qId]: this.testAnswers[qId] ? this.testAnswers[qId].concat([aId]) : [aId],
          });
          this.errors = Object.assign({}, this.errors, {
            [qId]: false,
          });
        } else {
          this.errors = Object.assign({}, this.errors, {
            [qId]: true,
          });
          const lastAnswer = this.testAnswers[qId].pop();
          const lastCheckbox = this.$el.querySelector(`#answer-${qId}-${lastAnswer}`);
          lastCheckbox.checked = false;
          this.testAnswers = Object.assign({}, this.testAnswers, {
            [qId]: this.testAnswers[qId] ? this.testAnswers[qId].concat([aId]) : [aId],
          });
        }
      } else {
        this.testAnswers = Object.assign({}, this.testAnswers, {
          [qId]: this.testAnswers[qId].filter(el => el !== aId),
        });
        this.errors = Object.assign({}, this.errors, {
          [qId]: false,
        });
      }
    },
    rejoin() {
      if (this.peer) {
        // todo: handle destroyed connection and check time for id to be freed
        if (this.peer.disconnected) {
          this.peer.reconnect();
        }

        if (!this.call || !this.call.open) {
          this.callTeacher();
        }
      }
    },
    answerSelected(qId, aId) {
      return this.testAnswers[qId] !== undefined ?
        this.testAnswers[qId].findIndex(el => el === aId) !== -1 :
        false;
    },
    checkAnswerBoxes() {
      if (this.task.format !== 1) {
        return;
      }

      for (let i = 0; i < this.task.test.questions.length; i += 1) {
        for (let j = 0; j < this.task.test.questions[i].answers.length; j += 1) {
          const qId = this.task.test.questions[i].id;
          const aId = this.task.test.questions[i].answers[j].id;
          const id = `#answer-${this.task.id}-${qId}-${aId}`;
          if (this.answerSelected(qId, aId)) {
            const el = this.$el.querySelector(id);
            el.checked = true;
          }
        }
      }
    },
  },
};
</script>

<style>
#student-board {
  margin: 10px;
}

#student-board > div {
  padding: 20px;
}

#open-answer {
  width: 100%;
}

.input-radio {
  margin-top: 0.1rem;
}

#task-info * {
  z-index: 1010;
}

#current-task {
  max-height: 600px;
  overflow-y: auto;
}

#chat-corner {
  position: fixed;
  bottom: 0;
  right: 0;
  z-index: 1000;
  padding: 0 !important;
}

.custom-checkbox .custom-control-input:checked ~ .custom-control-label::before {
  background-color: #00cec9 !important;
}

.custom-control-input {
  position: inherit;
}

#rejoin {
  margin-bottom: 20px;
  margin-right: 20px;
}
</style>
