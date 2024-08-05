<template>
  <div class="dropzone mb-3 dz-clickable"
       :class="[multiple ? 'dropzone-multiple': 'dropzone-single']">
    <div class="fallback">
      <div class="custom-file">
        <input type="file"
               class="custom-file-input"
               id="projectCoverUploads"
               :multiple="multiple">
        <label class="custom-file-label" for="projectCoverUploads">Choose file</label>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DropzoneFileUpload',
  props: {
    options: {
      type: Object,
      default: () => ({})
    },
    value: [String, Object, Array],
    url: {
      type: String,
      default: 'http://'
    },
    multiple: Boolean,
    previewClasses: [String, Object, Array]
  },
  model: {
    prop: 'value',
    event: 'change'
  },
  data() {
    return {
      currentFile: null,
      files: [],
      showList: false,
    }
  },
  watch: {
    currentFile(newVal) {
    }
  },
  methods: {
    async initDropzone() {
      let self = this;
      let Dropzone = await import('dropzone');

      Dropzone = Dropzone.default || Dropzone;
      Dropzone.autoDiscover = false;

      let finalOptions = {
        ...this.options,
        url: this.url,
        thumbnailWidth: null,
        thumbnailHeight: null,
        maxFiles: (!this.multiple) ? 1 : null,
        acceptedFiles: null,
        init: function () {
          this.on("addedfile", function (file) {
            if (!self.multiple && self.currentFile) {
              this.removeFile(self.currentFile);
            }
            self.currentFile = file;
          })
        }
      };
      this.dropzone = new Dropzone(this.$el, finalOptions);

      let evtList = ['drop', 'dragstart', 'dragend', 'dragenter', 'dragover', 'addedfile', 'removedfile', 'thumbnail', 'error', 'processing', 'uploadprogress', 'sending', 'success', 'complete', 'canceled', 'maxfilesreached', 'maxfilesexceeded', 'processingmultiple', 'sendingmultiple', 'successmultiple', 'completemultiple', 'canceledmultiple', 'totaluploadprogress', 'reset', 'queuecomplete']
      evtList.forEach(evt => {
        this.dropzone.on(evt, (data) => {
          this.$emit(evt, data);

          if (evt === 'addedfile') {
            this.files.push(data)
            this.$emit('change', this.files);
          } else if (evt === 'removedfile') {
            let index = this.files.findIndex(f => f.upload.uuid === data.upload.uuid)
            if (index !== -1) {
              this.files.splice(index, 1);
            }
            this.$emit('change', this.files);
          } else if (evt === 'success') {
            this.$emit("uploaded");
          }
        })
      })
    }
  },
  async mounted() {
    await this.initDropzone()
  }
}
</script>

<style scoped>
input {
  position: absolute;
  display: block;
  visibility: hidden;
  width: 100%;
  height: 100%;
}
</style>