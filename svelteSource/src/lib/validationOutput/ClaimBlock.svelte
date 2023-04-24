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
               color: claims.indexOf(claim) % 2 == 0 ? "var(--color-secondary-v2)" : "var(--color-secondary)"
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
   <div class="gradient"></div>
</output>

<style>
   .claim-section {
      display: block;
      position: sticky;

      background-color: var(--color-secondary);

      border-radius: 10px;
      
      overflow: auto;

      margin: 10px;
      padding: 10px;
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
      margin-bottom: 80px;
      /* margin-bottom: 800px; */
   }

   .gradient {
      position: fixed;
      bottom: 50px;
      left: 0;
      right: 0;
      height: 40px;
      background: linear-gradient(rgba(0, 0, 0, 0) 0%, var(--color-primary-alpha) 75%, var(--color-primary) 100%);
   }
</style>