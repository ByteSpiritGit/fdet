<script lang="ts">
   import PercentageBar from "./PercentageBar.svelte";

   export let claim: string;
   export let evidence: string;
   export let label: string;
   export let refutes: number;
   export let supports: number;
   export let justify: string;
   export let id: string;

   export let show: boolean = false;
   
   export let color: string = "var(--color-secondary)";
</script>

<button style="background-color: {color};" class="output-validation-section" data-shown="{show}" on:click={() => { show = !show; }} id={id}>
   <h3>{claim}</h3>
   <div class="dropdown">
      <p class="label">Label: {label}</p>

      <PercentageBar supports={supports} refutes={refutes}/>

      <div class="evidence">
         <p>Evidence:</p>
         <p>{evidence}</p>
      </div>

      <div class="evidence">
         <p>Justification:</p>
         <p>{justify}</p>
      </div>
   </div>
</button>

<style>
   p {
      margin: 0;
      padding: 0;
   }

   h3 {
      margin: 0;
      padding: 0;

      text-align: left;
   }

   .output-validation-section {
      width: 100%;
      /* background-color: var(--color-secondary); */
      
      border: none;
      outline: none;
      cursor: pointer;

      -webkit-user-select: none;
      user-select: none;

      display: flex;
      flex-direction: column;
      justify-content: center;
      
      color: var(--color-text);
      font-size: 1em;

      border-radius: 10px;

      margin-bottom: 10px;
      padding: 10px;
   }

   .dropdown {
      display: none;

      width: 50%;
      min-width: 900px;
   }

   .output-validation-section[data-shown="true"] .dropdown {
      display: flex;
      flex-direction: column;
      align-items: flex-start;

      color: var(--color-text);

      font-size: 1em;
   }

   .output-validation-section[data-shown="true"] {
      border-style: solid;
      border-width: 2px;
      border-color: var(--color-secondary);
      animation: colorFade 1s;
   }

   @keyframes colorFade {
      100% {
         border-color: var(--color-secondary);
      }
      50% {
         border-color: var(--color-tertiary);
      }
      0% {
         border-color: var(--color-secondary);
      }
   }

   .label {
      font-weight: 500;

      background-color: var(--color-tertiary);
      padding: 0.3em;
      border-radius: 7px;

      margin-bottom: 0.5em;
      margin-top: 0.5em;
   }

   .evidence {
      display: flex;
      flex-direction: column;
      align-items: flex-start;

      margin-top: 0.5em;
   }

   .evidence > p {
      margin: 0;
      padding: 0;

      text-align: left;
   }
</style>