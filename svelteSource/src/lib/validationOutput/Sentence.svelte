<script lang="ts">
   import SentenceValidation from "./SentenceValidation.svelte";

   export let claim: {
      claim: string,
      evidence: string,
      label: string,
      refutes: number,
      supports: number,
      nei: number,
      justify: string,
   };
   // export let id: string = "sentence_404_not_found";
   export let outputId: string = "sentence_404_not_found";

   export let clicked = false;

   export let onClick: () => void = () => { 
      console.log("Sentence clicked: " + claim.claim)
      let target = document.getElementById(outputId);
      clearIt(target);
      new SentenceValidation({
         target: target,
         props: {
            claim: claim
         }
      })
      clicked = true;
   };

   function clearIt(target) {
      target.innerHTML = "";
   }

   // ! on hover should be a overlay over output, so it doesnt delete the clicked output
</script>
<!-- TODO eeee -->

<!-- <a href="#{id}" on:click={doo}>{text}</a> -->
<a href="#{outputId}" class="sentence" on:click={onClick}>{claim.claim}</a>

<style>
   a {
      margin: 0;
      padding: 0;

      margin-left: 0.1em;
      margin-right: 0.1em;
      
      color: var(--color-text);
      text-decoration: none;

      cursor: pointer;
      
      font-size: 1.1em;
      font-weight: 300;

      transition: 0.1s;
   }

   a:hover {
      text-decoration: underline;
      background-color: var(--color-tertiary-alpha);
      border-radius: 0.3em;
   }
</style>