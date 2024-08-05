<template>
  <div :id="'drop-area-' + id"
       class="mt-2 flex justify-center rounded-lg border border-dashed border-gray-900/25 px-6 py-8"
       @dragover.prevent="preventDefault"
       @dragenter.prevent="preventDefault"
       @drop.prevent="handleDrop">
    <div class="text-center">
      <template v-if="fileType === 'image'">
        <template v-if="value">
          <div class="mx-auto w-14 h-14 rounded-lg mb-4"
               :style="'background-image: url(\'https://imagedelivery.net/MUP9cvwIiXaVOmbyPlpx4w/' + value + '/public\'); background-size: cover, cover;'">
            <XCircleIcon @click="removeImage" class="h-6 w-6 ml-auto text-red-500 bg-red-800 rounded-full cursor-pointer" aria-hidden="true" />
          </div>
        </template>
        <template v-else>
          <PhotoIcon class="mx-auto h-12 w-12 text-gray-300 mb-4" aria-hidden="true" />
        </template>
      </template>
      <template v-else>
        <template v-if="value">
          <DocumentTextIcon class="mx-auto h-12 w-12 text-gray-300 mb-4" aria-hidden="true" />
          <span class="mx-auto text-gray-300 text-xs">{{ value }}</span>
        </template>
        <template v-else>
          <DocumentTextIcon class="mx-auto h-12 w-12 text-gray-300 mb-4" aria-hidden="true" />
        </template>
      </template>
      <div class="flex text-sm leading-6 text-gray-600">
        <label :for="'file-upload-' + id" class="relative cursor-pointer rounded-md bg-white font-semibold text-primary-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-primary-600 focus-within:ring-offset-2 hover:text-primary-500">
          <span>Upload a file</span>
          <input :id="'file-upload-' + id" :ref="'file-upload-' + id" name="file-upload" type="file" class="sr-only" @change="handleFileInput"/>
        </label>
        <p class="pl-1">or drag and drop</p>
      </div>
      <p class="text-xs leading-5 text-gray-600">{{ requirements || 'PNG, JPG, GIF up to 10MB' }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { PhotoIcon, XCircleIcon, DocumentTextIcon } from "@heroicons/vue/20/solid";

export default {
  name: "FileDrop",
  components: { PhotoIcon, XCircleIcon, DocumentTextIcon },
  props: ['modelValue', 'id', 'fileType', 'uploadUrl', 'imageId', 'requirements'],
  emits: ['update:modelValue'],
  methods: {
    preventDefault(e) {
      e.preventDefault();
    },
    handleDrop(e) {
      e.preventDefault();
      const dt = e.dataTransfer;
      const files = dt.files;
      this.handleFiles(files);
    },
    handleFileInput() {
      const files = this.$refs['file-upload-' + this.id].files;
      this.handleFiles(files);
    },
    handleFiles(files) {
      let self = this;

      let file = files[0];

      let formData = new FormData();
      formData.append('files', file);

      axios.post(this.uploadUrl, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(function (res) {
        self.value = res.data.id;
      }).catch(function (error) {
        console.log(error);
      });
    },
    removeImage() {
      this.value = null;
    }
  },
  computed: {
    value: {
      get() {
        return this.modelValue
      },
      set(value) {
        this.$emit('update:modelValue', value)
      }
    }
  }
}
</script>

<style scoped>

</style>