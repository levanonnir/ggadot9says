<template>
  <div>
    <v-row align="center" justify="center" class="mt-2">
      <!-- ROBOLEGO -->
      <v-col cols="12" md="6" class="mb-4">
        <!-- AFTER CONNECTION -->
        <v-card v-if="robolegoConnected">
          <v-row align="center" justify="space-around">
            <v-col cols="5">
              <div class="text-overline">{{ robolegoName }}</div>
            </v-col>
            <v-col cols="5">
              <div :class="`text-overline text-end ${robolegoStatusColor}`">
                {{ robolego }}
              </div>
            </v-col>
          </v-row>
          <v-row align="center" justify="space-around">
            <v-col class="text-center">
              <v-btn
                icon
                x-large
                @mousedown="robolegoDrive('forward')"
                @mouseup="robolegoStop"
              >
                <v-icon>mdi-chevron-up</v-icon>
              </v-btn>
            </v-col>
          </v-row>
          <v-row align="center" justify="space-around">
            <v-col class="text-center">
              <v-btn
                icon
                x-large
                @mousedown="robolegoDrive('turn_left')"
                @mouseup="robolegoStop"
              >
                <v-icon>mdi-chevron-left</v-icon>
              </v-btn>
            </v-col>
            <v-col class="text-center">
              <v-btn
                icon
                x-large
                :color="color"
                @mousedown="robolegoSampleColor"
              >
                <v-icon>mdi-eyedropper-variant</v-icon>
              </v-btn>
            </v-col>
            <v-col class="text-center">
              <v-btn
                icon
                x-large
                @mousedown="robolegoDrive('turn_right')"
                @mouseup="robolegoStop"
              >
                <v-icon>mdi-chevron-right</v-icon>
              </v-btn>
            </v-col>
          </v-row>
          <v-row align="center" justify="space-around">
            <v-col class="text-center">
              <v-btn
                icon
                x-large
                @mousedown="robolegoDrive('backward')"
                @mouseup="robolegoStop"
              >
                <v-icon>mdi-chevron-down</v-icon>
              </v-btn>
            </v-col>
          </v-row>
          <v-row align="center" justify="center">
            <v-col cols="10">
              <v-slider
                v-model="power"
                thumb-label
                label="Power"
                min="0"
                max="100"
              ></v-slider>
            </v-col>
          </v-row>
        </v-card>

        <!-- BEFORE CONNECTION -->
        <v-card v-else>
          <v-row align="center" justify="center">
            <v-col cols="10">
              <div class="text-overline">
                Status:
                <span :class="robolegoStatusColor"> {{ robolego }}</span>
              </div>
              <div class="text-h6">RoboLego Controller</div>
            </v-col>
            <v-col cols="10">
              <v-text-field
                v-model="robolegoName"
                label="Robot's Name"
                :disabled="robolegoFrozen"
              ></v-text-field>
            </v-col>
            <v-col cols="10">
              <v-btn block @click="connectRobolego" :loading="robolegoFrozen"
                >Connect</v-btn
              >
            </v-col>
          </v-row>
        </v-card>
      </v-col>

      <!-- SCORPBOT -->
      <v-col cols="12" md="6">
        <v-card>
          <v-row align="center" justify="center">
            <v-col cols="10">
              <div class="text-overline">
                Status:
                <span :class="scorpStatusColor"> {{ scorp }}</span>
              </div>
              <div class="text-h6">ScorpBot Controller</div>
            </v-col>
            <v-col v-if="!scorpConnected" cols="10">
              <v-btn block @click="connectScorp" :loading="scorpConnecting"
                >Connect</v-btn
              >
            </v-col>
            <v-col v-if="scorpConnected" cols="5">
              <v-btn
                @click="scorpPerfromAction('home')"
                :disabled="scorpDisabled"
              >
                <v-icon>mdi-home</v-icon>
                Home
              </v-btn>
            </v-col>
            <v-col v-if="scorpConnected" cols="5" class="text-end">
              <v-btn
                @click="scorpPerfromAction('calibrate')"
                :disabled="scorpDisabled"
                >Calibrate</v-btn
              >
            </v-col>
            <v-col v-if="scorpConnected" cols="10">
              <v-btn
                v-for="color in colors"
                :key="color"
                @click="scorpPerfromAction(color)"
                :color="color"
                class="me-1"
                :disabled="scorpDisabled"
              >
                {{ color }}
              </v-btn>
            </v-col>
            <v-col v-if="scorpConnected" cols="10">
              <v-text-field
                v-model="point"
                type="number"
                label="Move to point..."
                :disabled="scorpDisabled"
                
              ></v-text-field>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    <v-row align="center">
      <!-- <v-col>
        <div class="text-overline">
          Redis Server:
          <span :class="redisServerColor">
            {{ redisServer }}
          </span>
        </div>
      </v-col> -->
      <!-- <v-col>
        <v-btn
          @click.prevent="pingServer"
          block
          :disabled="pingingRedisServer"
          :loading="pingingRedisServer"
        >
          ping
        </v-btn>
      </v-col> -->
    </v-row>
    <v-snackbar v-model="snackbar">
      {{ snackbarText }}

      <template v-slot:action="{ attrs }">
        <v-btn color="info" text v-bind="attrs" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
export default {
  data() {
    return {
      ws: null,
      redisConnection: false,
      pingingRedisServer: false,
      robolego: "offline",
      robolegoConnecting: false,
      robolegoName: "",
      robolegoSampling: false,
      power: 30,
      color: "",
      colors: [],
      scorp: "offline",
      number: 0,
      scorpConnecting: false,
      movementDirections: [
        "forward",
        "backward",
        "turn_left",
        "turn_right",
        "stop"
      ],
      snackbar: false,
      snackbarText: ""
    };
  },
  created() {
    document.title = "GGadot9 Says - Group 7";
    this.ws = new WebSocket("ws://localhost:3000/");
    this.ws.onopen = () => {
      this.pingServer();
    };
    try {
      this.ws.onmessage = ({ data }) => {
        // this.redisConnection = true;
        this.message = data;
        const dataParts = data.split(":");
        switch (dataParts[0]) {
          case this.robolegoName:
            switch (dataParts[1]) {
              case "status":
                this.robolego = dataParts[2];
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
                if (!["nothing", "black"].includes(dataParts[2])) {
                  this.color = dataParts[2];
                  this.colors.push(this.color);
                }
                this.robolegoSampling = false;
                this.snackbarText = `${this.robolegoName} found ${this.color}`;
                this.snackbar = true;
                break;
            }
            break;
          case "scorp":
            switch (dataParts[1]) {
              case "status":
                this.scorp = dataParts[2];
                break;
            }
            break;
          case "server":
            switch (dataParts[1]) {
              case "connection":
                this.redisConnection = dataParts[2] == "ping";
                this.pingingRedisServer = false;
                break;
            }
        }
      };
    } catch (err) {
      this.redisConnection = false;
      console.log(err);
      this.snackbarText = err;
      this.snackbar = true;
    }
  },
  methods: {
    initWebSocket() {
      const path =
        process.env.NODE_ENV === "production"
          ? "ggadot9says.web.app"
          : "localhost";
      return new WebSocket(`ws://${path}:3000/`);
    },
    pingServer() {
      this.redisConnection = false;
      try {
        // this.ws = this.initWebSocket();
        this.pingingRedisServer = true;
        this.ws.send("server:connection:ping");
      } catch (error) {
        this.pingingRedisServer = false;
        this.snackbarText = error.message;
        this.snackbar = true;
      }
    },
    connectRobolego() {
      try {
        this.robolegoConnecting = true;
        const connectMessage = `lego:connect:${this.robolegoName}`;
        this.ws.send(connectMessage);
      } catch (error) {
        this.robolegoConnecting = false;
        this.snackbarText = error.message;
        this.snackbar = true;
      }
    },
    robolegoConnectionSuccessful() {
      this.robolegoConnecting = false;
      this.snackbarText = `Connected to ${this.robolegoName}`;
      this.snackbar = true;
    },
    robolegoConnectionFail() {
      this.robolegoConnecting = false;
      this.snackbarText = `Failed connecting to ${this.robolegoName}`;
      this.snackbar = true;
    },
    connectScorp() {
      try {
        this.scorp = "connecting...";
        const connectMessage = "scorp:action:connect";
        this.ws.send(connectMessage);
      } catch (error) {
        this.robolegoConnecting = false;
        this.snackbarText = error.message;
        this.snackbar = true;
      }
    },
    scorpConnectionSuccessful() {
      this.scorp = "online";
      this.snackbarText = `Connected to ScorpBot`;
      this.snackbar = true;
    },
    scorpConnectionFail() {
      this.scorp = "offline";
      this.snackbarText = `Failed connecting to ScorpBot`;
      this.snackbar = true;
    },
    scorpPerfromAction(action) {
      // this.scorp = "Moving...";
      const actionMessage = `scorp:action:${action}`;
      this.ws.send(actionMessage);
    },
    robolegoDrive(direction) {
      if (this.movementDirections.includes(direction)) {
        const driveMessage = `${this.robolegoName}:${direction}:${this.power}`;
        this.ws.send(driveMessage);
      } else {
        this.snackbarText = "Wrong direction attempted. Process prevented.";
        this.snackbar = true;
      }
    },
    robolegoStop() {
      const stopMessage = `${this.robolegoName}:stop:${this.power}`;
      this.ws.send(stopMessage);
    },
    robolegoSampleColor() {
      const sampleMessage = `${this.robolegoName}:sample_color:${this.power}`;
      this.ws.send(sampleMessage);
      this.snackbarText = "Sampling color...";
      this.snackbar = true;
    }
  },
  computed: {
    redisServer() {
      return this.redisConnection ? "Online" : "Offline";
    },
    redisServerColor() {
      return this.redisConnection ? "success--text" : "error--text";
    },
    robolegoConnected() {
      return this.robolego != "offline";
    },
    robolegoStatusColor() {
      switch (this.robolego) {
        case "online":
          return "success--text";
        case "offline":
          return "error--text";
        default:
          return "info--text";
      }
    },
    robolegoFrozen() {
      return this.robolegoConnecting || this.robolegoSampling;
    },
    robolegoMoving() {
      return this.robolego == "moving";
    },
    scorpConnected() {
      return this.scorp != "offline";
    },
    scorpStatusColor() {
      switch (this.scorp) {
        case "online":
          return "success--text";
        case "offline":
          return "error--text";
        default:
          return "info--text";
      }
    },
    scorpDisabled() {
      return this.scorp != "online";
    }
  }
};
</script>
