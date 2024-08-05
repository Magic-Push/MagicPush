<template>
  <li :ref="dynamicRef" :id="dynamicRef" class="relative p-6 max-w-full">
    <template v-if="flowEventsLength > 1">
      <div class="border-t-2 absolute h-8 border-gray-300 top-0" :style="flowEventIndex === 0 ? 'left: 50%; right: 0;' : 'left: 0; right: 50%;'"></div>
    </template>
    <div class="relative flex justify-center">
      <div :id="`top-stroke-${dynamicRef}`" class="-mt-6 border-l-2 absolute h-6 border-gray-300 top-0"></div>
      <div class="text-center">
        <div v-if="flowEvent.type === 'Loop back'">
          <div @mouseover="highlightLoop(flowEvent.loop_back_to_event_id)" @mouseleave="quitHighlightLoop" class="mx-auto cursor-pointer relative rounded-full p-1 text-gray-400 border-gray-300 border-2 w-9 h-9 content-center">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="mx-auto size-5">
              <path fill-rule="evenodd" d="M12 5.25c1.213 0 2.415.046 3.605.135a3.256 3.256 0 0 1 3.01 3.01c.044.583.077 1.17.1 1.759L17.03 8.47a.75.75 0 1 0-1.06 1.06l3 3a.75.75 0 0 0 1.06 0l3-3a.75.75 0 0 0-1.06-1.06l-1.752 1.751c-.023-.65-.06-1.296-.108-1.939a4.756 4.756 0 0 0-4.392-4.392 49.422 49.422 0 0 0-7.436 0A4.756 4.756 0 0 0 3.89 8.282c-.017.224-.033.447-.046.672a.75.75 0 1 0 1.497.092c.013-.217.028-.434.044-.651a3.256 3.256 0 0 1 3.01-3.01c1.19-.09 2.392-.135 3.605-.135Zm-6.97 6.22a.75.75 0 0 0-1.06 0l-3 3a.75.75 0 1 0 1.06 1.06l1.752-1.751c.023.65.06 1.296.108 1.939a4.756 4.756 0 0 0 4.392 4.392 49.413 49.413 0 0 0 7.436 0 4.756 4.756 0 0 0 4.392-4.392c.017-.223.032-.447.046-.672a.75.75 0 0 0-1.497-.092c-.013.217-.028.434-.044.651a3.256 3.256 0 0 1-3.01 3.01 47.953 47.953 0 0 1-7.21 0 3.256 3.256 0 0 1-3.01-3.01 47.759 47.759 0 0 1-.1-1.759L6.97 15.53a.75.75 0 0 0 1.06-1.06l-3-3Z" clip-rule="evenodd" />
            </svg>
          </div>
          <div v-if="highLightEventId" class="mt-2 p-2 text-left bg-background border border-gray-200 rounded-lg shadow-sm opacity-80">
            <span class="text-gray-800 text-xs">
              Loops back
            </span>
          </div>
        </div>
        <div v-else-if="flowEvent.type === 'End'">
          <div @mouseover="hoverEnd = true" @mouseleave="hoverEnd = false" class="mx-auto cursor-pointer relative rounded-full p-1 text-gray-400 border-gray-300 border-2 w-9 h-9 content-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="mx-auto size-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>
          </div>
          <div v-if="hoverEnd" class="mt-2 p-2 text-left bg-background border border-gray-200 rounded-lg shadow-sm opacity-80">
            <span class="text-gray-800 text-xs">
              End flow
            </span>
          </div>
        </div>
        <div v-else class="flex flex-col justify-center items-center">
          <div :id="`div-${dynamicRef}`" @click="clickEvent(flowEvent)" :class="events.find((flowEvent2) => flowEvent.id === flowEvent2.id).isHighlighted ?  'opacity-100' : 'opacity-30'" class="p-2 text-left bg-background border border-gray-200 rounded-lg shadow-sm cursor-pointer" style="width: 250px; z-index: 10;">
            <div class="flex w-full items-center">
              <div class="inline-block rounded-lg w-7 h-7 relative content-center text-center" :class="typeColors[flowEvent.type]">
                <component :is="getIcon(flowEvent)" class="opacity-90 w-4 h-4 mx-auto text-white" />
              </div>
              <div class="inline-block text-sm text-gray-500 pl-2">
                {{ flowEvent.type }}
              </div>
            </div>
            <span class="text-gray-800 text-sm mt-2" v-if="flowEvent.type === 'Delay'">
              {{ flowEvent.delay }} {{ flowEvent.delay_unit }}
            </span>
            <span class="text-gray-800 text-sm mt-2" v-else-if="flowEvent.type === 'Yes/No condition'">
              <span class="bg-gray-100 text-gray-800 text-xs font-normal px-2.5 py-0.5 rounded dark:bg-gray-600 dark:text-gray-300">{{ flowEvent.statement }}</span>
            </span>
            <span class="text-gray-800 text-sm mt-2" v-else-if="flowEvent.type === 'Notification'">
              Send <span class="bg-gray-100 text-gray-800 text-xs font-normal px-2.5 py-0.5 rounded dark:bg-gray-600 dark:text-gray-300">{{ flowEvent.notification.name }}</span> notification.
            </span>
            <span class="text-gray-800 text-sm mt-2" v-else-if="flowEvent.type === 'Loop back'">
              Loop back to event <span class="whitespace-nowrap bg-gray-100 text-gray-800 text-xs font-normal px-2.5 py-0.5 rounded dark:bg-gray-600 dark:text-gray-300">{{ events.find((flowEvent2) => flowEvent2.id === flowEvent.loop_back_to_event_id).type }}</span>
            </span>
          </div>
          <div v-if="flowEvent.type !== 'Loop back'" :id="`bottom-stroke-${dynamicRef}`" class="border-l-2 block mx-auto h-6 border-gray-300"></div>
          <div v-if="flowEvent.type !== 'Yes/No condition' && flowEvent.type !== 'Loop back'" class="cursor-pointer block mx-auto w-8 h-8 text-gray-400 hover:text-gray-500" @click="addEvent(flowEvent.id)">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-8 h-8">
              <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25ZM12.75 9a.75.75 0 0 0-1.5 0v2.25H9a.75.75 0 0 0 0 1.5h2.25V15a.75.75 0 0 0 1.5 0v-2.25H15a.75.75 0 0 0 0-1.5h-2.25V9Z" clip-rule="evenodd" />
            </svg>
          </div>
        </div>
        <!-- Check if there are nested events and recursively render them -->
        <ul v-if="flowEvent.events && flowEvent.events.length > 0" class="flex flex-row justify-center">
          <flow-event v-for="(nestedEvent, index) in flowEvent.events" :key="nestedEvent.id"
                      v-bind:flowEvent="nestedEvent" v-bind:flowEventsLength="flowEvent.events.length"
                      v-bind:flowEventIndex="index" v-bind:events="events" v-bind:loopBackLineHeight="loopBackLineHeight"
                      v-bind:flowListWidth="flowListWidth" v-bind:flowSide="flowSideData" v-bind:loopBack="loopBack"
                      v-bind:selectedParentId="selectedParentId" v-on:clickEvent="clickEvent"
                      v-on:addEvent="addEvent" v-on:highlightLoop="highlightLoop"
                      v-on:quitHighlightLoop="quitHighlightLoop"></flow-event>
        </ul>
      </div>
    </div>
  </li>
</template>

<script>
import {
  ArrowPathRoundedSquareIcon,
  ClockIcon,
  FunnelIcon,
  MagnifyingGlassIcon,
  PaperAirplaneIcon
} from '@heroicons/vue/20/solid'

export default {
  name: "FlowEvent",
  components: {
    PaperAirplaneIcon,
    ClockIcon,
    FunnelIcon,
    MagnifyingGlassIcon,
    ArrowPathRoundedSquareIcon,
  },
  props: ['flowEvent', 'flowEventsLength', 'flowEventIndex', 'events', 'loopBackLineHeight', 'flowListWidth', 'flowSide', 'loopBack', 'selectedParentId'],
  data() {
    return {
      dynamicRef: '',
      flowSideData: null,
      highLightEventId: null,
      hoverEnd: false,
      typeColors: {
        'Delay': 'bg-blue-500',
        'Notification': 'bg-primary-500',
        'Yes/No condition': 'bg-yellow-400',
        'Yes': 'bg-green-400',
        'No': 'bg-red-500',
        'Loop back': 'bg-primary-500',
      }
    }
  },
  mounted() {
    this.dynamicRef = `event-${this.flowEvent.id}`;

    if (this.flowSide) {
      this.flowSideData = this.flowSide;
    } else {
      if (this.flowEventsLength > 1) {
        if (this.flowEventIndex === 0) {
          this.flowSideData = 'left';
        } else {
          this.flowSideData = 'right';
        }
      }
    }
  },
  watch: {
    flowSide(newVal) {
      this.flowSideData = newVal;
    }
  },
  methods: {
    getIcon(flowEvent) {
      switch (flowEvent.type) {
        case 'Delay':
          return 'ClockIcon';
        case 'Notification':
          return 'PaperAirplaneIcon';
        case 'Yes/No condition':
          return 'FunnelIcon';
        case 'Yes':
          return 'FunnelIcon';
        case 'No':
          return 'FunnelIcon';
        case 'Loop back':
          return 'ArrowPathRoundedSquareIcon';
        default:
            return null;
      }
    },
    addEvent(id) {
      this.$emit('addEvent', id);
    },
    clickEvent(flowEvent) {
      this.$emit('clickEvent', flowEvent);
    },
    highlightLoop(loop_back_to_event_id) {
      this.highLightEventId = loop_back_to_event_id;
      this.$emit('highlightLoop', loop_back_to_event_id);
    },
    quitHighlightLoop() {
      this.highLightEventId = null;
      this.$emit('quitHighlightLoop');
    }
  },
}
</script>

<style scoped>

</style>