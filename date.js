var today = new Date;

// const optionsDay = { weekday: 'long' , month: 'long'};
todayDay = new Intl.DateTimeFormat('en-US', { weekday: 'long' }).format(today);
todayMonth = new Intl.DateTimeFormat('en-US', { month: 'long' }).format(today);

const nth = function(d) {
    if (d > 3 && d < 21) return 'th';
    switch (d % 10) {
        case 1:
            return "st";
        case 2:
            return "nd";
        case 3:
            return "rd";
        default:
            return "th";
    }
}


document.getElementById('date').innerHTML = today.getDate() + nth(today.getDate())
document.getElementById('day').innerHTML = todayDay;
document.getElementById('month').innerHTML = todayMonth;

console.log("updated date");