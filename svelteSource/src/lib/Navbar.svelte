<script lang="ts">
   import Login from "../mains/Login.svelte";

   let logedin: boolean = true;
</script>

<nav class="navbar">
   <section class="menu-section">
      <a href="/">Home</a>
      <a href="/">About us</a>
      <a href="/">Learn</a>
      <a href="https://github.com/fdet/fDet">Github</a>
   </section>
   <section class="sides-section">
      <section class="logo-section">
         <h3 class="no-margin">fDet</h3>
         <p class="no-margin">by ByteSpirit</p>
      </section>
      <section class="profile-section">
         <a href="/users/login" class="no-margin">Login</a>
         <a href="/users/register" class="no-margin"><b>Register</b></a>
      </section>
   </section>
</nav>

<style>
   .logo-section {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      justify-content: center;

      padding: 0.5em;
   }

   .profile-section > a:hover{
      text-shadow: 0px 0px 1px #ffffffce, 0px 0px 10px #cccccc77;
   }

   .profile-section {
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-evenly;

      padding: 0.5em;
   }

   .no-margin {
      margin: 0;
      padding: 0;

      line-height: 1em;
   }

   a {
      color: var(--color-text);
      text-decoration: none;

      width: 100%;
      height: 100%;

      display: flex;
      align-items: center;
      justify-content: center;

      /* transition: 0.1s; */

      white-space: nowrap;

      padding: 0 0.5em;
      border: none;
   }

   a:focus {
      border: none;
      outline: 2px solid var(--color-text);
      outline-offset: -2px;
   }

   .navbar {
      position: fixed;
      top: 0;

      z-index: 200;

      width: 100%;
      height: 3.5rem;

      font-size: 1.2em;

      background-color: var(--color-primary);

      /* border-bottom: 1px solid var(--color-primary); */
      box-shadow: 0 0 10px 1px var(--color-primary);
   }
   
   .sides-section {
      position: relative;
      z-index: 250;
      top: -3.5rem;

      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-between;

      width: 100%;
      height: 3.5rem;
   }

   .sides-section > section {
      width: 150px;
      background-color: var(--color-secondary);
      height: 100%;

      border: none;
   }

   .sides-section > section:first-child {
      border-radius: 0 0 10px 0;
      /* box-shadow: 0 0 10px 1px var(--color-primary); */
   }

   .sides-section > section:last-child {
      border-radius: 0 0 0 10px;
      /* box-shadow: 0 0 10px 1px var(--color-primary); */
   }

   .menu-section {
      position: relative;
      z-index: 500;

      width: 100%;
      height: 3.5rem;

      border-radius: 0 0 10px 10px;
      width: fit-content;

      margin: 0 auto;
      left: 0;
      right: 0;


      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-evenly;

      overflow: hidden;

      background-color: var(--color-secondary);

      /* box-shadow: 0 0 10px 1px var(--color-primary); */
   }

   .menu-section > a:hover {
      background-color: var(--color-tertiary);
   }

   @media (max-width: 680px) {
      .navbar {
         height: 7rem;
      }

      .sides-section {
         top: 0;
      }

      .sides-section > section {
         width: 100%;
         
         border-width: 2px 0 0 0;
         border-color: var(--color-primary);
         border-style: solid;
      }

      .sides-section > section:first-child {
         /* border-radius: 0 0 10px 0; */
         border-radius: 0 0 0 0;
         box-shadow: none;

         border-width: 2px 2px 0 0;
      }

      .sides-section > section:last-child {
         /* border-radius: 0 0 0 10px; */
         border-radius: 0 0 0 0;
         box-shadow: none;
      }
      
      .menu-section {
         border-radius: 0 0 0 0;

         width: 100%;
      }
   }
</style>