<script lang="ts">
   export let text: string = "Sentence missing";
   export let id: string = "sentence_404_not_found";
</script>

<a href="#{id}">{text}.</a>

<style>
   a {
      margin: 0;
      padding: 0;

      margin-left: 0.15em;
      margin-right: 0.15em;
      
      color: var(--color-text);
      text-decoration: none;

      cursor: pointer;
      
      font-size: 1em;
      font-weight: 300;

      transition: color 0.2s;
   }

   a:hover {
      text-decoration: underline;
   }
</style>