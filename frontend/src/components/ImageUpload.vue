<template>
  <v-container class="py-8">
    <v-card class="mx-auto" max-width="800" elevation="4">
      <v-card-title class="text-h5 font-weight-bold primary--text">
        <v-icon large left color="primary">mdi-image-filter-center-focus</v-icon>
        AI Image Analysis System
      </v-card-title>
      
      <v-card-subtitle class="pl-3">
        <v-icon large left color="primary">mdi-image-filter</v-icon>
        <v-icon large left color="primary">mdi-image-filter</v-icon>
        Upload an image to process with our AI model
      </v-card-subtitle>
      
      <v-card-text>
        <v-row>
          <v-col cols="12">
            <v-file-input
              v-model="image"
              label="Choose an image file"
              accept="image/*"
              prepend-icon="mdi-camera"
              show-size
              outlined
              :rules="[v => !!v || 'Image is required']"
              :loading="isLoading"
              :disabled="isLoading"
              @change="previewImage"
            ></v-file-input>
          </v-col>
        </v-row>
        
        <v-row v-if="imagePreview">
          <v-col cols="12" class="text-center">
            <v-card flat>
              <v-card-title class="subtitle-1">Preview:</v-card-title>
              <v-img
                :src="imagePreview"
                max-height="300"
                contain
                class="grey lighten-2 rounded"
              ></v-img>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
      
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          large
          :loading="isLoading"
          :disabled="!image"
          @click="uploadImage"
        >
          <v-icon left>mdi-upload</v-icon>
          Process Image
        </v-btn>
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>
    
    <v-card v-if="result" class="mt-6 mx-auto" max-width="800" elevation="4">
      <v-card-title class="text-h6 success--text">
        <v-icon left color="success">mdi-check-circle</v-icon>
        Analysis Results
      </v-card-title>
      
      <v-card-text>
        <v-row>
          <v-col cols="12" md="6">
            <v-card outlined>
              <v-card-title class="subtitle-1">Original Image</v-card-title>
              <v-img
                :src="imagePreview"
                max-height="250"
                contain
                class="grey lighten-2"
              ></v-img>
            </v-card>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-card outlined>
              <v-card-title class="subtitle-1">Processed Result</v-card-title>
              <v-img
                v-if="resultImage"
                :src="resultImage"
                max-height="250"
                contain
                class="grey lighten-2"
              ></v-img>
              <v-card-text v-else>
                <pre class="result-json">{{ JSON.stringify(result, null, 2) }}</pre>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        
        <v-expansion-panels class="mt-4">
          <v-expansion-panel>
            <v-expansion-panel-header>
              Detailed Results
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <pre class="result-json">{{ JSON.stringify(result, null, 2) }}</pre>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-card-text>
    </v-card>
    
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="4000"
    >
      {{ snackbar.text }}
      <template v-slot:action="{ attrs }">
        <v-btn
          text
          v-bind="attrs"
          @click="snackbar.show = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      image: null,
      imagePreview: null,
      result: null,
      resultImage: null,
      isLoading: false,
      snackbar: {
        show: false,
        text: '',
        color: 'info'
      },
      apiBaseUrl: 'http://localhost:5000'
    };
  },
  mounted() {
    this.checkBackendConnection();
  },
  methods: {
    async checkBackendConnection() {
      try {
        await axios.get(`${this.apiBaseUrl}/health`, { timeout: 5000 });
      } catch (error) {
        console.warn("Backend health check failed:", error);
        this.showSnackbar('Warning: Backend server may not be reachable', 'warning');
      }
    },
    
    previewImage() {
      if (!this.image) {
        this.imagePreview = null;
        return;
      }
      
      const reader = new FileReader();
      reader.readAsDataURL(this.image);
      reader.onload = (e) => {
        this.imagePreview = e.target.result;
      };
    },
    
    async uploadImage() {
      if (!this.image) {
        this.showSnackbar('Please select an image first', 'warning');
        return;
      }
      
      this.isLoading = true;
      const formData = new FormData();
      formData.append('image', this.image);
      
      try {
        const response = await axios.post(`${this.apiBaseUrl}/upload`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          withCredentials: false, 
          timeout: 30000 
        });
        
        this.result = response.data;
        
        if (response.data.image_url) {
          this.resultImage = response.data.image_url;
        } else {
          this.resultImage = null;
        }
        
        this.showSnackbar('Image processed successfully!', 'success');
      } catch (error) {
        console.error("Error uploading image:", error);
        
        let errorMessage = 'Error processing image. ';
        
        if (error.response) {
          errorMessage += `Server responded with status ${error.response.status}`;
        } else if (error.request) {
          errorMessage += 'No response received from server. Check if the backend is running.';
        } else {
          errorMessage += error.message;
        }
        
        this.showSnackbar(errorMessage, 'error');
      } finally {
        this.isLoading = false;
      }
    },
    
    showSnackbar(text, color = 'info') {
      this.snackbar.text = text;
      this.snackbar.color = color;
      this.snackbar.show = true;
    }
  }
};
</script>

<style>
.result-json {
  background-color: #f0f0f0;
  padding: 8px;
  border-radius: 4px;
  max-height: 300px;
  overflow-y: auto;
  font-family: monospace;
  font-size: 14px;
}
</style>