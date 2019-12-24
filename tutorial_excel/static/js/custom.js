$(document).ready(function(){
	$('.btn-delete-sale').click(function(){
		var sale = $(this).data('sale-number');
		alert('Are you sure want to delete Oder with number ' + sale);
	});
});