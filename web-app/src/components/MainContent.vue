<template>
  <v-container fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" md="6">
        <v-card v-if="robolego">
          <v-row align="center" justify="center">
            <v-col cols="6">
              <div class="text-overline">{{ robolegoName }}</div>
              <div class="text-overline" :class="robolegoStatusColor">
                {{ robolegoStatus }}
              </div>
            </v-col>
            <v-col cols="6"> </v-col>
          </v-row>
          <v-row align="center" justify="center"> </v-row>
        </v-card>
        <v-card v-else>
          <v-row align="center" justify="center">
            <v-col cols="10">
              <div class="text-overline">
                Status:
                <span :class="robolegoStatusColor"> {{ robolegoStatus }}</span>
              </div>
              <div class="text-h6">RoboLego Controller</div>
            </v-col>
            <v-col cols="10">
              <v-text-field
                v-model="robolegoName"
                label="Robot's Name"
                :disabled="robolegoConnecting"
              ></v-text-field>
            </v-col>
            <v-col cols="10">
              <v-btn
                block
                @click="connectRobolego"
                :disabled="robolegoConnecting"
                >Connect</v-btn
              >
            </v-col>
          </v-row>
          <!-- <v-card-text>text</v-card-text>
          <v-card-actions>text</v-card-actions> -->
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card v-if="scorp">
          <v-card-text>text</v-card-text>
          <v-card-actions>text</v-card-actions>
        </v-card>
        <v-card v-else>
          <v-card-text>text</v-card-text>
          <v-card-actions>text</v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        {{ message }}
      </v-col>
      <v-col>
        <v-btn @click.prevent="sendMessage"> send message </v-btn>
      </v-col>
    </v-row>
    <v-snackbar v-model="snackbar">
      {{ snackbarText }}

      <template v-slot:action="{ attrs }">
        <v-btn color="info" text v-bind="attrs" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      ws: new WebSocket("ws://localhost:3000/"),
      message: "",
      robolego: false,
      robolegoName: "",
      robolegoConnecting: false,
      color: "",
      scorp: false,
      scorpStatus: "offline",
      movementDirections: ["forward", "backward", "left", "right"],
      snackbar: false,
      snackbarText: ""
    };
  },
  created() {
    try {
      this.ws.onmessage = ({ data }) => {
        this.message = data;
        const dataParts = data.split(":");
        switch (dataParts[0]) {
          case "lego":
            switch (dataParts[1]) {
              case "status":
                switch (dataParts[2]) {
                  case "offline":
                    this.robolegoConnectionFail();
                    break;
                  case "online":
                    this.robolegoConnectionSuccessful();
                    break;
                }
                break;
              case "color":
                this.color = dataParts[2];
                break;
            }
            break;
          case "scorp":
            break;
        }
      };
    } catch (err) {
      console.log(err);
    }
  },
  methods: {
    sendMessage() {
      this.ws.send("lego::dothis");
    },
    connectRobolego() {
      this.robolegoConnecting = true;
      const connectMessage = `lego:connect:${this.robolegoName}`;
      this.ws.send(connectMessage);
    },
    robolegoConnectionSuccessful() {
      this.robolegoConnecting = false;
      this.robolego = true;
      this.snackbarText = `Connected to ${this.robolegoName}`;
      this.snackbar = true;
    },
    robolegoConnectionFail() {
      this.robolegoConnecting = false;
      this.robolego = false;
      this.snackbarText = `Failed connecting to ${this.robolegoName}`;
      this.snackbar = true;
    }
  },
  computed: {
    robolegoStatus() {
      return this.robolego ? "online" : "offline";
    },
    robolegoStatusColor() {
      return this.robolego ? "succuess--text" : "error--text";
    }
  }
};
</script>
