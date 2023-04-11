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
               text: claim.claim
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
   <section class="claim-section" bind:this={claimSection}></section>
   <section class="validation-section" bind:this={validationSection}></section>
</output>

<style>
   .claim-section {
      display: flex;
      width: 50%;
      height: 100%;
   }
</style>