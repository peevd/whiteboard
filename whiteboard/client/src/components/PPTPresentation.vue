<template>
  <div
    id="ppt"
    :class="[ fullscreen ? 'fullscreen' : '' ]" >
    <div
      ref="ppt-body"
      :style="{ width: divWidth }"
      class="ppt-body">
      <div
        id="ppt-div"
        ref="pptdiv"
        :style="{ height: divHeight, width: divWidth }">
        <iframe
          v-show="ppt.url !== undefined"
          id="ppt-presentation"
          ref="pptframe"
          :src="ppt.url"
          :style="{'pointer-events': hideControls ? 'none' : 'initial'}"
          class="border shadow"
          @resize="handleResize"
          @load="attachMouseEvents" />
      </div>
      <div
        id="ppt-controls"
        :style="{ width: divWidth }"
        class="card border shadow">
        <div class="card-body p-1">
          <div class="row">

            <div
              v-if="!hideControls"
              class="col-auto">
              <button
                id="ppt-fs-btn"
                class="btn btn-sm btn-default"
                title="Select presentation"
                @click="handleSelect" >
                <custom-icon
                  icon="task"
                  size="1x" />
              </button>
            </div>

            <div class="col" />

            <div
              v-if="!hideControls"
              class="col-auto p-0">
              <button
                id="ppt-fs-btn"
                class="btn btn-sm btn-default"
                title="Previous"
                @click="handlePrevSlide" >
                <custom-icon
                  icon="prev"
                  size="1x" />
              </button>
            </div>

            <div
              v-if="!hideControls"
              class="col-auto p-0">
              <button
                id="ppt-fs-btn"
                class="btn btn-sm btn-default"
                title="Next"
                @click="handleNextSlide" >
                <custom-icon
                  icon="next"
                  size="1x" />
              </button>
            </div>

            <div class="col-auto">
              <button
                id="ppt-fs-btn"
                class="btn btn-sm btn-default"
                title="Fullscreen"
                @click="handleClick" >
                <custom-icon
                  icon="fullscreen"
                  size="1x" />
              </button>
            </div>

          </div>
        </div>
      </div>
    </div>

    <PPTSelectModal
      :show="showSelect"
      :c-id="cId"
      @hide="handleSelect" />

  </div>
</template>

<script>
import io from 'socket.io-client';
import config from '@/config.json';

import PPTSelectModal from '@/components/PPTSelectModal';

export default {
  name: 'PPTPresentation',
  components: {
    PPTSelectModal,
  },
  props: {
    cId: { type: Number, default: 0 },
    hideControls: { type: Boolean, default: false },
  },
  data() {
    return {
      fullscreen: false,
      aspectRatio: 1,
      divHeight: null,
      divWidth: null,
      showSelect: false,
      currentSlide: 0,
      currentEffect: 0,
      socket: io(`${config.hostname}/data`, {
        path: '/whiteboard.io',
      }),
    };
  },
  computed: {
    ppt() {
      return this.$store.state.currentPPT;
    },
  },
  mounted() {
    window.addEventListener('resize', this.handleResize);
    this.$refs.pptframe.addEventListener('load', this.onLoad);

    if (this.socket !== null) {
      this.socket.emit('ppt', { room: this.cId, action: 'join' });

      const self = this;
      this.socket.on('ppt', (data) => {
        switch (data.action) {
          case ('getSlide'):
            if (!self.hideControls) {
              self.sendCurrentSlide();
            }
            break;
          case ('setSlide'):
            if (self.hideControls) {
              self.currentSlide = data.slide;
              self.currentEffect = data.effect;
              self.setCurrentPresentation(data.currentPPT);
            }
            break;
          case ('nextEffect'):
            if (self.hideControls) {
              self.handleNextSlide();
            }
            break;
          case ('prevEffect'):
            if (self.hideControls) {
              self.handlePrevSlide();
            }
            break;
          default:
            break;
        }
      });

      if (this.hideControls) {
        this.socket.emit('ppt', { room: this.cId, action: 'getSlide' });
      }
    }
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
    this.socket.disconnect();
  },
  methods: {
    onLoad() {
      this.handleResize();

      this.$refs.pptframe.contentWindow.onload = null;
      this.$refs.pptframe.contentWindow.oncontext = null;

      if (!this.hideControls) {
        this.sendCurrentSlide();
      } else {
        this.setCurrentSlide();
      }
    },
    handleClick(e) {
      this.toggleFullscreen();
      e.preventDefault();
    },
    getAspectRatio() {
      const svg = this.$refs.pptframe.contentDocument.querySelector('svg');
      const parts = svg.getAttribute('viewBox').split(' ');
      this.aspectRatio = parts[2] / parts[3];
    },
    handleResize() {
      if (this.ppt.url === undefined) return;

      this.getAspectRatio();

      let newHeight = this.$refs.pptdiv.clientWidth / this.aspectRatio;
      this.divHeight = `${newHeight}px`;

      if (this.fullscreen) {
        if (newHeight > document.documentElement.clientHeight * 0.8) {
          newHeight = Number(document.documentElement.clientHeight) * 0.8;

          this.divHeight = `${newHeight}px`;
          this.divWidth = `${newHeight * this.aspectRatio}px`;
        }
      }
    },
    toggleFullscreen() {
      this.fullscreen = !this.fullscreen;

      if (!this.fullscreen) {
        this.divHeight = null;
        this.divWidth = null;
      }

      this.$nextTick(() => {
        this.handleResize();
      });
    },
    handleNextSlide() {
      this.$refs.pptframe.contentWindow.dispatchEffects(1);

      if (!this.hideControls) {
        this.sendNextSlide();
      }
    },
    handlePrevSlide() {
      this.$refs.pptframe.contentWindow.dispatchEffects(-1);

      if (!this.hideControls) {
        this.sendPrevSlide();
      }
    },
    setCurrentPresentation(name) {
      this.$store.dispatch('selectPPT', { cId: this.cId, name });
    },
    setCurrentSlide() {
      if (this.$refs.pptframe.contentWindow.aSlideShow === undefined) return;

      this.$refs.pptframe.contentWindow.aSlideShow.displaySlide(this.currentSlide);

      while (this.$refs.pptframe.contentWindow.aSlideShow.nCurrentEffect !== this.currentEffect) {
        this.$refs.pptframe.contentWindow.aSlideShow.skipPlayingOrNextEffect();
      }
    },
    handleSelect() {
      this.showSelect = !this.showSelect;
    },
    attachMouseEvents() {
      // prevent context menu when right clicking to get previous slide
      this.$refs.pptframe.contentWindow.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        this.sendPrevSlide();
        return false;
      });
      // prevent text selection when left clicking to get next slide
      this.$refs.pptframe.contentWindow.addEventListener('mousedown', (e) => {
        e.preventDefault();
        return false;
      });

      this.$refs.pptframe.contentWindow.addEventListener('click', (e) => {
        this.sendNextSlide();
        e.preventDefault();
        return false;
      });
    },
    sendCurrentSlide() {
      if (this.ppt.url === undefined) return;

      const payload = {
        room: this.cId,
        action: 'setSlide',
        currentPPT: this.ppt.name,
        slide: this.$refs.pptframe.contentWindow.nCurSlide,
        effect: this.$refs.pptframe.contentWindow.aSlideShow.nCurrentEffect,
      };

      this.socket.emit('ppt', payload);
    },
    sendNextSlide() {
      const payload = {
        room: this.cId,
        action: 'nextEffect',
      };

      this.socket.emit('ppt', payload);
    },
    sendPrevSlide() {
      const payload = {
        room: this.cId,
        action: 'prevEffect',
      };

      this.socket.emit('ppt', payload);
    },
  },
};
</script>

<style>
#ppt-presentation {
  border: 0;

  height: 100%;
  width: 100%;

  background: white;
}

#ppt-div {
  position: relative;
}

.fullscreen > .ppt-body {
  position: fixed;
  max-width: 80%;
  width: 80%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.fullscreen > #ppt-controls {
  width: 80%;
}

#ppt-controls {
  border-radius: 0 0 0.25rem 0.25rem;
}

.ppt-body,
.ppt-body * {
  z-index: 1030;
}
</style>
