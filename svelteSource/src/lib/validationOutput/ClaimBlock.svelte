<script lang="ts">
   import { onMount } from "svelte";

   import Sentence from "./Sentence.svelte";
   import SentenceValidation from "./SentenceValidation.svelte";
   
   let claimSection;
   let validationSection;

   export let claims: Array<{
      claim: string,
      evidence: string,
      label: string,
      refutes: number,
      supports: number
   }>;

   onMount(() => {
      claims.forEach(claim => {
         new Sentence({
            target: claimSection,
            props: {
               text: claim.claim,
               id: claim.claim
            }
         })

         new SentenceValidation({
            target: validationSection,
            props: {
               claim: claim.claim,
               evidence: claim.evidence,
               label: claim.label,
               refutes: claim.refutes,
               supports: claim.supports
            }
         })
      });
   })
</script>

<output>
   <section class="claim-section" bind:this={claimSection}>
      <p>Claim: </p>
   </section>
   <section class="validation-section" bind:this={validationSection}></section>
</output>

<style>
   .claim-section {
      display: flex;
      justify-content: flex-start;
      
      overflow: auto;

      padding: 0.6em;
   }

   .claim-section p {
      margin: 0;
      padding: 0;

      color: var(--color-text);
      text-decoration: none;
      font-size: 1em;
      font-weight: 300;

      -webkit-user-select: none;
      user-select: none;
   }

   .validation-section {
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      
      overflow: auto;

      padding: 0.7em;
   }
</style>