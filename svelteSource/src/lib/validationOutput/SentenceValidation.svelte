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
</script>

<section class="output-validation-section border-top">
   <h3>{claim.claim}</h3>
   <p class="label">Label: {claim.label}</p>

   <PercentageBar supports={claim.supports} refutes={claim.refutes} nei={claim.nei}/>
   <div class="evidence">
      <p>Justification:</p>
      <p>{claim.justify}</p>
   </div>

   <div class="evidence border-top smaller-text">
      <p>Evidence:</p>
      <p>{claim.evidence}</p>
   </div>

</section>

<style>
   h3 {
      margin: 0;
      padding: 0;
   }

   p {
      margin: 0;
      padding: 0;
   }

   .border-top {
      border-top: 2px var(--color-tertiary-alpha) solid;
      margin-top: 0.5em
   }

   .smaller-text {
      font-size: 0.9rem;
   }
</style>