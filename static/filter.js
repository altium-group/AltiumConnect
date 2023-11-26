function filterTable() {
    let dropdown = document.getElementById("filterDropdown");
    let selectedValue = dropdown.value.toLowerCase();

    let table = document.getElementById("dataTable");
    let tr = table.getElementsByTagName("tr");

    for (let i = 0; i < tr.length; i++) {
        let td = tr[i].getElementsByTagName("td")[4];
        if (td) {
            let cellText = td.textContent.toLowerCase();
            if (selectedValue === "all" || cellText.includes(selectedValue)) {
                tr[i].classList.remove("hidden");
            } else {
                tr[i].classList.add("hidden");
            }
        }
    }
}