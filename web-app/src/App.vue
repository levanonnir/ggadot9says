<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-img
        class="shrink me-2"
        contain
        :src="require('../public/img/arm_robot.png')"
        transition="scale-transition"
        width="40"
      />
      <v-spacer></v-spacer>
      <v-app-bar-title style="text-overflow: clip;"> GGadot9 Says </v-app-bar-title>
      <v-spacer></v-spacer>
      <v-img
        class="shrink ms-2"
        contain
        :src="require('../public/img/RobotNXT.png')"
        transition="scale-transition"
        width="40"
      />
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <MainContent />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import MainContent from "./components/MainContent";
// import { functions } from './firebase';
// import {  httpsCallable } from 'firebase/functions';
    
export default {
  name: "App",
  components: {
    MainContent,
  },

  data: () => ({
    //
  }),
  // methods: {
  //   startWebSocket() {
  //     const startWebSocketFunction = httpsCallable(functions, "startWebSocket");
  //     try {
  //       startWebSocketFunction()
  //     }
  //   }
  // },
  // created() {
  //   this.startWebSocket()
  // }
};
</script>
