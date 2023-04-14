<script lang="ts">
   export let supports: number;
   export let refutes: number;

   supports = parseFloat((supports * 100).toFixed(2))
   refutes = parseFloat((refutes * 100).toFixed(2))
   if (refutes + supports > 100) {
      supports /= 100;
      refutes /= 100;
   }
</script>

<div class="text-holder">
   <p class="text">Supports</p>
   <p class="text">Refutes</p>
</div>
<div class="percentage-bar">
   <div class="supports bar" style="width: {supports}%">
      {#if supports >= 5}
         {supports}%
      {/if}
   </div>
   <div class="refutes bar" style="width: {refutes}%">
      {#if refutes >= 5}
         {refutes}%
      {/if}
   </div>
</div>

<style>
   .percentage-bar {
      width: 100%;
      height: 1.5em;

      background-color: var(--color-primary);

      display: flex;
      flex-direction: row;

      position: relative;

      border-radius: 0.25em;

      overflow: hidden;
   }

   .supports {
      height: 100%;
      background-color: var(--color-tertiary);
   }

   .refutes {
      height: 100%;
      background-color: var(--color-primary);
   }

   .bar {
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
   }

   .text-holder {
      display: flex;
      flex-direction: row;
      justify-content: space-between;

      width: 100%;

      margin-bottom: 0.25em;
   }
   
   .text {
      margin: 0;
      padding: 0;

      height: 100%;
   }
</style>