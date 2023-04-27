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
      supports: number,
      justify: string,
   }>;

   onMount(() => {
      claims.forEach(claim => {
         new Sentence({
            target: claimSection,
            props: {
               text: claim.claim,
               id: `${claims.indexOf(claim)}`
            }
         })

         new SentenceValidation({
            target: validationSection,
            props: {
               claim: claim.claim,
               evidence: claim.evidence,
               label: claim.label,
               refutes: claim.refutes,
               supports: claim.supports,
               id: `${claims.indexOf(claim)}`,
               show: false,
               justify: claim.justify
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
      display: block;
      position: sticky;
      top: 60px;
      z-index: 200;
      background-color: var(--color-secondary);

      border-radius: 10px;
      
      overflow: auto;

      margin: 10px;
      padding: 10px;

      margin-top: 60px;

      border: 2px solid var(--color-tertiary);
   }

   .claim-section p {
      margin: 0;
      padding: 0;

      color: var(--color-text);
      text-decoration: none;
      font-size: 1em;
      font-weight: 500;

      -webkit-user-select: none;
      user-select: none;
   }

   .validation-section {
      display: flex;
      /* flex-wrap: wrap; */
      flex-direction: column;
      justify-content: center;
      
      overflow: auto;

      margin: 10px;
      margin-bottom: 195px;
      /* margin-bottom: 800px; */
   }

   @media (max-width: 768px) {
      .claim-section {
         margin-top: 115px;
      }
   } 
</style>