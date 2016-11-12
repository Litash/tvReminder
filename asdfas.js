$.ajax({
    url: 'api/DashboardApi',
    type: 'GET',
    dataType: 'json',
})
.done(function(data) {
    for (var i = data.length - 1; i >= 0; i--) {
        console.log(data[i].name);
    }
})
.fail(function() {
    console.log("error");
})
.always(function() {
    console.log("complete");
});
