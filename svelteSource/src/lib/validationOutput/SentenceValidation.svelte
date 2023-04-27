<script lang="ts">
   import PercentageBar from "./PercentageBar.svelte";

   export let claim: {
      claim: string,
      evidence: string,
      label: string,
      refutes: number,
      supports: number,
      nei: number,
      justify: string,
   };

   export let id: string;
</script>

<section id={id} class="output-validation-section">
   <h3>{claim}</h3>
   <div class="dropdown">
      <p class="label">Label: {claim.label}</p>

      <PercentageBar supports={claim.supports} refutes={claim.refutes} nei={claim.nei}/>

      <div class="evidence">
         <p>Evidence:</p>
         <p>{claim.evidence}</p>
      </div>

      <div class="evidence">
         <p>Justification:</p>
         <p>{claim.justify}</p>
      </div>
   </div>
</section>

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
      width: 50%;
      min-width: 900px;
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