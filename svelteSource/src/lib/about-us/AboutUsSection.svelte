<script lang="ts">
  import janImg from "../../assets/team-photo/Jan.jpg";
  import ondraImg from "../../assets/team-photo/Ondra.jpg";
  import davidImg from "../../assets/team-photo/David.jpg";
  import blankaImg from "../../assets/team-photo/Blanka.jpg";
  import martinImg from "../../assets/team-photo/Martin.jpg";
  import github from "../../assets/socials/github.png";
  import linkedin from "../../assets/socials/linkedin.png";
  
  let members = [
    {
      name: "Jan Soukeník",
      role: "Data sorcerer",
      linkedin: "https://www.linkedin.com/in/jan-soukenik/",
      github: "https://github.com/Dzeniks",
      img: janImg,
    },
    {
      name: "Ondřej Šteffan",
      role: "Frontend developer",
      github: "https://github.com/OriginalStefikO",
      linkedin: "https://www.linkedin.com/in/steffan-ondrej/",
      img: ondraImg,
    },
    {
      name: "David Vrtílek",
      role: "Backend developer",
      linkedin: "https://www.linkedin.com/in/vrtilek-david/",
      github: "https://github.com/TheLastMercy",
      img: davidImg,
    },
    {
      name: "Blanka Ducháčková",
      role: "Graphic designer",
      linkedin: "#",
      github: "https://github.com/Bllanch",
      img: blankaImg,
    },
    {
      name: "Martin Minařík",
      role: "Tester",
      linkedin: "#",
      github: "https://github.com/MartinTheDoge",
      img: martinImg,
    },
  ];
</script>

<section class="Us">
  {#each members as member}
    <section class="block">
      <img class="photo-member" src={member.img} alt={member.name} />
      <div class="info">
        <div>
          <h2>{member.name}</h2>
          <h3>{member.role}</h3>
        </div>
        <div class="contact-bar">
          <a href="{member.github}" class="mask" data-png={github}>
            <img src={github} alt="github" />
          </a>
          <a href="{member.linkedin}" class="mask" data-png={linkedin}>
            <img src={linkedin} alt="linkedin"/>
          </a>
        </div>
      </div>
    </section>
  {/each}
</section>

<style>
  .contact-bar {
    /* border: 2px solid white; */
    margin-top: 10%;

    display: flex;
    align-items: center;
    justify-content: center;

    width: 100%;
    height: auto;
  }

  .Us {
    /* border: 2px solid white; */

    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-evenly;

    max-width: 80%;
    min-width: 60%;
    
    height: 100%;
    
    margin: 0 auto;
    margin-top: 8%;

    gap: 10%;
  }

  .info{
    margin: 5%;
  }
  
  .block {
    /* border: 2px solid white; */

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    width: 15%;
    height: auto;

    margin: 0 auto;

    min-height: 15%;
  }
  .mask {
    display: inline-block;
    
    min-width: 30px;
    max-width: 60px;
    margin: 5%;
  }

  img {
    border-radius: 10%;
    width: 100%;
    height: 100%;
    object-fit: cover;
    margin: 1%;
  }


  h2 {
    margin: 0.5em;
    padding: 0.4em 0.7em;

    white-space: nowrap;

    background-color: #393e469c;
    border-radius: 0.5em 0.5em 0.2em 0.2em;

    text-align: center;
  }

  h3 {
    margin: 0;
    margin-top: 0.2em;

    white-space: nowrap;

    color: var(--color-text-darker);

    background-color: #393d4491;
    border-radius: 0.2em 0.2em 0.5em 0.5em;
    text-align: center;

    padding: 0.2em 0.5em;
  }

  @media (max-width: 1280px) {
    .Us {

      position: relative;

      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-evenly;

      max-width: 80%;


      height: 100%;

      margin-top: 8em;
      margin-bottom: 4em;

      gap: 6em;
    }

    .block {
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: center;

      width: auto;
      height: 10em;

      margin: 0 auto;
      min-height: 20em;
    }
    .contact-bar {
      min-width: auto;
      min-height: 30%;
    }

    .photo-member {
      width: 100%;
      height: 100%;
      object-fit: cover;
      margin-right: 30%;
    }
  }

  @media (max-width: 680px) {
    .Us {
      margin-top: 12em;
      max-width: 100%;
      margin-top: 8em;

      flex-direction: column;
      width: fit-content;
      height: auto;

      margin-bottom: 15%;
      gap: 0.5em;
    }

    .block {
      width: 80%;
      height: auto;
      margin: 5%;
      flex-direction: column;
    }

    .info{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }

    img{
      margin: 0 auto;
    }

  }

  @media (max-height: 560px) {
    .Us {
      max-width: 100%;
      margin-top: 4em;
      gap: 4em;
    }
  }
</style>
