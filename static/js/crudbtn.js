(function (){
    console.log("CRUD Button JS loaded");

    const btnDelete = document.querySelectorAll('.btn-delete');

    btnDelete.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmation = confirm("Are you sure you want to delete this item?");
            if (!confirmation) {
                e.preventDefault();
            }
        });
    });

})();