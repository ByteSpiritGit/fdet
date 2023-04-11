<script lang="ts">
   export let claim: string;
   export let evidence: string;
   export let label: string;
   export let refutes: number;
   export let supports: number;
   
   let show: boolean = false;
   
</script>

<section class="output-validation-section" data-shown="{show}" on:click={() => {
   show = !show;
   console.log(show);
}}>
   <h3 >{claim}</h3>
   <div class="dropdown">
      <p>Label: {label}</p>
      <p>Supports: {supports}</p>
      <p>Refutes: {refutes}</p>
      <p>Evidence: <br />{evidence}</p>
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
   }

   .output-validation-section {
      background-color: var(--color-secondary);
      margin: 20px;
      padding: 10px;
   }

   .dropdown {
      display: none;
   }

   .output-validation-section[data-shown="true"] .dropdown {
      display: block;
   }
</style>