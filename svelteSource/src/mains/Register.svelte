<script lang="ts">
   import Navbar from "../lib/Navbar.svelte";
   import Footer from "../lib/Footer.svelte";
   import ReqisterSection from "../lib/log-reg/ReqisterSection.svelte";

   import { onMount } from "svelte";

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

   onMount(() => {
      getCsrfToken();
   });
</script>

<Navbar />

<ReqisterSection getCookie={getCookie} />

<Footer />

<style>
   
</style>