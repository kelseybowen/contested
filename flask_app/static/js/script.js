
function revealContestTable(contest_id){
    let table_div = document.getElementById("contest-table-div")
    if (table_div.style.display === 'none'){
        table_div.style.display = "block"
    } else {
        table_div.style.display = 'none'
    }
    // console.log(`==== contest id = ${contest_id}`) // WORKS

}

