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
                :disabled="robolegoMoving"
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
                :disabled="robolegoMoving"
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
                :disabled="robolegoMoving"
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
                :disabled="robolegoMoving"
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
                :disabled="robolegoMoving"
              >
                <v-icon>mdi-chevron-down</v-icon>
              </v-btn>
            </v-col>
          </v-row>
          <v-row align="center" justify="center">
            <v-col cols="10">
              <v-slider
                v-model="power"
                @change="robolegoChangePower"
                thumb-label
                label="Power"
                min="0"
                max="100"
                :disabled="robolegoMoving"
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
              <v-btn block @click="connectRobolego" :disabled="robolegoFrozen"
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
              <v-btn block @click="connectScorp">Connect</v-btn>
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
              <v-btn :disabled="scorpDisabled">Calibrate</v-btn>
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
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    <v-row align="center">
      <v-col>
        <div class="text-overline">
          Redis Server:
          <span :class="redisServerColor">
            {{ redisServer }}
          </span>
        </div>
      </v-col>
      <v-col>
        <v-btn @click.prevent="checkServer" block :disabled="checkRedisServer">
          Check
        </v-btn>
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
  </div>
</template>

<script>
export default {
  data() {
    return {
      ws: new WebSocket("ws://localhost:3000/"),
      redisConnection: false,
      checkRedisServer: false,
      robolego: "offline",
      robolegoName: "",
      robolegoConnecting: false,
      robolegoSampling: false,
      power: 30,
      color: "",
      colors: [],
      scorp: "offline",
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
    try {
      this.ws.onmessage = ({ data }) => {
        this.redisConnection = true;
        this.message = data;
        const dataParts = data.split(":");
        switch (dataParts[0]) {
          case this.robolegoName:
            switch (dataParts[1]) {
              case "status":
                this.robolego = dataParts[2]
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
                if (dataParts[2] != "nothing") {
                  this.color = dataParts[2];
                  this.colors.concat(this.color);
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
                this.redisConnection = dataParts[2];
                this.checkRedisServer = false;
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
    checkServer() {
      this.checkRedisServer = true;
      this.ws.send("server:connection:check");
    },
    connectRobolego() {
      this.robolegoConnecting = true;
      const connectMessage = `lego:connect:${this.robolegoName}`;
      this.ws.send(connectMessage);
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
      this.scorp = "connecting...";
      const connectMessage = "scorp:action:connect";
      this.ws.send(connectMessage);
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
      this.scorp = "Moving...";
      const actionMessage = `scorp:action:${action}`;
      this.ws.send(actionMessage);
    },
    robolegoDrive(direction) {
      if (direction in this.movementDirections) {
        const driveMessage = `${robolegoName}:${direction}:${this.robolegoName}`;
        this.ws.send(driveMessage);
      } else {
        this.snackbarText = "Wrong direction attempted. Process prevented.";
        this.snackbar = true;
      }
    },
    robolegoStop() {
      const stopMessage = `${robolegoName}:stop:${this.robolegoName}`;
      this.ws.send(stopMessage);
    },
    robolegoSampleColor() {
      const sampleMessage = `${robolegoName}:sample_color:${this.robolegoName}`;
      this.ws.send(sampleMessage);
      this.snackbarText = "Sampling color...";
      this.snackbar = true;
    },
    robolegoChangePower() {
      const powerMessage = `${robolegoName}:power_${this.power}:${this.robolegoName}`;
      this.ws.send(powerMessage);
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
      return this.robolego == 'moving'
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
