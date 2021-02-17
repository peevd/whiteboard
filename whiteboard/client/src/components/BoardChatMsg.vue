<template>
  <div
    :class="classObject"
    class="row mb-2 message">
    <div
      v-if="!myMessage"
      :title="msg.from"
      class="col-sm-auto">
      <font-awesome-icon
        icon="user-circle"
        size="1x" />
    </div>
    <div class="col-sm-auto">
      {{ msg.message }}
    </div>
    <div
      v-if="myMessage"
      :title="msg.from"
      class="col-sm-auto">
      <font-awesome-icon
        icon="user-circle"
        size="1x" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'BoardChatMsg',
  props: {
    msg: {
      type: Object,
      default() {
        return {
          from: '',
          date: '',
          message: '',
          joined: false,
        };
      },
    },
  },
  computed: {
    myMessage() {
      return this.msg.senderId === this.userId;
    },
    classObject() {
      return {
        sent: this.myMessage,
        recieved: !this.myMessage,
      };
    },
    me() {
      return `${this.$store.state.user.first_name} ${this.$store.state.user.last_name}`;
    },
    userId() {
      return this.$store.state.user.id;
    },
  },
};
</script>

<style scoped>
.message > div {
  padding: 10px;
  border: 1px solid rgba(0, 0, 0, 0.25);
  max-width: 200px;
  word-wrap: break-word;
  border-radius: 0.25rem;
}

.recieved {
  -ms-flex-pack: start !important;
  -webkit-box-pack: start !important;
  justify-content: flex-start !important;
}

.recieved > div {
  background-color: #f5f5f5 !important;
}

.sent {
  -ms-flex-pack: end !important;
  -webkit-box-pack: end !important;
  justify-content: flex-end !important;
}

.sent > div {
  background-color: #00b894 !important;
}

.message > div:nth-of-type(1) {
  border-right: none;
  border-radius: 0.25rem 0 0 0.25rem;
}

.message > div:nth-of-type(2) {
  border-left: none;
  border-radius: 0 0.25rem 0.25rem 0;
}
</style>
