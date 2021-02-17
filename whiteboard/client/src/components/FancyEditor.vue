<template>
  <div class="row">
    <div
      id="editor-container"
      class="col">
      <div class="row m-0 mb-1">
        <editor-menu-bar
          :editor="editor">
          <div
            slot-scope="{ commands, isActive }"
            class="row m-0">

            <button
              :class="[ isActive.bold() ? 'btn-success' : 'btn-default', toolBtnClass ]"
              @click="commands.bold">
              <font-awesome-icon
                icon="bold" />
            </button>

            <button
              :class="[ isActive.italic() ? 'btn-success' : 'btn-default', toolBtnClass ]"
              @click="commands.italic">
              <font-awesome-icon
                icon="italic" />
            </button>

            <button
              :class="[ isActive.strike() ? 'btn-success' : 'btn-default', toolBtnClass ]"
              @click="commands.strike">
              <font-awesome-icon
                icon="strikethrough" />
            </button>

            <button
              :class="[ isActive.underline() ? 'btn-success' : 'btn-default', toolBtnClass ]"
              @click="commands.underline">
              <font-awesome-icon
                icon="underline" />
            </button>

            <button
              :class="[ isActive.code() ? 'btn-success' : 'btn-default', toolBtnClass ]"
              @click="commands.code">
              <font-awesome-icon
                icon="code" />
            </button>

            <button
              :class="[ isActive.paragraph() ? 'btn-success' : 'btn-default', toolBtnClass ]"
              @click="commands.paragraph">
              <font-awesome-icon
                icon="paragraph" />
            </button>

            <div class="dropdown">
              <button
                id="headings-menu"
                :class="[ isActive.heading() ? 'btn-success' : 'btn-default', toolBtnClass ]"
                class="dropdown-toggle"
                data-toggle="dropdown">
                <font-awesome-icon
                  icon="heading" />
              </button>

              <div class="dropdown-menu">
                <a
                  :class="{ 'bg-success': isActive.heading({ level: 1 }) }"
                  class="dropdown-item"
                  href="#"
                  @click.prevent="commands.heading({ level: 1 })">
                  Heading 1
                </a>

                <a
                  :class="{ 'bg-success': isActive.heading({ level: 2 }) }"
                  class="dropdown-item"
                  href="#"
                  @click.prevent="commands.heading({ level: 2 })" >
                  Heading 2
                </a>

                <a
                  :class="{ 'bg-success': isActive.heading({ level: 3 }) }"
                  class="dropdown-item"
                  href="#"
                  @click.prevent="commands.heading({ level: 3 })" >
                  Heading 3
                </a>
              </div>

            </div>

            <button
              :class="[ isActive.bullet_list() ? 'btn-success' : 'btn-default', toolBtnClass ]"
              @click="commands.bullet_list">
              <font-awesome-icon
                icon="list-ul" />
            </button>

            <button
              :class="[ isActive.ordered_list() ? 'btn-success' : 'btn-default', toolBtnClass ]"
              @click="commands.ordered_list">
              <font-awesome-icon
                icon="list-ol" />
            </button>

            <button
              :class="[ isActive.code_block() ? 'btn-success' : 'btn-default', toolBtnClass ]"
              @click="commands.code_block">
              <font-awesome-icon
                icon="code" />
            </button>

            <button
              :class="toolBtnClass"
              @click="commands.undo">
              <font-awesome-icon
                icon="undo" />
            </button>

            <button
              :class="toolBtnClass"
              @click="commands.redo">
              <font-awesome-icon
                icon="redo" />
            </button>

          </div>
        </editor-menu-bar>
      </div>
      <div
        class="row m-0 align-items-stretch">
        <editor-content
          :editor="editor"
          class="border rounded bg-default p-3 editor br-1 col" />
      </div>
    </div>
  </div>
</template>

<script>
import { Editor, EditorContent, EditorMenuBar } from 'tiptap';
import { CodeBlock, HardBreak, Heading, OrderedList, BulletList, ListItem,
  TodoItem, TodoList, Bold, Code, Italic, Link, Strike, Underline, History }
  from 'tiptap-extensions';

export default {
  name: 'FancyEditor',
  components: {
    EditorContent,
    EditorMenuBar,
  },
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    value: { type: String, default: '' },
    placeholder: { type: String, default: '' },
  },
  data() {
    return {
      editor: null,
      changed: false,
      afterChange: false,
      toolBtnClass: ['btn', 'btn-sm', 'border', 'mr-1', 'mb-1'],
    };
  },
  watch: {
    value(newVal) {
      if (!this.afterChange) {
        this.editor.setContent(newVal);
      } else {
        this.afterChange = false;
      }

      this.changed = true;
    },
  },
  mounted() {
    const self = this;

    this.editor = new Editor({
      content: this.value || '',
      extensions: [
        new BulletList(),
        new CodeBlock(),
        new HardBreak(),
        new Heading({ levels: [1, 2, 3] }),
        new ListItem(),
        new OrderedList(),
        new TodoItem(),
        new TodoList(),
        new Bold(),
        new Code(),
        new Italic(),
        new Link(),
        new Strike(),
        new Underline(),
        new History(),
      ],
      onUpdate: (state) => {
        self.afterChange = true;
        self.$emit('change', state.getHTML());
      },
    });
  },
  beforeDestroy() {
    this.editor.destroy();
  },
  methods: {
  },
};
</script>

<style lang="scss">
.editor p.is-empty:first-child::before {
  content: attr(data-empty-text);
  float: left;
  color: #aaa;
  pointer-events: none;
  height: 0;
  font-style: italic;
}
</style>
