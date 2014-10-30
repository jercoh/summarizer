(function(){
    $('#start-btn').click(function() {
    	$("#cover").fadeOut(300, function() {
    		$("#form").show();
    	});
    });
    $('#summarizeit').click(function() {
        var url = $('#url').val();
        $(location).attr('href','/post?url='+url);
    });
})();