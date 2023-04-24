<nav class="navbar">
   <section class="logo-section">
      <a href="/#/evaluations">**Logo**</a>
   </section>
   <section class="menu-section">
      <a href="/">Home</a>
      <a href="/evaluation?text=The sky is blue">About us</a>
      <a href="/">Learn</a>
      <a href="https://github.com/fdet/fDet">Github</a>
      <a href="/">History</a>
   </section>
   <section class="profile-section">
      <a href="/#/login">**profile**</a>
   </section>
</nav>

<style>
   @import "../main.css";

   .navbar {
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-between;

      font-size: 1.2em;
      font-weight: 500;
      text-transform: uppercase;

      height: 55px;
   }

   .navbar > section {
      background-color: var(--color-secondary);
      height: 100%;

      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: baseline;

      overflow: hidden;
   }

   .navbar > section > a {
      color: var(--color-text);
      text-decoration: none;

      width: 100%;
      height: 100%;

      display: flex;
      align-items: center;
      justify-content: center;

      transition: 0.1s;
   }

   .menu-section {
      border-radius: 0 0 10px 10px;
      width: fit-content;
      min-width: 440px;
   }

   .menu-section > a {
      padding: 0 20px;
      white-space: nowrap;
   }

   .navbar > .profile-section {
      border-radius: 0 0 0 10px;
      width: 180px;
   }

   .logo-section {
      border-radius: 0 0 10px 0;
      width: 180px;
   }

   .navbar > .menu-section > a:hover {
      background-color: var(--color-tertiary);
   }
</style>