<template>
  <div class="app">
    <header class="app-header">
      <h2 class="header-title">FastAPI Agmin</h2>
      <select 
        v-model="selectedModel" 
        class="model-select"
        @change="handleModelChange"
      >
        <option value="__diagram__">Database Diagram</option>
        <option disabled>────────────</option>
        <option v-for="model in metadataStore.models" :key="model" :value="model">
          {{ model }}
        </option>
      </select>
    </header>
    <div class="main-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useMetadataStore } from './stores/metadata'

const router = useRouter()
const route = useRoute()
const metadataStore = useMetadataStore()
const selectedModel = ref('')

const handleModelChange = () => {
  if (selectedModel.value === '__diagram__' || !selectedModel.value) {
    router.push('/')
  } else {
    router.push(`/model/${selectedModel.value}`)
  }
}

// Load metadata when the component mounts
onMounted(async () => {
  await metadataStore.fetchMetadata()
  // Set initial model from route if present
  if (route.params.modelName) {
    selectedModel.value = route.params.modelName as string
  }
})

// Watch for route changes
watch(() => route.params.modelName, (newModel) => {
  if (newModel) {
    selectedModel.value = newModel as string
  } else {
    selectedModel.value = ''
  }
})

// Watch for model selection changes
watch(selectedModel, (newModel) => {
  if (newModel && !metadataStore.metadata) {
    metadataStore.fetchMetadata()
  }
})
</script>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
}

.app-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 4px 12px;
  background-color: #f5f5f5;
  border-bottom: 1px solid #ddd;
  height: 28px;
  width: 100%;
  box-sizing: border-box;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-title {
  margin: 0;
  font-size: 1em;
  color: #333;
  font-weight: 600;
  letter-spacing: 1px;
}

.model-select {
  width: 220px;
  max-width: 100%;
  padding: 4px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1em;
  background: white;
  box-sizing: border-box;
}

.main-content {
  flex: 1;
  overflow: auto;
  width: 100%;
}
</style>
