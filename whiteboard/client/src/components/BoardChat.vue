<template>
  <div
    id="board-chat"
    class="card bg-default">
    <div class="card-header">
      <h6 class="mb-0">
        <button
          id="collapse-chat-btn"
          class="btn btn-link"
          type="button"
          data-toggle="collapse"
          data-target="#collapse-chat" >
          <font-awesome-icon
            icon="comments"
            size="2x" />
        </button>
      </h6>
    </div>
    <div
      id="collapse-chat"
      class="collapse show"
      data-parent="#collapse-chat-btn">
      <div
        id="board-chat-messages"
        class="card-body">
        <template
          v-for="msg in history">

          <BoardChatMsg
            v-if="!msg.joined"
            :key="msg.id"
            :msg="msg" />

          <div
            v-else
            :key="msg.id"
            class="col-sm-12 text-center">
            <small>{{ msg.from }} joined</small>
          </div>

        </template>
      </div>
      <div class="card-footer">
        <form @submit.prevent="sendMessage">
          <div class="input-group">
            <input
              id="board-chat-message-input"
              v-model="currentMessage"
              type="text"
              placeholder="Enter message..."
              class="form-control"
              autocomplete="off"
              @submit="sendMessage">
            <div
              id="board-chat-send"
              class="input-group-append"
              @click="sendMessage">
              <span class="input-group-text">
                <font-awesome-icon
                  icon="paper-plane"
                  size="1x" />
              </span>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import BoardChatMsg from '@/components/BoardChatMsg';

export default {
  name: 'BoardChat',
  components: { BoardChatMsg },
  props: {
    socket: {
      type: Object,
      default: null,
    },
    gId: { type: Number, default: 0 },
    cId: { type: Number, default: 0 },
  },
  data() {
    return {
      // socket: io(`${config.apiHost}/data`),
      sentMsgClass: 'sent',
      recievedMsgClass: 'recieved',
      currentMessage: '',
      history: [],
    };
  },
  computed: {
    me() {
      return `${this.$store.state.user.first_name} ${this.$store.state.user.last_name}`;
    },
    userId() {
      return this.$store.state.user.id;
    },
  },
  updated() {
    const chat = this.$el.querySelector('#board-chat-messages');
    chat.scrollTop = chat.scrollHeight;
  },
  mounted() {
    if (this.socket !== null) {
      const self = this;
      this.socket.on('message', (data) => {
        self.history.push(data);
      });
      this.socket.on('status', (data) => {
        if (data.senderId === self.userId) return;

        const now = new Date(Date.now);
        self.history.push({
          from: data.name,
          senderId: data.senderId,
          date: now.toLocaleTimeString(),
          message: '',
          joined: true,
          left: false,
        });
      });
      this.socket.on('left', (data) => {
        if (data.senderId === self.userId) return;

        const now = new Date(Date.now);
        self.history.push({
          from: data.name,
          senderId: data.senderId,
          date: now.toLocaleTimeString(),
          message: '',
          joined: false,
          left: true,
        });
      });
    } else {
      console.log('missing socket prop in BoardChat');
    }
  },
  beforeDestroy() {
    if (this.socket !== null) {
      this.socket.emit('left', { room: this.cId, name: this.me });
    } else {
      console.log('missing socket prop in BoardChat');
    }
  },
  methods: {
    sendMessage() {
      if (this.currentMessage === null || this.currentMessage.trim() === '') {
        return;
      }

      const now = new Date(Date.now);
      if (this.socket !== null) {
        this.socket.emit('text', {
          room: this.cId,
          data: {
            from: this.me,
            senderId: this.userId,
            date: now.toLocaleTimeString(),
            message: this.currentMessage.trim(),
          },
        });
      } else {
        console.log('missing socket prop in BoardChat');
      }

      this.currentMessage = '';

      this.$el.querySelector('#board-chat-message-input').focus();
    },
  },
};
</script>

<style scoped>
#board-chat {
  padding: 0;
  margin-right: 20px;
  margin-bottom: 20px;
  max-width: 300px;
  max-height: 600px;
}

#board-chat,
#board-chat * {
  z-index: 100;
}

#board-chat div.card-footer {
  padding: 5px;
}

#board-chat div.card-header {
  padding: 10px;
}

#board-chat div.card-header button {
  color: #00b894;
}

#board-chat-messages {
  max-height: 400px;
  overflow-y: scroll;
}

#board-chat-message-input {
  border-color: #ced4da !important;
  -webkit-box-shadow: none;
  box-shadow: none;
}
</style>
