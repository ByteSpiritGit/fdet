<script lang="ts">
   export let claim: string;
   export let evidence: string;
   export let label: string;
   export let refutes: number;
   export let supports: number;
   export let id: string;

   let show: boolean = false;
   
</script>

<button class="output-validation-section" data-shown="{show}" on:click={() => { show = !show; }} id={id}>
   <h3>{claim}</h3>
   <div class="dropdown">
      <p class="label">Label: {label}</p>
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
      width: 100%;
      background-color: var(--color-secondary);
      
      border: none;
      outline: none;
      cursor: pointer;

      -webkit-user-select: none;
      user-select: none;

      display: flex;
      flex-direction: column;
      justify-content: center;
      
      color: var(--color-text);
      font-size: 1em;

      border-radius: 10px;

      margin-bottom: 10px;
      padding: 10px;
   }

   .dropdown {
      display: none;
   }

   .output-validation-section[data-shown="true"] .dropdown {
      display: flex;
      flex-direction: column;
      align-items: flex-start;

      color: var(--color-text);

      font-size: 1em;
   }

   .output-validation-section[data-shown="true"] {
      border-style: solid;
      border-width: 2px;
      border-color: var(--color-secondary);
      animation: colorFade 1s;
   }

   @keyframes colorFade {
      100% {
         border-color: var(--color-secondary);
      }
      50% {
         border-color: var(--color-tertiary);
      }
      0% {
         border-color: var(--color-secondary);
      }
   }
</style>