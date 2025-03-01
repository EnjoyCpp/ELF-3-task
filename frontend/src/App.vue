<template>
  <v-app>
    <v-app-bar color="primary" dark app>
      <v-app-bar-title>AI Image Processing</v-app-bar-title>
    </v-app-bar>
    <v-main>
      <image-upload></image-upload>
    </v-main>
    <v-footer app>
      <span>&copy; {{ new Date().getFullYear() }} - ND3. Užduotis - AI Image Processing</span>
    </v-footer>
  </v-app>
</template>

<script>
import ImageUpload from './components/ImageUpload.vue';

export default {
  name: 'App',
  components: {
    ImageUpload,
  },
};
</script>

<style>
.v-application {
  background-color: #f5f5f5;
}
</style>