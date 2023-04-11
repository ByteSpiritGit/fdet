<script lang="ts">
   export let claim: string;
   export let evidence: string;
   export let label: string;
   export let refutes: number;
   export let supports: number;
   
   let show: boolean = false;
   
</script>

<button class="output-validation-section" data-shown="{show}" on:click={() => { show = !show; }}>
   <h3>{claim}</h3>
   <div class="dropdown">
      <p>Label: {label}</p>
      <p>Supports: {supports}</p>
      <p>Refutes: {refutes}</p>
      <p>Evidence: <br />{evidence}</p>
   </div>
</button>

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
      
      border: none;
      outline: none;
      cursor: pointer;

      -webkit-user-select: none;
      user-select: none;

      margin-bottom: 10px;
      padding: 10px;

      display: flex;
      flex-direction: column;
      justify-content: center;
      
      color: var(--color-text);
      font-size: 1em;
   }

   .dropdown {
      display: none;
   }

   .output-validation-section[data-shown="true"] .dropdown {
      display: flex;
      flex-direction: column;
      align-items: flex-start;

      margin-top: 10px;

      color: var(--color-text);

      font-size: 1em;
   }
</style>