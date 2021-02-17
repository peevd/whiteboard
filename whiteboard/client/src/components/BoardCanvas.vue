<template>
  <div
    id="board-canvs"
    class="row">
    <div class="col-sm-12">
      <div class="row">
        <div class="col-sm-12">
          <div
            v-if="editable"
            id="board-canvas--tools"
            class="row row-eq-height m-0 mb-4">
            <div
              v-if="isTeacher"
              class="col-sm-auto p-0">
              <button
                title="Allow students to edit board"
                class="btn btn-default bg-default shadow border mr-1 mb-1"
                @click="toggleStudentEdit">
                <custom-icon
                  icon="student"
                  size="2x" />
              </button>
            </div>
            <div
              v-for="tool in tools"
              :key="tool.name"
              class="col-sm-auto p-0">
              <button
                :title="tool.name"
                :class="{ 'btn-success': tool.active, 'bg-default btn-default': !tool.active }"
                class="btn shadow mr-1 mb-1 border"
                @click="activateTool(tool)">
                <!--
                <font-awesome-icon
                  :icon="tool.icon"
                  size="2x" />
                -->
                <custom-icon
                  :icon="tool.icon"
                  size="2x" />
              </button>
            </div>
            <div class="dropdown d-inline-block mr-1 mb-1">
              <button
                id="dropdownMenuButton"
                :style="{ fill: primaryColor }"
                class="btn btn-default bg-default dropdown-toggle border shadow"
                type="button"
                title="Primary Color"
                data-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false">
                <custom-icon
                  icon="paintPaletteStroke"
                  size="2x" />
              </button>
              <div class="dropdown-menu bg-default mr-1 mb-1">
                <a
                  v-for="color in colors"
                  :key="color.name"
                  :title="color.name"
                  :style="{ color: color.color }"
                  class="dropdown-item"
                  href="#"
                  @click.prevent="activateColorP(color)" >
                  <font-awesome-icon
                    icon="circle"
                    class="border rounded-circle"
                    size="2x" />
                </a>
              </div>
            </div>
            <div class="dropdown d-inline-block mr-1 mb-1">
              <button
                id="dropdownMenuButton"
                :style="{ fill: secondaryColor }"
                class="btn btn-default bg-default dropdown-toggle border shadow"
                type="button"
                title="Secondary Color"
                data-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false">
                <custom-icon
                  icon="paintPaletteFill"
                  size="2x" />
              </button>
              <div class="dropdown-menu bg-default">
                <a
                  v-for="color in colors"
                  :key="color.name"
                  :title="color.name"
                  :style="{ color: color.color }"
                  class="dropdown-item"
                  href="#"
                  @click.prevent="activateColorS(color)" >
                  <font-awesome-icon
                    icon="circle"
                    class="border rounded-circle"
                    size="2x" />
                </a>
              </div>
            </div>
            <div class="dropdown d-inline-block mr-1 mb-1">
              <button
                id="dropdownMenuButton"
                class="btn btn-default bg-default dropdown-toggle border shadow"
                type="button"
                title="Stroke Width"
                data-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false">
                <custom-icon
                  icon="pencilSize"
                  size="2x" />
              </button>
              <div class="dropdown-menu bg-default">
                <div class="input-group w-200 px-2 py-1">
                  <input
                    v-model="strokeWidth"
                    type="number"
                    class="form-control col-sm-4 text-center py-1">
                  <input
                    id="stroke-width-input"
                    v-model="strokeWidth"
                    type="range"
                    class="form-control custom-range col-sm-8 border px-2">
                </div>
              </div>
            </div>
            <div
              class="col-sm-auto p-0">
              <button
                title="Undo"
                class="btn btn-default bg-default shadow border mr-1 mb-1"
                @click="undo">
                <custom-icon
                  icon="undo"
                  size="2x" />
              </button>
            </div>
            <div
              class="col-sm-auto p-0">
              <button
                title="Redo"
                class="btn btn-default bg-default shadow border mr-1 mb-1"
                @click="redo">
                <custom-icon
                  icon="redo"
                  size="2x" />
              </button>
            </div>
            <div class="col-sm-auto p-0">
              <button
                title="Clear Board"
                class="btn btn-default bg-default shadow border mr-1 mb-1"
                @click="clear">
                <custom-icon
                  icon="close"
                  size="2x" />
              </button>
            </div>
            <button
              title="Save"
              class="btn btn-default bg-default shadow border mr-1 mb-1"
              @click="save">
              <custom-icon
                icon="floppyDisk"
                size="2x" />
            </button>
            <button
              title="Zoom in"
              class="btn btn-default bg-default shadow border mr-1 mb-1"
              @click="zoom(1)">
              <custom-icon
                icon="zoomIn"
                size="2x" />
            </button>
            <button
              title="Zoom out"
              class="btn btn-default bg-default shadow border mr-1 mb-1"
              @click="zoom(-1)">
              <custom-icon
                icon="zoomOut"
                size="2x" />
            </button>
          </div>
          <div
            v-else
            id="board-canvas--tools"
            class="row row-eq-height m-0 mb-4">
            <button
              title="Zoom in"
              class="btn btn-default bg-default shadow border mr-1 mb-1"
              @click="zoom(1)">
              <custom-icon
                icon="zoomIn"
                size="2x" />
            </button>
            <button
              title="Zoom out"
              class="btn btn-default bg-default shadow border mr-1 mb-1"
              @click="zoom(-1)">
              <custom-icon
                icon="zoomOut"
                size="2x" />
            </button>
          </div>
        </div>
      </div>
      <div
        class="row">
        <div
          id="canvas"
          class="overlay" />
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable-next-line */
import LC_CSS from 'literallycanvas/lib/css/literallycanvas.css';
import LC from 'literallycanvas/lib/js/literallycanvas-core';

export default {
  name: 'BoardCanvas',
  props: {
    socket: { type: Object, default: null },
    editable: { type: Boolean, default: true },
    gId: { type: Number, default: 0 },
    cId: { type: Number, default: 0 },
  },
  data() {
    return {
      ticking: false,
      tools: [],
      colors: [
        {
          name: 'Black',
          color: 'rgb(0, 0, 0)',
        },
        {
          name: 'Red',
          color: 'rgb(255, 0, 0)',
        },
        {
          name: 'Green',
          color: 'rgb(0, 255, 0)',
        },
        {
          name: 'Blue',
          color: 'rgb(0, 0, 255)',
        },
        {
          name: 'White',
          color: 'rgb(255, 255, 255)',
        },
        {
          name: 'Yellow',
          color: 'rgb(250, 250, 60)',
        },
      ],
      primaryColor: '#000',
      secondaryColor: '#fff',
      strokeWidth: 5,
      canvasHeight: 0,
      canvasWidth: 0,
      firstUpdate: true,
      studentEdit: false,
    };
  },
  computed: {
    strokeWidthStr() {
      let out = '';

      if (this.strokeWidth < 10) {
        out += '0';
      }

      out += this.strokeWidth;
      return out;
    },
    task() {
      return this.$store.state.currentTask;
    },
    me() {
      // return `${this.$store.state.user.first_name} ${this.$store.state.user.last_name}`;
      return this.$store.state.user.id;
    },
    board() {
      return this.$store.state.currentBoard;
    },
    boardData() {
      return this.$store.state.currentBoardData;
    },
    isTeacher() {
      return this.$store.getters.isTeacher;
    },
  },
  watch: {
    strokeWidth(v) {
      this.tools.forEach((t) => {
        // eslint-disable-next-line
        t.tool.strokeWidth = parseInt(v, 10);
      });
    },
    boardData(newVal) {
      if (newVal) {
        this.lc.loadSnapshot(JSON.parse(newVal));
      }
    },
    editable(v) {
      if (v) {
        this.activateTool(this.tools[0]);
      } else {
        this.activateTool(this.tools[6]);
      }
    },
  },
  mounted() {
    window.addEventListener('resize', this.resize);

    const options = {
      imageSize: {
        width: null,
        height: null,
      },
    };

    this.lc = LC.init(this.$el.querySelector('#canvas'), options);

    this.tools = [
      {
        name: 'Pencil',
        tool: new LC.tools.Pencil(this.lc),
        active: false,
        icon: 'pencil',
      },
      {
        name: 'Eraser',
        tool: new LC.tools.Eraser(this.lc),
        active: false,
        icon: 'eraser',
      },
      {
        name: 'Line',
        tool: new LC.tools.Line(this.lc),
        active: false,
        icon: 'vector',
      },
      {
        name: 'Rectangle',
        tool: new LC.tools.Rectangle(this.lc),
        active: false,
        icon: 'shapeSize',
      },
      {
        name: 'Polygon',
        tool: new LC.tools.Polygon(this.lc),
        active: false,
        icon: 'polygon',
      },
      {
        name: 'Text',
        tool: new LC.tools.Text(this.lc),
        active: false,
        icon: 'text',
      },
      {
        name: 'Pan',
        tool: new LC.tools.Pan(this.lc),
        active: false,
        icon: 'move',
      },
      {
        name: 'Eye Dropper',
        tool: new LC.tools.Eyedropper(this.lc),
        active: false,
        icon: 'eyeDropper',
      },
    ];

    this.lc.on('primaryColorChange', this.primaryColorChange);
    this.lc.on('secondaryColorChange', this.secondaryColorChange);

    this.tools.forEach((t) => {
      // eslint-disable-next-line
      t.tool.strokeWidth = this.strokeWidth;
    });

    if (this.editable) {
      this.activateTool(this.tools[0]);
    } else {
      this.activateTool(this.tools[6]);
    }

    this.activateColorP(this.colors[0]);
    this.activateColorS(this.colors[4]);

    this.drawingChangeUnsubscribe = this.lc.on('drawingChange', this.drawingChange);

    if (this.boardData) this.lc.loadSnapshot(JSON.parse(this.boardData));

    if (this.socket !== null) {
      this.socket.on('data_transfer', (data) => {
        if (data.from !== this.me) {
          this.drawingChangeUnsubscribe();
          this.lc.loadSnapshot(data.snapshot);
          this.drawingChangeUnsubscribe = this.lc.on('drawingChange', this.drawingChange);
        }
      });

      this.socket.on('status', () => {
        this.socket.emit('b_edit', {
          room: this.cId,
          data: this.studentEdit,
        });
      });
    } else {
      console.log('missing socket prop in BoardCanvas');
    }

    this.$nextTick(this.resize);
  },
  methods: {
    toggleStudentEdit() {
      this.studentEdit = !this.studentEdit;
      console.log(this.studentEdit);

      const payload = {
        room: this.cId,
        data: this.studentEdit,
      };

      console.log(payload);
      this.socket.emit('b_edit', payload);
    },
    activateTool(t) {
      this.lc.setTool(t.tool);

      this.tools = this.tools.map((t2) => {
        if (t === t2) {
          return Object.assign({}, t2, { active: true });
        }

        return Object.assign({}, t2, { active: false });
      });
    },
    activateColorP(c) {
      this.lc.setColor('primary', c.color);

      this.colors = this.colors.map((c2) => {
        if (c.name === c2.name) {
          return Object.assign({}, c2, { activeP: true });
        }

        return Object.assign({}, c2, { activeP: false });
      });
    },
    primaryColorChange(c) {
      this.primaryColor = c;
    },
    activateColorS(c) {
      this.lc.setColor('secondary', c.color);

      this.colors = this.colors.map((c2) => {
        if (c.name === c2.name) {
          return Object.assign({}, c2, { activeS: true });
        }

        return Object.assign({}, c2, { activeS: false });
      });
    },
    secondaryColorChange(c) {
      this.secondaryColor = c;
    },
    resize() {
      this.canvasHeight = document.documentElement.clientHeight;
      this.canvasWidth = document.documentElement.clientWidth;

      if (this.lc) {
        this.lc.canvas.width = this.canvasWidth;
        this.lc.canvas.height = this.canvasHeight;
        this.lc.canvas.style.width = `${this.canvasWidth}px`;
        this.lc.canvas.style.height = `${this.canvasHeight}px`;

        this.lc.backgroundCanvas.width = this.canvasWidth;
        this.lc.backgroundCanvas.height = this.canvasHeight;

        this.lc.repaintLayer('main', true);
        this.lc.repaintLayer('background', true);
      }
    },
    drawingChange() {
      const snapshot = this.lc.getSnapshot(['shapes', 'backgroundShapes']);

      if (this.socket !== null) {
        this.socket.emit('b_data', {
          room: this.cId,
          data: {
            from: this.me,
            snapshot,
          },
        });
      } else {
        console.log('missing socket prop in BoardCanvas');
      }
    },
    undo() {
      this.lc.undo();
    },
    redo() {
      this.lc.redo();
    },
    clear() {
      this.lc.clear();
    },
    zoom(sign) {
      this.lc.zoom(Number(sign) * this.lc.config.zoomStep);
    },
    save() {
      const snapshot = this.lc.getSnapshot(['shapes', 'backgroundShapes']);
      const svg = this.lc.getImage().toDataURL();

      this.$store.dispatch('saveBoardData', {
        cId: this.cId,
        gId: this.gId,
        payload: {
          board_data: JSON.stringify(snapshot),
        },
      });

      this.$store.dispatch('saveBoardSnapshot', {
        cId: this.cId,
        gId: this.gId,
        payload: {
          board_snapshot: svg,
        },
      });
    },
  },
};
</script>

<style scoped>
button.btn:focus {
  box-shadow: none;
}

#canvas {
  background: transparent !important;
}

button.border {
  border-color: #b7b7b7 !important;
  border-radius: 0.25rem;
}

div.dropdown-menu {
  min-width: 0;
}

.w-200 {
  min-width: 200px;
}

.form-control {
  background-color: #fff;
  border: none;
}

input[type='number'] {
  -moz-appearance:textfield;
}

input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  display: none;
  margin: 0;
}

.row-eq-height {
  display: -webkit-box;
  display: -webkit-flex;
  display: -ms-flexbox;
  display:         flex;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  min-width: 100%;
  z-index: 50;
}

#board-canvas--tools * {
  z-index: 100;
}
</style>
