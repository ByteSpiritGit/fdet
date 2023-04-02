<script lang="ts">
   export let text: string;
   export let whenClicked: () => void;
   export let disabled: boolean = false;
</script>

<div class="button">
   <button on:click={whenClicked} disabled={disabled}>{text}</button>
</div>

<style>
   @import "../main.css";

   .button {
      display: flex;
      align-items: center;
      justify-content: center;
   }

   .button > button {
      background-color: var(--color-tertiary);
      color: var(--color-text);
      border: none;
      border-radius: 10px;

      padding: 8px 20px;
      font-size: 1.2em;
      font-weight: 500;
      text-transform: uppercase;
      cursor: pointer;
      transition: 0.1s;
   }

   .button > button:disabled {
      background-color: red;
      opacity: 0.5;
      cursor: grabbing;
   }

</style>