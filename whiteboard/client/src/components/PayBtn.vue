<template>
  <div>
    <vue-stripe-checkout
      ref="checkoutRef"
      :image="image"
      :name="name"
      :description="description"
      :currency="currency"
      :amount="amount"
      :allow-remember-me="false"
      :panel-label="panelLabel"
      @done="done"
      @opened="opened"
      @closed="closed"
      @canceled="canceled" />
    <button
      class="btn btn-success"
      @click="checkout">Join</button>
  </div>
</template>

<script>
export default {
  props: {
    cId: { type: Number, default: 0 },
    gId: { type: Number, default: 0 },
    courseName: { type: String, default: '' },
    amount: { type: Number, default: 0 },
  },
  data() {
    return {
      image: 'https://i.imgur.com/HhqxVCW.jpg',
      currency: 'USD',
      description: '',
      panelLabel: 'Pay {{amount}}',
      tokenFromPromise: {},
      tokenFromEvent: {},
    };
  },
  computed: {
    name() {
      return `Sign up for ${this.courseName}!`;
    },
  },
  methods: {
    async checkout() {
      this.tokenFromPromise = await this.$refs.checkoutRef.open();
    },
    done(token) {
      this.tokenFromEvent = token;
      this.submit(token.token);
    },
    opened() {
      // do stuff
    },
    closed() {
      // do stuff
    },
    canceled() {
      // do stuff
    },
    submit(token) {
      this.$emit('loading');
      this.$store.dispatch('submitPayment', {
        c_id: this.cId,
        g_id: this.gId,
        stripeToken: token.id,
        email: token.email,
      }).then(() => (this.$emit('done')))
        .catch(() => (this.$emit('done')));
    },
  },
};
</script>
