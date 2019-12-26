$("#test").click(function(){
    console.log('dan')
    $.ajax({
        url : '/findName?name=' + document.getElementById('name').value + "&age=" + document.getElementById("age").value,
        success : function(data){
            $("#trueName").html($("#trueName").html() + '\n' + data['name'] + "age is " + data['age'] )
        }
    });
});

$('#test2').click(function(){
    $.ajax({
        url : '/findName?name=' + document.getElementById('name').value + "&age=" + document.getElementById('age').value,
        success : function(data){
            $("#trueName").html($("#trueName").html() + '\n' + data['age'] + "age is " + data['name'] )
        }
