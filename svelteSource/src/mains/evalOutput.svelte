<script lang="ts">
   import Navbar from "../lib/Navbar.svelte";
   import Footer from "../lib/Footer.svelte";
   import ClaimBlock from "../lib/validationOutput/ClaimBlock.svelte";
   import NotificationBlock from "../lib/notifications/NotificationBlock.svelte";

   import { onMount } from "svelte";

   let toEvaluate: string;
   if (new URLSearchParams(window.location.search).get("text")) {
      toEvaluate = new URLSearchParams(window.location.search).get("text");
   }

   function getCsrfToken() {
      var xhr = new XMLHttpRequest();
      // Set up a callback function to handle the response
      xhr.onreadystatechange = function () {
         if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
               try {
                  document.cookie =
                     "csrftoken=" +
                     encodeURIComponent(
                        JSON.parse(xhr.responseText).csrf_token
                     ) +
                     "; path=/";
               } catch (error) {
                  console.log(error);
               }
            } else {
               console.log("Request failed");
            }
         }
      };

      xhr.open("GET", "/csrf_view");
      xhr.send();
   }

   function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
         const cookies = document.cookie.split(";");
         for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + "=") {
               cookieValue = decodeURIComponent(
                  cookie.substring(name.length + 1)
               );
               break;
            }
         }
      }
      return cookieValue;
   }

   // async function getEvaluated(text: string, type = "") {
   //    let url: string;

   //    if (window.sessionStorage.getItem("evalued") && !text) {
   //       console.log("from sessionStorage");
   //       return JSON.parse(window.sessionStorage.getItem("evalued"));
   //    }

   //    switch (type) {
   //       case "Dummy":
   //          url = `/dummy?text=${text}`;
   //          break;
   //       case "Evaluation":
   //          url = `/rag_evaluation?text=${text}`;
   //          break;
   //       case "NoServer":
   //          return [
   //          ];
   //       default:
   //          url = `/evaluation?text=${text}`;
   //          break;
   //    }

   //    const csrftoken = getCookie("csrftoken");

   //    const request = new Request(url, {
   //       method: "POST",
   //       headers: { "X-CSRFToken": csrftoken },
   //       mode: "same-origin",
   //    });

   //    try {
   //       const response = (await (await fetch(request)).json()).validated;
   //       return response;
   //    } catch (error) {
   //       console.log(error);

   //       return null;
   //    }
   // }

   // async function evaluate(text: string) {
   //    if (text) {
   //       evalued = await getEvaluated(text, "Evaluation");
   //       window.sessionStorage.setItem("evalued", JSON.stringify(evalued));
   //    } else {
   //       evalued = await getEvaluated(text, "NoServer");
   //       window.sessionStorage.setItem("evalued", JSON.stringify(evalued));
   //    }

   //    const urlParams = new URLSearchParams(window.location.search);
   //    urlParams.delete("text");
   //    window.history.replaceState(
   //       {},
   //       "",
   //       `${window.location.pathname}?${urlParams}`
   //    );
   // }

   onMount(() => {
      // let text: string;
      // if (new URLSearchParams(window.location.search).get("text")) {
      //    text = new URLSearchParams(window.location.search).get("text");
      // }

      getCsrfToken();
      // evaluate(text);
   });

   let warnings;
</script>

<section>
   <Navbar />
   
   <ClaimBlock getCsrfToken={getCsrfToken} getCookie={getCookie} toEvaluate={toEvaluate} />
   
   <!-- {#if evalued}
      <ClaimBlock claims={evalued} />
   {:else if !evalued}
      <div class="loading">
         <Loading />
         <p>Calculating the universe</p>
      </div>
   {/if} -->

   <Footer />
   <NotificationBlock bind:theComponent={warnings} notificationNumber={1} />
</section>

<style>
   .loading {
      position: fixed;
      top: 48%;
      left: 50%;
      transform: translate(-50%, -50%);

      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
   }

   .loading > p {
      font-size: 1.2em;
      font-weight: 500;
      color: var(--color-text);

      margin-top: 0px;
      animation: loading 2s ease-in infinite;
   }

   @keyframes loading {
      0% {
         opacity: 0.6;
      }
      50% {
         opacity: 1;
      }
      100% {
         opacity: 0.6;
      }
   }

   
</style>
