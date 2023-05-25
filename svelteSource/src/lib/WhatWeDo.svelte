<section class="whatWeDo">
    <section class="block">
        <h3>You state a fact</h3>
        <p>"The human body is made up<br />of about 60% water"</p>
    </section>
    <div class="hyphen" />
    <section class="block">
        <h3>We find the evidence</h3>
        <p>"The human body contains<br />from 55% to 78% of water"</p>
    </section>
    <div class="hyphen" />
    <section class="block">
        <h3>And return results</h3>
        <p>"Supports: 83.74%<br />Refutes: 16.26%"</p>
    </section>
</section>

<style>
    .whatWeDo {
        position: relative;

        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-evenly;

        max-width: 46em;

        height: 100%;

        margin: 0 auto;
        margin-top: 70px;
    }

    .hyphen {
        width: 2em;
        height: 0.25em;

        border-radius: 2em;

        background-color: var(--color-text);

        margin: 0 1em;
    }

    h3 {
        margin: 0;
        padding: 0.4em 0.7em;

        white-space: nowrap;

        background-color: #393e469c;
        border-radius: 0.5em 0.5em 0.2em 0.2em;

        text-align: center;
    }

    p {
        margin: 0;
        margin-top: 0.2em;

        white-space: nowrap;

        color: var(--color-text-darker);

        background-color: #393d4491;
        border-radius: 0.2em 0.2em 0.5em 0.5em;
        text-align: center;

        padding: 0.2em 0.5em;
    }

    @media (max-width: 680px) {
        .whatWeDo {
            flex-direction: column;

            margin-top: 8em;

            width: fit-content;

            margin-bottom: 45%;
        }

        .hyphen {
            width: 0.25em;
            height: 1em;

            margin: 0.5em 0;
        }

        .block {
            width: 100%;
        }
    }

    @media (max-height: 560px) {
        .whatWeDo {
            margin-top: 8em;
        }
    }
</style>
