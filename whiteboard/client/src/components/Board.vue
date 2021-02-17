<template>
  <div
    id="board"
    class="row align-self-stretch">

    <div class="col-sm-3">

      <div class="row">

        <div
          ref="tasksCol"
          class="col-sm-12">

          <div
            v-show="tasks.length === 0"
            id="tasks-missing"
            class="card bg-default">

            <div class="card-body">
              <h5 class="mb-0">No tasks found</h5>
            </div>

          </div>

          <div
            v-show="tasks.length !== 0"
            class="row">
            <div class="col">
              <div class="card bg-default shadow">
                <div class="card-header p-0">
                  <button
                    id="tasks-toggle"
                    class="btn w-100"
                    title="Toggle tasks"
                    @click="toggleTasks">
                    <custom-icon
                      icon="task"
                      size="2x" />
                    Tasks
                  </button>
                </div>
                <div class="card-body p-0">
                  <div
                    v-show="displayTasks"
                    id="tasks-list"
                    ref="tasksList"
                    class="accordion bg-default">

                    <div
                      v-for="task in tasks"
                      :key="task.id"
                      class="card bg-default">

                      <div
                        :class="[ task.id === currentTask ? 'bg-success' : 'bg-default' ]"
                        class="card-header border-bottom-0 btn"
                        href="#"
                        @click="showTask(task.id)">

                        <h5 class="mb-0 d-flex justify-content-between">
                          {{ task.name }}
                          <a
                            v-if="task.id === openTask && task.id !== currentTask"
                            href="#"
                            class="badge badge-secondary align-self-center"
                            @click.prevent="sendTask(task.id)">Send</a>
                          <span
                            v-if="task.id === currentTask"
                            class="badge badge-secondary align-self-center">
                            <font-awesome-icon
                              icon="check"
                              size="xs" />
                          </span>

                        </h5>

                      </div>

                      <div
                        :id="'task-' + task.id"
                        :class="{ show: task.id === openTask }"
                        class="collapse">

                        <div
                          class="card-body ProseMirror"
                          v-html="task.description" />

                      </div>

                    </div>

                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>

      </div>

      <div class="row mt-4">

        <div class="col">
          <PPTPresentation :c-id="cId" />
        </div>

      </div>

    </div>

    <div class="col-sm-9">

      <BoardCanvas
        :c-id="cId"
        :g-id="gId"
        :socket="socket" />

    </div>

    <div
      id="chat-corner"
      class="row align-items-end">
      <button
        v-if="stream"
        id="mute"
        class="btn"
        @click="muteMic">
        <custom-icon
          v-if="muted"
          icon="micMuted"
          size="2x" />
        <custom-icon
          v-else
          icon="mic"
          size="2x" />
      </button>

      <button
        v-if="peer && peer.disconnected"
        id="rejoin"
        class="btn"
        title="Rejoin audio conference"
        @click="rejoin">
        <custom-icon
          icon="phone"
          size="2x" />
      </button>

      <BoardChat
        :c-id="cId"
        :g-id="gId"
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
import PPTPresentation from '@/components/PPTPresentation';

export default {
  name: 'Board',
  components: {
    BoardCanvas,
    BoardChat,
    PPTPresentation,
  },
  data() {
    return {
      socket: io(`${config.hostname}/data`, {
        path: '/whiteboard.io',
      }),
      peer: null,
      openTask: 0,
      muted: false,
      stream: null,
      displayTasks: true,
    };
  },
  computed: {
    board() {
      return this.$store.state.currentBoard;
    },
    currentTask() {
      return this.$store.state.currentBoard.task_id;
    },
    tasks() {
      return this.$store.state.currentTasks;
    },
    cId() {
      return Number(this.$route.params.cId);
    },
    course() {
      return this.$store.state.currentCourse;
    },
    gId() {
      return Number(this.$route.params.gId);
    },
    group() {
      return this.$store.state.currentGroup;
    },
    taskClasses(id) {
      return {
        'bg-success': id === this.currentTask,
      };
    },
    me() {
      return `${this.$store.state.user.first_name} ${this.$store.state.user.last_name}`;
    },
    userId() {
      return this.$store.state.user.id;
    },
  },
  created() {
    window.addEventListener('resize', this.onResize);

    this.$store.dispatch('fetchCourse', this.cId)
      .then(() => {
        this.$store.dispatch('fetchGroup', { cId: this.cId, gId: this.gId })
          .then(() => {
            this.$store.dispatch('setBreadcrumbs', [
              {
                name: this.course.name,
                href: `/my-courses/${this.course.id}`,
              },
              {
                name: this.group.name,
                href: `/my-courses/${this.course.id}/groups/${this.group.id}`,
              },
            ]);
          });
      });
    this.$store.dispatch('fetchTasks', this.cId);
    this.$store.dispatch('fetchBoard', { cId: this.cId, gId: this.gId });
    this.$store.dispatch('fetchBoardData', { cId: this.cId, gId: this.gId });

    this.socket.emit('joined', { room: this.cId, data: { name: this.me, senderId: this.userId } });

    const peerId = `${this.cId}-${this.gId}`;

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
      switch (err.type) {
        case 'server-error':
          this.peerError = true;
          this.$toastr.error('Failed to connect to server: server error', 'Conference call error');
          break;
        case 'network':
          this.peerError = true;
          this.$toastr.error('Failed to connect to server: network error', 'Conference call error');
          break;
        case 'unavailable-id':
          this.$toastr.error('Board is already open somewhere', 'Conference call error');
          break;
        default:
          this.$toastr.error(err.type, 'Conference call error');
      }
    });

    this.peer.on('call', (call) => {
      if (this.stream) {
        this.answerCall(call, this.stream);
      } else {
        navigator.mediaDevices.getUserMedia({ video: false, audio: true })
          .then((stream) => {
            this.stream = stream;
            this.answerCall(call, this.stream);
          })
          .catch(err => this.$toastr.error(err, 'MediaDevices error'));
      }
    });
  },
  mounted() {
    this.$nextTick(() => {
      this.onResize();
    });
  },
  beforeDestroy() {
    this.socket.disconnect();
    this.peer.destroy();
  },
  methods: {
    showTask(id) {
      if (id !== this.openTask) {
        this.openTask = Number(id);
      } else {
        this.openTask = 0;
      }
    },
    sendTask(id) {
      this.$store.dispatch('updateBoard', { cId: this.cId, gId: this.gId, payload: { task_id: id } });
      this.socket.emit('task_id', { room: this.cId, data: { cId: this.cId, tId: id } });
    },
    answerCall(call, stream) {
      call.answer(stream);
      call.on('error', err => this.$toastr.error(err, 'Call error'));
    },
    muteMic() {
      if (this.stream !== null) {
        this.muted = !this.muted;
        this.stream.getAudioTracks()[0].enabled = !this.muted;
      }
    },
    toggleTasks() {
      this.displayTasks = !this.displayTasks;
    },
    rejoin() {
      if (this.peer && !this.peer.destroyed) {
        this.peer.reconnect();
      }
    },
    onResize() {
      const height = document.documentElement.clientHeight;
      const tasksColEl = this.$refs.tasksCol;
      const tasksListEl = this.$refs.tasksList;
      if (tasksListEl) {
        const rect = tasksColEl.getBoundingClientRect();
        tasksListEl.style.maxHeight = `${height - rect.top - 200}px`;
      }
    },
  },
};
</script>

<style>
#board {
  margin: 10px;
}

#board > div {
  padding: 20px;
}

#tasks-list {
  max-height: 600px;
  overflow-y: auto;
}

#tasks-list *,
#tasks-missing * {
  z-index: 100;
}

.list-group-item {
  background-color: inherit;
}

#tasks-list .btn-link {
  color: #2c3e50 !important;
  font-weight: bold;
}

#tasks-list .bg-success .btn-link {
  color: #fff !important;
}

#tasks-list .btn-link .badge {
  color: #fff !important;
  padding-top: 0.3rem;
}

#chat-corner {
  position: fixed;
  bottom: 0;
  right: 0;
  z-index: 1000;
  padding: 0 !important;
}

#mute,
#rejoin {
  margin-bottom: 20px;
  margin-right: 20px;
}

#tasks-toggle {
  position: relative;
  z-index: 100;
}
</style>
