<template>
  <v-container>
    <v-row>
      <v-col>
        {{ message }}
      </v-col>
      <v-col>
        <v-btn @click.prevent="sendMessage"> send message </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      ws: new WebSocket("ws://localhost:3000/"),
      message: ""
    };
  },
  created() {
    try {
      this.ws.onmessage = ({ data }) => {
        this.message = data;
      };
    } catch (err) {
      console.log(err);
    }
  },
  methods: {
    sendMessage() {
      this.ws.send("lego::dothis");
    }
  }
};
</script>
