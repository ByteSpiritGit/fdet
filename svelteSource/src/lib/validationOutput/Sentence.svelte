<script lang="ts">
   import SentenceValidation from "./SentenceValidation.svelte";
   import hideImg from "../../assets/icons/hide.png";

   export let claim: {
      claim: string,
      evidence: string,
      label: string,
      refutes: number,
      supports: number,
      nei: number,
      justify: string,
      url: Array<string>,
      is_error: boolean
   };
   
   export let outputId: string = "sentence_404_not_found";
   export let clicked = false;
   export let whenClicked: () => void = () => { console.log("clicked"); };

   export let onClick: () => void = () => { 
      console.log("Sentence clicked: " + claim.claim)
      let target = document.getElementById(outputId);
      whenClicked();
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

<a href="# " class="sentence" on:click={onClick}>{claim.claim}</a>

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