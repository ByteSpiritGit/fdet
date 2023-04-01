<script lang="ts">
   import OldEvaluationPage from "./lib/OldEvaluationPage.svelte";
   import NewEvaluationPage from "./lib/NewEvaluationPage.svelte";
   let page;
</script>

<!-- * HTML -->
<main>
   <input type="checkbox" bind:checked={page} class="whichSwitch" />

   {#if page}
      <OldEvaluationPage />
   {:else if !page}
      <NewEvaluationPage />
   {/if}

</main>

<!-- * css -->
<style>
   main {
      margin: 0;
      padding: 0;
   }

   .whichSwitch {
      visibility: hidden;
      position: absolute;
      left: -20px;
      top: -20px;
      
      margin: 0;
      cursor: pointer;
   }

   .whichSwitch::before {
      left: 25px;
      top: 25px;

      content: "";
      /* visibility: visible; */
      display: block;

      position: absolute;

      width: 40px;
      height: 20px;

      background-color: #1f1f20;
      border-radius: 5px;

      z-index: 50;
   }

   .whichSwitch::after {
      left: 25px;
      top: 25px;

      content: "0";
      /* visibility: visible; */
      display: block;

      position: absolute;

      width: 20px;
      height: 20px;

      background-color: rgb(199, 199, 199);
      border-radius: 5px;

      z-index: 51;
      transition: 0.2s;

      color: #1f1f20;
      font-size: 1.2rem;
      text-align: center;
   }

   .whichSwitch:checked::after {
      margin-left: 20px;
      content: "1";
   }

</style>
