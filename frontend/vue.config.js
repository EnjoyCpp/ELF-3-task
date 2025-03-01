const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,

  devServer: {
    host: '0.0.0.0',  // Allows connections from Docker
    port: 8080,       // Match the port in docker-compose.yml
    watchFiles: ['src/**/*'], // Ensures hot-reloading works inside Docker
    allowedHosts: 'all', // Allows external access
  }
});
