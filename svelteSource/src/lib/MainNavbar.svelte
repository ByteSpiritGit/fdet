<script lang="ts">

</script>

<div class="navbar">
    <div data-page="1">Home</div>
    <div data-page="2">About</div>
    <div data-page="3">Learn</div>
    <div data-page="4">Contact</div>
</div>

<style>
    .navbar {
        display: flex;
        flex-direction: row;
        justify-content: space-around;

        margin: 0;
        padding: 10px;

        width: 50%;

        border-radius: 0 0 10px 10px;
    }

    .navbar > div {
        color: white;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        cursor: pointer;
    }
</style>
