function searchTable() {
    let input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("searchInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("dataTable");
    tr = table.getElementsByTagName("tr");

    let resultCount = 0;

    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[1];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].classList.remove("hidden");
                resultCount++;
            } else {
                tr[i].classList.add("hidden");
            }
        }
    }

    const resultCountElement = document.getElementById("resultCount");

    if (filter === "") {
        resultCountElement.style.display = "none";
    } else {
        resultCountElement.style.display = "block";
        resultCountElement.textContent = `${resultCount} résultat(s)`;
    }
}