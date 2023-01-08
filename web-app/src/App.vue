<template>
  <v-app>
    <v-app-bar app color="primary" dark> </v-app-bar>

    <v-main>
      <MainContent />
    </v-main>
  </v-app>
</template>

<script>
import MainContent from "./components/MainContent";

export default {
  name: "App",

  components: {
    MainContent
  },

  data: () => ({
    //
  })
};
</script>
