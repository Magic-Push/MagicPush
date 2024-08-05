<template>
  <div v-if="flow" class="builder h-screen bg-background overflow-hidden bg-gray-50 border-l-gray-50" style="border-left-style: solid; border-left-width: 0;">
    <div class="flex w-full items-center p-4 z-30">
      <div v-if="loopBack" class="inline-block rounded-lg hover:bg-gray-200 w-6 h-6 mr-4 cursor-pointer" @click="loopBack = false">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="black" class="size-6">
          <path fill-rule="evenodd" d="M11.03 3.97a.75.75 0 0 1 0 1.06l-6.22 6.22H21a.75.75 0 0 1 0 1.5H4.81l6.22 6.22a.75.75 0 1 1-1.06 1.06l-7.5-7.5a.75.75 0 0 1 0-1.06l7.5-7.5a.75.75 0 0 1 1.06 0Z" clip-rule="evenodd" />
        </svg>
      </div>
      <div v-else class="inline-block rounded-lg hover:bg-gray-200 w-6 h-6 mr-4 cursor-pointer" @click="$router.push({ path: '/flows', query: { app: currentApp.id }})">
        <svg xmlns="http://www.w3.org/2000/svg" fill="black" viewBox="0 0 24 24" stroke-width="1.5" stroke="black"
             class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12"/>
        </svg>
      </div>
      <h1 class="inline-block font-normal text-2xl text-slate-900">{{ loopBack ? 'Loop back to' : 'Flow Builder' }}</h1>
      <button @click="openSettingsModal = true" class="fixed right-0 mr-4 cursor-pointer hidden rounded-md bg-white px-2.5 py-1.5 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:block">
        Settings
      </button>
    </div>

    <div ref="flowBuilder" class="relative flow-builder overflow-auto w-full h-full"
         @mousedown="startDrag"
         @mouseup="stopDrag"
         @mouseleave="stopDrag"
         @mousemove="handleDrag"
         @wheel="handleZoom">
      <div class="canvas w-full flex justify-center sm:ml-0 min-w-max min-h-full" :style="zoomStyle">
        <div class="text-center">
          <div class="flex flex-col items-center">
            <div class="text-sm font-normal text-gray-500 bg-background border border-gray-200 rounded-lg shadow-sm p-5">
              Triggered by event <span class="bg-gray-100 text-gray-800 text-xs font-normal px-2.5 py-0.5 rounded dark:bg-gray-600 dark:text-gray-300">{{ flow.event }}</span>
            </div>
            <div class="border-l-2 h-6 border-gray-300"></div>
            <div class="cursor-pointer block mx-auto w-8 h-8 text-gray-400 hover:text-gray-500" @click="addEvent(null)">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-8 h-8">
                <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25ZM12.75 9a.75.75 0 0 0-1.5 0v2.25H9a.75.75 0 0 0 0 1.5h2.25V15a.75.75 0 0 0 1.5 0v-2.25H15a.75.75 0 0 0 0-1.5h-2.25V9Z" clip-rule="evenodd" />
              </svg>
            </div>
          </div>
          <ul id="flowList" class="flex flex-row justify-center">
            <flow-event v-for="(event, index) in flow.events" :key="event.id" v-bind:flowEvent="event"
                        v-bind:flowEventsLength="flow.events.length" v-bind:flowEventIndex="index"
                        v-bind:events="events" v-bind:loopBackLineHeight="loopBackLineHeight"
                        v-bind:flowListWidth="flowListWidth" v-bind:loopBack="loopBack"
                        v-bind:selectedParentId="selectedParentId" v-on:clickEvent="clickEvent" v-on:addEvent="addEvent"
                        v-on:highlightLoop="highlightLoop" v-on:quitHighlightLoop="quitHighlightLoop">
            </flow-event>
          </ul>
        </div>
      </div>
    </div>

    <AddEventModal v-bind:open="openAddEventModal" v-on:onClose="openAddEventModal = false" v-on:onSelect="onSelect"/>
    <CreateNotificationModal2 v-bind:show="openAddNotificationModal" v-on:onClose="openAddNotificationModal = false"
                              v-bind:flowId="flowId" v-bind:parentId="selectedParentId"
                              v-bind:selectedFlowEvent="selectedFlowEvent" v-on:onUpdate="updateFlow"/>
    <AddDelayModal v-bind:open="openAddDelayModal" v-bind:flowId="flowId" v-bind:parentId="selectedParentId"
                   v-on:onClose="openAddDelayModal = false" v-bind:selectedFlowEvent="selectedFlowEvent"
                   v-on:onUpdate="updateFlow"/>
    <AddYesNoCondition v-bind:open="openAddYesNoCondition" v-bind:flowId="flowId" v-bind:parentId="selectedParentId"
                       v-on:onClose="openAddYesNoCondition = false" v-bind:selectedFlowEvent="selectedFlowEvent"
                       v-on:onUpdate="updateFlow"/>
  </div>
</template>

<script>
import FlowEvent from "@/components/FlowEvent.vue";
import AddEventModal from "@/modals/AddEventModal.vue";
import AddDelayModal from "@/modals/AddDelayModal.vue";
import AddYesNoCondition from "@/modals/AddYesNoCondition.vue";
import CreateNotificationModal2 from "@/modals/CreateNotificationModal2.vue";

export default {
  name: "FlowBuilderPage",
  components: {
    CreateNotificationModal2,
    AddYesNoCondition,
    AddDelayModal,
    AddEventModal,
    FlowEvent,
  },
  data() {
    return {
      originX: 0,
      originY: 0,
      zoomLevel: 1,
      isDragging: false,
      start: { x: 0, y: 0 },
      openSettingsModal: false,
      openAddEventModal: false,
      openAddNotificationModal: false,
      openAddDelayModal: false,
      openAddYesNoCondition: false,
      loopBack: false,
      loopBackFromParentId: null,
      loopBackLineHeight: 0,
      selectedParentId: null,
      selectedFlowEvent: null,
      flow: null,
      flowId: null,
      events: [],
      flowListWidth: 0
    }
  },
  mounted() {
    if (this.$route.params.id) {
      let self = this;

      this.flowId = this.$route.params.id;
      if (this.flowId) {
        this.$store.dispatch('getFlow', this.flowId)
            .then((res) => {
              self.flow = res.data;

              setTimeout(() => {
                self.$refs.flowBuilder.scrollLeft = (self.$refs.flowBuilder.scrollWidth - self.$refs.flowBuilder.clientWidth) / 2;
                self.flowListWidth = document.getElementById('flowList').clientWidth / 10;
              }, 10);
            })
            .catch((err) => {
              alert('Error fetching flow, please try again');
            });
      }
    }
  },
  computed: {
    zoomStyle() {
      return {
        transform: `scale(${this.zoomLevel})`,
        transformOrigin: `${this.originX}px ${this.originY}px`
      };
    },
    currentApp() {
      return this.$store.getters.currentApp;
    }
  },
  methods: {
    addEvent(id) {
      this.selectedFlowEvent = null;
      this.openAddEventModal = true;
      this.selectedParentId = id;
    },
    clickEvent(flowEvent) {
      if (this.loopBack && flowEvent.id !== this.selectedParentId) {
        let flowData = {
          id: this.flowId,
          events: [
            {
              type: 'Loop back',
              parent_id: this.selectedParentId,
              loop_back_to_event_id: flowEvent.id
            }
          ],
        }

        let self = this;
        this.$store.dispatch('updateFlow', flowData)
            .then((res) => {
              self.loopBack = false;
              self.updateFlow(res.data);
            })
            .catch((err) => {
              alert('Error adding delay, please try again');
            });
      } else {
        this.selectedFlowEvent = flowEvent;
        if (flowEvent.type === 'Notification') {
          this.openAddNotificationModal = true;
        } else if (flowEvent.type === 'Delay') {
          this.openAddDelayModal = true;
        } else if (flowEvent.type === 'Yes/No condition') {
          this.openAddYesNoCondition = true;
        }
      }
    },
    onSelect(item) {
      this.openAddEventModal = false;
      if (item.name === 'Notification') {
        this.openAddNotificationModal = true;
      } else if (item.name === 'Delay') {
        this.openAddDelayModal = true;
      } else if (item.name === 'Yes/No condition') {
        this.openAddYesNoCondition = true;
      } else if (item.name === 'Loop back') {
        this.loopBack = true;
      } else if (item.name === 'End') {
        let flowData = {
          id: this.flowId,
          events: [
            {
              type: 'End',
              parent_id: this.selectedParentId
            }
          ],
        }

        let self = this;
        this.$store.dispatch('updateFlow', flowData)
            .then((res) => {
              self.updateFlow(res.data);
            })
            .catch((err) => {
              alert('Error adding delay, please try again');
            });
      }
    },
    startDrag(e) {
      this.isDragging = true;
      this.start = {
        x: e.clientX,
        y: e.clientY
      };
      e.preventDefault(); // Prevent text selection during drag
    },
    handleDrag(e) {
      if (this.isDragging) {
        const dx = e.clientX - this.start.x;
        const dy = e.clientY - this.start.y;
        this.start = {
          x: e.clientX,
          y: e.clientY
        };
        this.$refs.flowBuilder.scrollLeft -= dx;
        this.$refs.flowBuilder.scrollTop -= dy;
      }
    },
    stopDrag() {
      this.isDragging = false;
    },
    handleZoom(e) {
      if (this.$refs.flowBuilder === undefined) {
        return;
      }

      const rect = this.$refs.flowBuilder.getBoundingClientRect();
      const x = e.clientX - rect.left; // Mouse x position within the element
      const y = e.clientY - rect.top;  // Mouse y position within the element

      const oldZoomLevel = this.zoomLevel;
      if (e.deltaY < 0) {
        this.zoomLevel *= 1.1;  // Zoom in
      } else {
        this.zoomLevel /= 1.1;  // Zoom out
      }

      // Update origin to cursor position
      this.originX = x;
      this.originY = y;

      // Adjust scroll to keep the cursor point stable
      const scaleFactor = this.zoomLevel / oldZoomLevel;
      this.$refs.flowBuilder.scrollLeft = (this.$refs.flowBuilder.scrollLeft + x) * scaleFactor - x;
      this.$refs.flowBuilder.scrollTop = (this.$refs.flowBuilder.scrollTop + y) * scaleFactor - y;

      e.preventDefault(); // Prevent the page from scrolling
    },
    updateFlow(flow) {
      console.log('Flow updated')
      console.log(flow);
      this.flow = flow;
    },
    parseFlowEvent(flowEvents) {
      let self = this;
      flowEvents.forEach((flowEvent) => {
        flowEvent['isHighlighted'] = true;
        self.events.push(flowEvent);
        if (flowEvent.events && flowEvent.events.length > 0) {
          self.parseFlowEvent(flowEvent.events);
        }
      });
    },
    calculateLoopBackHeight() {
      let self = this;
      this.events.forEach((flowEvent) => {
        if (flowEvent.loop_back_to_event_id) {
          let loopElement = document.getElementById(`event-${flowEvent.id}`);
          this.events.forEach((flowEvent2) => {
            if (flowEvent.loop_back_to_event_id === flowEvent2.id) {
              let targetElement = document.getElementById(`event-${flowEvent2.id}`);

              // Calculate the center points of both elements
              let loopElementCenter = loopElement.scrollTop + (loopElement.scrollHeight / 2);
              let targetElementCenter = targetElement.scrollHeight - targetElement.scrollTop - (targetElement.scrollHeight / 2);

              // Calculate the height difference
              self.loopBackLineHeight = targetElementCenter;
            }
          });
        }
      });
    },
    highlightLoop(loop_back_to_event_id) {
      this.events.forEach((flowEvent) => {
        if (flowEvent.id === loop_back_to_event_id) {
          flowEvent.isHighlighted = true;
        } else {
          flowEvent.isHighlighted = false;
        }
      });
    },
    quitHighlightLoop() {
      this.events.forEach((flowEvent) => {
        flowEvent.isHighlighted = true;
      });
    }
  },
  watch: {
    flow: function (newFlow) {
      this.parseFlowEvent(newFlow.events);
    }
  }
}
</script>

<style scoped>
.canvas {
  background-image: radial-gradient(#d0d0d0 1px, transparent 0);
  background-size: 30px 30px;
  background-position: -14px -14px;
}

.flow-builder {
  cursor: grab; /* Shows a grabbing hand when mouse is over the scroll area */
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

.flow-builder:active {
  cursor: grabbing; /* Changes cursor to grabbing when dragging */
}

.flow-builder::-webkit-scrollbar {
  width: 6px;               /* width of the entire scrollbar */
  padding: 1px;
}

.flow-builder::-webkit-scrollbar-track {
  background: transparent;        /* color of the tracking area */
}

.flow-builder::-webkit-scrollbar-thumb {
  background-color: #eeeeee;    /* color of the scroll thumb */
  border-radius: 20px;       /* roundness of the scroll thumb */
  border: 3px solid transparent;  /* creates padding around scroll thumb */
}
</style>