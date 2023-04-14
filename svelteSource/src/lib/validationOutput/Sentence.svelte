<script lang="ts">
   export let text: string = "Sentence missing";
   export let id: string = "sentence_404_not_found";
</script>

<a href="#{id}" on:click={() => {
   let element = document.getElementById(id);
   let validation_section = document.getElementsByClassName("validation-section")[0];
   let sentences = validation_section.children;
   for (let i = 0; i < sentences.length; i++) {
      sentences[i].setAttribute("data-shown", "false");
   }
   element.dataset.shown = "true";
}}>{text}.</a>

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

      transition: color 0.2s;
   }

   a:hover {
      text-decoration: underline;
      background-color: var(--color-tertiary-alpha);
      border-radius: 0.3em;
   }
</style>